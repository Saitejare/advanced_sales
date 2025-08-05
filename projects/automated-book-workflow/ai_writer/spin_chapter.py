import os
import requests
from dotenv import load_dotenv

from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

CHAPTER_PATH = os.path.join("output", "chapter.txt")
SPUN_PATH = os.path.join("output", "chapter_spun.txt")

def spin_chapter(input_path=CHAPTER_PATH, output_path=SPUN_PATH, style_instructions="Make the text more engaging and clear", max_tokens=1000):
    if not os.path.exists(input_path):
        print(f"Input file '{input_path}' not found.")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        chapter_text = f.read()

    prompt = f"Rewrite the following text with the following style: {style_instructions}.\n\nOriginal text:\n{chapter_text}\n\nRewritten text:"

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-70b-8192",  
        "messages": [
            {"role": "system", "content": "You are a helpful editor that improves the style of writing."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": max_tokens
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        spun_text = response.json()['choices'][0]['message']['content'].strip()

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(spun_text)

        print(f"Spun chapter saved to '{output_path}'.")
    except Exception as e:
        print("Error during AI spin:", e)

if __name__ == "__main__":
    spin_chapter()

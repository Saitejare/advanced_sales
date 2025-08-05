import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

SPUN_PATH = os.path.join("output", "chapter_spun.txt")
REVIEW_PATH = os.path.join("output", "chapter_review.txt")

def review_chapter(
    input_path=SPUN_PATH,
    output_path=REVIEW_PATH,
    review_instructions="Review the following chapter for clarity, coherence, and engagement. Suggest improvements and highlight any issues.",
    max_tokens=1000
):
    if not os.path.exists(input_path):
        print(f"Input file '{input_path}' not found.")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        spun_text = f.read()

    prompt = f"{review_instructions}\n\nChapter:\n{spun_text}\n\nReview:"

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",  # You can change to "mixtral-8x7b-32768" if needed
        "messages": [
            {"role": "system", "content": "You are an expert editor and reviewer."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.5,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        review_text = response.json()['choices'][0]['message']['content'].strip()

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(review_text)

        print(f"Review saved to '{output_path}'.")
    except Exception as e:
        print("Error during review:", e)

if __name__ == "__main__":
    review_chapter()

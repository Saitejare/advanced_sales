
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import gradio as gr
from versioning import chromadb_store
from feedback_loop import rl_reward

CHAPTER_UPLOAD = "output/uploaded_chapter.txt"
SPUN_PATH = "output/chapter_spun.txt"
REVIEW_PATH = "output/chapter_review.txt"

# Dummy reward state for display
reward_state = {"score": 0}

def upload_chapter(file):
    # Gradio may pass a string, NamedString, or file-like object depending on version
    if hasattr(file, 'read'):
        content = file.read().decode("utf-8")
    elif hasattr(file, 'value'):
        content = file.value
    else:
        content = str(file)
    with open(CHAPTER_UPLOAD, "w", encoding="utf-8") as f:
        f.write(content)
    return content

def spin_chapter_ui(text):
   
    spun = text.upper()
    with open(SPUN_PATH, "w", encoding="utf-8") as f:
        f.write(spun)
    return spun

def edit_chapter(text):
    with open(SPUN_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    return text

def review_chapter_ui(text):
    # Here you would call your LLM review function
    review = f"Review: {text[:100]}... (truncated)"
    with open(REVIEW_PATH, "w", encoding="utf-8") as f:
        f.write(review)
    return review

def submit_feedback(feedback, version_text):
    # Simulate reward assignment
    if feedback == "Approve":
        reward = 1
    elif feedback == "Reject":
        reward = -1
    else:
        reward = 0
    reward_state["score"] += reward
    # Save to ChromaDB
    chromadb_store.add_version(
        version_number=1,  # In real use, increment or track
        content=version_text,
        author="User",
        editor=None
    )
    # Trigger RL feedback loop (simulate)
    rl_reward.update_dummy_ppo_model(reward, {"total_reward": reward_state["score"], "updates": 1})
    return f"Feedback submitted. Reward: {reward}. Total score: {reward_state['score']}"

def get_spun_text():
    if os.path.exists(SPUN_PATH):
        with open(SPUN_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def get_review_text():
    if os.path.exists(REVIEW_PATH):
        with open(REVIEW_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return ""

with gr.Blocks() as demo:
    gr.Markdown("# Automated Book Publisher UI")
    upload = gr.File(label="Upload Chapter Version (.txt)")
    upload_btn = gr.Button("Upload")
    uploaded_text = gr.Textbox(label="Uploaded Chapter", lines=10)
    spin_btn = gr.Button("Spin with AI")
    spun_text = gr.Textbox(label="Spun Version", lines=10)
    edit_box = gr.Textbox(label="Edit Spun Version", lines=10)
    review_btn = gr.Button("Review with AI")
    review_text = gr.Textbox(label="Review", lines=5)
    feedback = gr.Radio(["Approve", "Neutral", "Reject"], label="Feedback")
    submit_btn = gr.Button("Submit Feedback")
    reward_score = gr.Textbox(label="Reward Score", value=str(reward_state["score"]))

    upload_btn.click(upload_chapter, upload, uploaded_text)
    spin_btn.click(spin_chapter_ui, uploaded_text, spun_text)
    spun_text.change(edit_chapter, spun_text, edit_box)
    review_btn.click(review_chapter_ui, edit_box, review_text)
    submit_btn.click(submit_feedback, [feedback, edit_box], reward_score)

demo.launch()

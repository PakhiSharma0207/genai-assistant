# app.py

from flask import Flask, request, render_template
import os
from transformers import pipeline
from document_handler import extract_text

# Initialize Flask app
app = Flask(__name__)

# Initialize summarizer
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Store extracted document text
document_text = ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global document_text

    file = request.files['file']
    if not file:
        return "No file uploaded."

    # Save file locally
    filepath = os.path.join("uploads", file.filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(filepath)

    # Extract document text using PyMuPDF
    document_text = extract_text(filepath)

    if document_text.startswith("Error"):
        return f"Summary: {document_text}"

    try:
        # Handle long docs in chunks (1000 tokens max per call)
        if len(document_text) > 1000:
            chunks = [document_text[i:i+1000] for i in range(0, len(document_text), 1000)]
            summaries = [
                summarizer(chunk, max_length=120, min_length=30, do_sample=False)[0]['summary_text']
                for chunk in chunks
            ]
            full_summary = " ".join(summaries)
        else:
            full_summary = summarizer(document_text, max_length=120, min_length=30, do_sample=False)[0]['summary_text']

        # Trim to ≤ 150 words
        trimmed_summary = " ".join(full_summary.split()[:150])

        return render_template('summary.html', summary=trimmed_summary)

    except Exception as e:
        return f"Error during summarization: {str(e)}"

@app.route('/ask', methods=['POST'])
def ask_anything():
    from qa_module import answer_question

    question = request.form['question']
    answer, justification = answer_question(question, document_text)

    return render_template('answer.html', question=question, answer=answer, justification=justification)

@app.route('/challenge')
def challenge_me():
    from challenge_me import generate_questions

    questions = generate_questions(document_text)
    return render_template('challenge.html', questions=questions)

if __name__ == '__main__':
    app.run(debug=True)


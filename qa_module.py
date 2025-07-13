# qa_module.py

from transformers import pipeline
import re

# Load the QA pipeline once
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

def split_into_sentences(text):
    # Simple sentence splitter (could improve later with nltk/spacy)
    return re.split(r'(?<=[.!?]) +', text)

def answer_question(question, context):
    try:
        result = qa_pipeline({
            'context': context,
            'question': question
        })

        answer = result['answer']

        # Find justification sentence containing the answer
        for sentence in split_into_sentences(context):
            if answer.lower() in sentence.lower():
                justification = sentence.strip()
                break
        else:
            justification = "No specific justification found."

        return answer, justification

    except Exception as e:
        return "Error answering question.", str(e)

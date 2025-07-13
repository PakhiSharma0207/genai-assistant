# challenge_me.py

import random
import re

def generate_questions(text):
    # Simple logic-based question generator (could be replaced by GPT later)
    sentences = re.split(r'(?<=[.!?]) +', text.strip())

    questions = []
    for s in sentences:
        if "is" in s or "are" in s:
            # Convert statement into a fill-in-the-blank style question
            question = s.replace(" is ", " _____ ", 1)
            questions.append(question.strip())

    if len(questions) < 3:
        # Fallback generic questions
        questions += [
            "What is the main focus of the document?",
            "Summarize the document in your own words.",
            "What is discussed in the introduction?"
        ]

    return random.sample(questions, 3)

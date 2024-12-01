
from flask import Flask, request, render_template
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from PyPDF2 import PdfReader
from docx import Document
from sklearn.feature_extraction.text import CountVectorizer

nltk.download('punkt',quiet=True)

app = Flask(__name__)

def predict_personality(text):
    # Define keywords for each personality trait
    traits = {
        'extroversion': ['social', 'outgoing', 'talkative', 'energetic', 'friendly'],
        'conscientiousness': ['organized', 'responsible', 'dependable', 'efficient'],
        'openness': ['creative', 'curious', 'imaginative', 'adventurous'],
        'agreeableness': ['cooperative', 'compassionate', 'friendly', 'kind'],
        'neuroticism': ['anxious', 'moody', 'sensitive', 'nervous']
    }

    personality_scores = {trait: 0 for trait in traits.keys()}

    # Tokenize the text
    words = word_tokenize(text.lower())

    # Count occurrences of keywords
    for word in words:
        for trait, keywords in traits.items():
            if word in keywords:
                personality_scores[trait] += 1

    return personality_scores
# Function to extract text from PDF
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ''
    for page in reader.pages:
        text += page.extract_text() + '\n'
    return text

# Function to extract text from DOCX
def extract_text_from_docx(file):
    doc = Document(file)
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        file = request.files['resume']
        if file:
            if file.filename.endswith('.pdf'):
                text = extract_text_from_pdf(file)
            elif file.filename.endswith('.docx'):
                text = extract_text_from_docx(file)
            else:
                text = file.read().decode('utf-8', errors='ignore')  # Fallback for plain text files

            personality_scores = predict_personality(text)
            return render_template('index.html', scores=personality_scores)

    return render_template('index.html', scores=None)

if __name__ == '__main__':
    app.run(debug=True)
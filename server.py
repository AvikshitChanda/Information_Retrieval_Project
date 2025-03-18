import streamlit as st
import os
import re
import unicodedata
import dateparser
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import contractions
from unidecode import unidecode
from metaphone import doublemetaphone

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('omw-1.4')

def normalize_punctuation(text):
    text = re.sub(r'\b(\w(?:\.\w)+)\b', lambda x: x.group(1).replace('.', ''), text)
    return text

def normalize_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))

def normalize_stopwords(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    return ' '.join([word for word in words if word.lower() not in stop_words])

def normalize_lemmatization(text):
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(text)
    return ' '.join([lemmatizer.lemmatize(word) for word in words])

def normalize_dates(text):
    words = text.split()
    for i, word in enumerate(words):
        try:
            date_obj = dateparser.parse(word, languages=['en', 'ja'])
            if date_obj:
                words[i] = date_obj.strftime("%m/%d/%Y")
        except:
            continue
    return " ".join(words)

def normalize_case(text):
    return text.lower()

def normalize_language_variations(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')

def normalize_whitespace(text):
    return re.sub(r'\s+', ' ', text).strip()


def normalize_contractions(text):
    words = text.split()
    expanded_words = [contractions.fix(word) for word in words]
    return ' '.join(expanded_words)


def normalize_all(text):
    text = normalize_punctuation(text)
    text = normalize_stopwords(text)
    text = normalize_lemmatization(text)
    text = normalize_accents(text)
    text = normalize_dates(text)
    text = normalize_case(text)
    text = normalize_language_variations(text)
    text = normalize_contractions(text)
    text = normalize_whitespace(text)
    return text

def soundex(word):
    if not word:
        return ""
    word = word.upper()
    mapping = {
        "B": "1", "F": "1", "P": "1", "V": "1",
        "C": "2", "G": "2", "J": "2", "K": "2", "Q": "2", "S": "2", "X": "2", "Z": "2",
        "D": "3", "T": "3",
        "L": "4",
        "M": "5", "N": "5",
        "R": "6"
    }
    first_letter = word[0]
    encoded = first_letter
    for char in word[1:]:
        if char in mapping:
            digit = mapping[char]
            if digit != encoded[-1]:
                encoded += digit
    return (encoded + "000")[:4]

def normalize_with_soundex(text):
    words = text.split()
    return ' '.join([soundex(word) for word in words])

def normalize_with_metaphone(text):
    words = text.split()
    return ' '.join([doublemetaphone(word)[0] for word in words])

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    normalized_text = normalize_all(text)
    soundex_text = normalize_with_soundex(text)
    metaphone_text = normalize_with_metaphone(text)
    return normalized_text, soundex_text, metaphone_text

def main():
    st.title("Text Normalization App")
    uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])
    if uploaded_file is not None:
        file_path = os.path.join("temp.txt")
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())
        normalized_text, soundex_text, metaphone_text = process_file(file_path)
        
        st.subheader("Normalized Text")
        st.text_area("", normalized_text, height=200)
        
        st.subheader("Soundex Normalized Text")
        st.text_area("", soundex_text, height=200)
        
        st.subheader("Metaphone Normalized Text")
        st.text_area("", metaphone_text, height=200)
        
        output_file_path = "normalized_output.txt"
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write(normalized_text)
        
        st.download_button(
            label="Download Normalized Text",
            data=normalized_text,
            file_name="normalized_output.txt",
            mime="text/plain"
        )
        
        soundex_file_path = "soundex_output.txt"
        with open(soundex_file_path, "w", encoding="utf-8") as f:
            f.write(soundex_text)
        
        st.download_button(
            label="Download Soundex Text",
            data=soundex_text,
            file_name="soundex_output.txt",
            mime="text/plain"
        )
        
        metaphone_file_path = "metaphone_output.txt"
        with open(metaphone_file_path, "w", encoding="utf-8") as f: 
            f.write(metaphone_text)
        
        st.download_button(
            label="Download Metaphone Text",
            data=metaphone_text,
            file_name="metaphone_output.txt",
            mime="text/plain"
        )

if __name__ == "__main__":
    main()

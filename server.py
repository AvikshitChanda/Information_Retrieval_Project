import streamlit as st
import os
import re
import unicodedata
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import contractions
from unidecode import unidecode
from metaphone import doublemetaphone
import string

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('omw-1.4')

def normalize_punctuation(text):
    text = text.translate(str.maketrans("", "", string.punctuation.replace("-", "").replace(".", "")))
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

def normalize_contractions(text):
    words = text.split()
    expanded_words = [contractions.fix(word) for word in words]
    return ' '.join(expanded_words)

def normalize_language_variations(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')

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

def normalize_with_metaphone(text):
    words = text.split()
    return ' '.join([doublemetaphone(word)[0] for word in words])

def normalize_text(text):
    text = normalize_punctuation(text)
    text = normalize_accents(text)
    text = normalize_contractions(text)
    text = normalize_language_variations(text)
    text = normalize_stopwords(text)
    text = normalize_lemmatization(text)
    return text

def main():
    st.title("Text Normalization ")
    
    methods = {
        "Normalize Punctuation": normalize_punctuation,
        "Normalize Accents": normalize_accents,
        "Normalize Stopwords": normalize_stopwords,
        "Normalize Lemmatization": normalize_lemmatization,
        "Normalize Contractions": normalize_contractions,
        "Normalize Language Variations": normalize_language_variations,
    }
    
    for method_name, method_func in methods.items():
        st.subheader(method_name)
        user_input = st.text_area(f"Enter text for {method_name}", "", key=method_name)
        if st.button(f"{method_name}", key=f"btn_{method_name}"):
            st.markdown(f"### Output:\n\n**{method_func(user_input)}**")


    
    
    # Soundex Normalization
    st.header("Soundex Normalization")
    soundex_input = st.text_area("Enter text for Soundex", "", key="soundex")
    if st.button("Generate Soundex", key="btn_soundex"):
        words = soundex_input.split()
        soundex_output = ' '.join([soundex(word) for word in words])
        st.write("Output:", soundex_output)

      # Apply All Normalization Methods
    st.header("Full Text Normalization")
    uploaded_file = st.file_uploader("Upload a .txt file for Complete Regex Normalisation", type=["txt"], key="normalised_file")
    if uploaded_file is not None and st.button("Generate Normalised File", key="btn_regex"):
        file_path = "regex_normalised_output.txt"
        text = uploaded_file.read().decode("utf-8")
        regex_text = normalize_text(text)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(regex_text)
        # Display a preview (first 500 characters or entire text if small)
        st.subheader("Preview of Normalised Text:")
        st.text_area("Normalized Output", regex_text[:500] + ("..." if len(regex_text) > 500 else ""), height=200)

        st.download_button("Download Normalised Text", data=regex_text, file_name=file_path, mime="text/plain")
    
    # Metaphone Normalization with File Upload
    st.header("Metaphone Normalization")
    uploaded_file = st.file_uploader("Upload a .txt file for Metaphone", type=["txt"], key="metaphone_file")
    if uploaded_file is not None and st.button("Generate Metaphone File", key="btn_metaphone"):
        file_path = "metaphone_output.txt"
        text = uploaded_file.read().decode("utf-8")
        metaphone_text = normalize_with_metaphone(text)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(metaphone_text)
        
        # Display a preview (first 500 characters or entire text if small)
        st.subheader("Preview of Normalised Text:")
        st.text_area("Normalized Output", metaphone_text[:500] + ("..." if len(metaphone_text) > 500 else ""), height=200)

        st.download_button("Download Metaphone Text", data=metaphone_text, file_name=file_path, mime="text/plain")
    
  

if __name__ == "__main__":
    main()
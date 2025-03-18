

!pip install --upgrade nltk

import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('stopwords')
nltk.download('punkt_tab') # Download the punkt_tab data

!pip install contractions

import re
import unicodedata
from dateutil import parser
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import inflect
from contractions import fix
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

"""**1. Normalize Punctuation Variations**"""

def normalize_punctuation(text):
    # Remove dots within words but preserve decimal points and email addresses
    text = re.sub(r'\b(\w(?:\.\w)+)\b', lambda x: x.group(1).replace('.', ''), text)

    return text

# Example Test Cases
input_text = input("Enter a text: ")
print("Normalized Text:", normalize_punctuation(input_text))

"""**2. Normalize Hyphenated Words**"""

def normalize_hyphenation(text):
    return re.sub(r'(\w+)-(\w+)', r'\1\2', text)

input_text = input("Enter a text: ")
print("Normalized Text:", normalize_hyphenation(input_text))

## e.g., anti-discriminatory → antidiscriminatory

"""**3. Normalize Accents & Special Characters**"""

def normalize_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))

input_text = input("Enter a text: ")
print("Normalized Text:", normalize_accents(input_text))

## e.g., résumé → resume

"""**4. Removing Stopwords**"""

import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def normalize_stopwords(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    return ' '.join([word for word in words if word.lower() not in stop_words])

input_text = input("Enter text: ")
print("Stopword-Normalized Text:", normalize_stopwords(input_text))
#This is a good day to go outside.

"""**5. Lemmatization**"""

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

def normalize_lemmatization(text):
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(text)
    return ' '.join([lemmatizer.lemmatize(word) for word in words])

input_text = input("Enter text: ")
print("Lemmatized Text:", normalize_lemmatization(input_text))
#running dogs are happier than sleeping ones

"""**6. Normalize Different Date Formats**"""

def normalize_dates(text):
    try:
        return parser.parse(text, fuzzy=True).strftime("%m/%d/%Y")
    except:
        return text  # Return original if no valid date is found

input_text = input("Enter a text: ")
print("Normalized Text:", normalize_dates(input_text))


## e.g., 7月30日 → 7/30

"""**7. Normalize Proper Nouns & Case Variations**"""

def normalize_case(text):
    return text.lower()

input_text = input("Enter a text: ")
print("Normalized Text:", normalize_case(input_text))


## e.g., General Motors → general motors

"""**8. Normalize Language Variations**"""

def normalize_language_variations(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')

input_text = input("Enter a text: ")
print("Normalized Text:", normalize_language_variations(input_text))


## e.g., Tübingen → Tubingen

"""**9. Normalize Extra Whitespace**"""

def normalize_whitespace(text):
    return re.sub(r'\s+', ' ', text).strip()

input_text = input("Enter a text: ")
print("Normalized Text:", normalize_whitespace(input_text))


## (e.g., Hello     World → Hello World

"""**10. Normalize Contractions**"""

def normalize_contractions(text):
    return fix(text)

input_text = input("Enter a text: ")
print("Normalized Text:", normalize_contractions(input_text))

## e.g., can't → cannot, it's → it is

"""**Normalize Full Sentence**"""

def normalize_all(text):
    text = normalize_punctuation(text)
    text = normalize_hyphenation(text)
    text = normalize_stopwords(text)
    text = normalize_lemmatization(text)
    text = normalize_accents(text)
    text = normalize_dates(text)
    text = normalize_case(text)
    text = normalize_language_variations(text)
    text = normalize_contractions(text)
    text = normalize_whitespace(text)

    return text

input_text = input("Enter a text: ")
print("\n\n")  # Adds a clean double line break for spacing
print("Fully Normalized Text:", normalize_all(input_text))



## Sample text

## "U.S.A and USA are the same. The anti-discriminatory policies were updated. His résumé was impressive, just like Général Motors'. Tübingen and Tubingen are the same place. He was born on 7月30日, while another record states 30-07-2023. SAIL and sail refer to different things, but co-operate and cooperate mean the same."

!pip install unidecode

"""**Normalizing using Soundex**"""

import re
from unidecode import unidecode

# Soundex Implementation
def soundex(word):
    if not word:
        return ""
    word = word.upper()
    soundex_mapping = {
        "B": "1", "F": "1", "P": "1", "V": "1",
        "C": "2", "G": "2", "J": "2", "K": "2", "Q": "2", "S": "2", "X": "2", "Z": "2",
        "D": "3", "T": "3",
        "L": "4",
        "M": "5", "N": "5",
        "R": "6"
    }

    first_letter = word[0]  # Keep the first letter
    encoded = first_letter

    # Convert remaining letters
    for char in word[1:]:
        if char in soundex_mapping:
            digit = soundex_mapping[char]
            if digit != encoded[-1]:  # Avoid consecutive duplicates
                encoded += digit

    encoded = encoded.replace("0", "")  # Remove zeros
    encoded = (encoded + "000")[:4]  # Ensure length is 4
    return encoded

# Test sentence
sentence = "The résumé of Dr. J.K.L. is well-known. He visited U.S.A. on 12月25日, and researched anti-discriminatory policies for Windows-based systems."

# Apply Soundex to Each Word
soundex_codes = {word: soundex(word) for word in sentence.split()}

# Print results
print("\n🔹 Original Sentence:")
print(sentence)

print("\n🔹 Soundex Codes:")
for word, code in soundex_codes.items():
    print(f"{word}: {code}")

def normalize_with_soundex(text):
    text = normalize_all(text)  # Apply all normalizations
    codes = [soundex(word) for word in sentence.split()]  # Convert each word to Soundex
    return ' '.join(codes)

# **Example Run**
input_text = input("Enter a text: ")
print("\n\n")
print("Fully Normalized Text:", normalize_all(input_text))
print("Soundex Normalized Text:", normalize_with_soundex(input_text))

## Sample text

## "U.S.A and USA are the same. The anti-discriminatory policies were updated. His résumé was impressive, just like Général Motors'. Tübingen and Tubingen are the same place. He was born on 7月30日, while another record states 30-07-2023. SAIL and sail refer to different things, but co-operate and cooperate mean the same."

"""Normalisation using metaphone"""

!pip install metaphone

from metaphone import doublemetaphone

def normalize_with_metaphone(text):
    """
    Normalizes text by converting each word into its Metaphone encoding.

    Args:
    - text (str): Input sentence.

    Returns:
    - str: Sentence with words replaced by their Metaphone encoding.
    """
    text = normalize_all(text)  # Apply all normalizations (assumed to be defined)
    words = text.split()
    codes = [doublemetaphone(word)[0] for word in words]  # Convert words to Metaphone primary encoding
    return ' '.join(codes)

# **Example Run**
input_text = input("Enter a text: ")
print("\n\n")
print("Fully Normalized Text:", normalize_all(input_text))
print("Metaphone Normalized Text:", normalize_with_metaphone(input_text))

"""Normalising a file"""

import os
def process_file(input_file, norm_file):
    """
    Reads a file, applies text normalization & Metaphone normalization,
    then saves both versions to separate files.
    """
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()

    normalized_text = normalize_all(text)
    metaphone_text = normalize_with_metaphone(text)

    phonetic_file = norm_file.replace(".txt", "_metaphone.txt")  # Auto-generate Metaphone file

    with open(norm_file, "w", encoding="utf-8") as f:
        f.write(normalized_text)

    with open(phonetic_file, "w", encoding="utf-8") as f:
        f.write(metaphone_text)

    return normalized_text, metaphone_text, phonetic_file


# **Manually Enter File Path Instead of Using Tkinter**
input_filename = input("Enter the full path of the input text file: ")

# **Check if File Exists**
if not os.path.exists(input_filename):
    print("❌ Error: File not found. Please check the path and try again.")
else:
    output_filename = input("Enter the output filename for normalized text (without extension): ") + ".txt"

    # Process the file
    normalized_text, metaphone_text, metaphone_file = process_file(input_filename, output_filename)

    # **Preview of Results**
    print("\n--- Normalized Text Preview ---\n")
    print(normalized_text[:500])  # Show first 500 characters

    print("\n--- Metaphone Normalized Text Preview ---\n")
    print(metaphone_text[:500])  # Show first 500 characters

    print(f"\n✅ Normalized text saved in: {output_filename}")
    print(f"✅ Metaphone normalized text saved in: {metaphone_file}")


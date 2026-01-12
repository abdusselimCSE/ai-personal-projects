import re
import nltk
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)


def summarize(transcript_text, top_n=5):

    # --------------------------
    # 1 Clean text
    # --------------------------
    def clean_text(text):
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"[^a-zA-Z0-9.?!, ]", "", text)
        return text.strip()

    cleaned_text = clean_text(transcript_text)

    # --------------------------
    # 2 Sentence Tokenization
    # --------------------------
    sentences = []

    lines = transcript_text.split("\n")

    for line in lines:
        line = line.strip()

        if len(line) > 0:
            sentences.append(line)

    if len(sentences) == 1:
        sentences = sent_tokenize(cleaned_text)

    if len(sentences) == 0:
        sentences = sent_tokenize(cleaned_text)

    # --------------------------
    # 3 Word Tokenization + Stopwords Removal
    # --------------------------
    stop_words = set(stopwords.words("english"))

    words = word_tokenize(cleaned_text.lower())
    filtered_words = []

    for word in words:
        if word not in stop_words:
            filtered_words.append(word)

    # --------------------------
    # 4 Word Frequency Count
    # --------------------------
    word_freq = Counter(filtered_words)

    # --------------------------
    # 5 Sentence Scoring
    # --------------------------
    sentence_scores = {}

    for sentence in sentences:
        sentence_words = word_tokenize(sentence.lower())
        score = 0

        for item in sentence_words:
            if item in word_freq:
                score = score + word_freq[item]

        sentence_scores[sentence] = score

    # --------------------------
    # 6 Select Top N Sentences
    # --------------------------
    scored_list = list(sentence_scores.items())
    scored_list.sort(key=lambda x: x[1], reverse=True)

    top_sentences = []
    count = 0

    for item in scored_list:
        if count < top_n:
            top_sentences.append(item[0])
            count = count + 1

    # --------------------------
    # 7 Keep Original Order
    # --------------------------
    ordered_sentences = []

    for s in sentences:
        if s in top_sentences:
            ordered_sentences.append(s)

    # --------------------------
    # 8 Build Summary
    # --------------------------
    summary = ""

    for s in ordered_sentences:
        s = s.strip()
        if len(s) > 0:
            s = s[0].upper() + s[1:]
        if len(s) > 0:
            summary = summary + s + " "

    return summary.strip()

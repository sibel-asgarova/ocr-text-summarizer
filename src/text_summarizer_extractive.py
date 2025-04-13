import spacy
import heapq
import math

nlp = spacy.load("en_core_web_sm")

def summarize_text_spacy(text, ratio=0.25):
    doc = nlp(text)

    sentences = [sent.text for sent in doc.sents]
    total_sentences = len(sentences)


    max_sentences = max(1, math.ceil(total_sentences * ratio))

    word_freq = {}
    for token in doc:
        if not token.is_stop and not token.is_punct and token.is_alpha:
            lemma = token.lemma_.lower()
            word_freq[lemma] = word_freq.get(lemma, 0) + 1

    max_freq = max(word_freq.values()) if word_freq else 1
    for word in word_freq:
        word_freq[word] /= max_freq

    # Sentence scores
    sentence_scores = {}
    for sent in doc.sents:
        for token in sent:
            lemma = token.lemma_.lower()
            if lemma in word_freq:
                sentence_scores[sent.text] = sentence_scores.get(sent.text, 0) + word_freq[lemma]

    # Get top-ranked sentences
    summary_sentences = heapq.nlargest(max_sentences, sentence_scores, key=sentence_scores.get)

    summary = ' '.join(summary_sentences)
    return summary

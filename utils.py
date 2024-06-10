import matplotlib
matplotlib.use('Agg')

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from collections import Counter
import pandas as pd
import io
import base64
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

STOP_WORDS = set(stopwords.words('english')).union({'the', 'and', 'to', 'based', 'requires', 'ability', 'work', 'knowledge', 'including', 'technologies', 'using', 'new', 'techniques', 'tools', 'technologies', 'years', 'related', 'field', 'working', 'environment', 'degree', 'equivalent', 'preferred', 'ca', 'us'})

def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=STOP_WORDS).generate(text)
    img = io.BytesIO()
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

def generate_wordclouds(resume_text, job_description):
    resume_wc = generate_wordcloud(resume_text)
    job_wc = generate_wordcloud(job_description)
    return resume_wc, job_wc

def get_word_frequencies(text1, text2):
    def word_freq(text):
        words = nltk.word_tokenize(text.lower())
        words = [word for word in words if word.isalnum() and word not in STOP_WORDS and not word.isdigit()]
        return Counter(words)

    resume_freq = word_freq(text1)
    job_freq = word_freq(text2)


    resume_top_10 = (pd.DataFrame(resume_freq.items(), columns=['Word', 'Frequency'])
                     .sort_values(by='Frequency', ascending=False)[:10].to_dict(orient='records'))
    job_top_10 = (pd.DataFrame(job_freq.items(), columns=['Word', 'Frequency'])
                  .sort_values(by='Frequency', ascending=False)[:10].to_dict(orient='records'))

    return resume_top_10, job_top_10

def analyze_keywords(resume_text, job_description):
    def word_set(text):
        words = nltk.word_tokenize(text.lower())
        words = {word for word in words if word.isalnum() and word not in STOP_WORDS and not word.isdigit()}
        return words

    resume_words = word_set(resume_text)
    job_words = word_set(job_description)

    matching_keywords = resume_words & job_words
    missing_keywords = job_words - resume_words

    match_percentage = (len(matching_keywords) / len(job_words)) * 100 if job_words else 0
    match_percentage = f"{match_percentage:.1f}"

    missing_keywords_freq = {word: job_description.lower().count(word) for word in missing_keywords}

    missing_keywords_sorted = sorted(missing_keywords, key=lambda word: missing_keywords_freq[word], reverse=True)

    return matching_keywords, missing_keywords_sorted, match_percentage

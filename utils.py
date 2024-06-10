import matplotlib
matplotlib.use('Agg')  

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from collections import Counter
import pandas as pd
import io
import base64

nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords

STOP_WORDS = set(stopwords.words('english')).union({'the', 'and', 'to'})

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
        words = [word for word in words if word.isalnum() and word not in STOP_WORDS]
        return Counter(words)

    resume_freq = word_freq(text1)
    job_freq = word_freq(text2)
    return (pd.DataFrame(resume_freq.items(), columns=['Word', 'Frequency'])
            .sort_values(by='Frequency', ascending=False).to_dict(orient='records'),
            pd.DataFrame(job_freq.items(), columns=['Word', 'Frequency'])
            .sort_values(by='Frequency', ascending=False).to_dict(orient='records'))

from flask import Flask, render_template, request
from forms import ResumeForm
from utils import generate_wordclouds, get_word_frequencies, analyze_keywords

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ResumeForm()
    if form.validate_on_submit():
        resume_text = form.resume.data
        job_description = form.job_description.data
        resume_wc, job_wc = generate_wordclouds(resume_text, job_description)
        resume_freq, job_freq = get_word_frequencies(resume_text, job_description)
        matching_keywords, missing_keywords, match_percentage = analyze_keywords(resume_text, job_description)
        return render_template('result.html', 
                               resume_wc=resume_wc, job_wc=job_wc, 
                               resume_freq=resume_freq, job_freq=job_freq,
                               matching_keywords=matching_keywords, missing_keywords=missing_keywords,     match_percentage=match_percentage)
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)

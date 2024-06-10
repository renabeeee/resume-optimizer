from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

class ResumeForm(FlaskForm):
    resume = TextAreaField('Resume', validators=[DataRequired()])
    job_description = TextAreaField('Job Description', validators=[DataRequired()])
    submit = SubmitField('Generate')

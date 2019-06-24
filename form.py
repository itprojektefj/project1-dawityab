from wtforms import Form, BooleanField, StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf import FlaskForm


class RegistrationForm(FlaskForm):

    user_email = StringField('Email Address', [validators.DataRequired(), Length(min=6, max=35)])
    username = StringField('Username', [validators.DataRequired(), Length(min=4, max=25)])
    password = PasswordField('New Password', [validators.DataRequired(), Length(min=4, max=25)])
    confirm_password = PasswordField('Confirm password', [validators.DataRequired(), EqualTo('password' )])


class LoginForm(FlaskForm):
    user_email = StringField('Email', validators=[DataRequired(), Email('email')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit', validators=[DataRequired()])


class SearchForm(FlaskForm):
     title = StringField('title', validators=[DataRequired(), Length(max=50)])
     author = StringField('author', validators=[DataRequired, Length(max=50)])
     isbn = StringField('isbn', validators=[DataRequired, Length(max=30)])
     year = StringField('year', validators=[DataRequired])
class Comment(FlaskForm):
    text = StringField('text', validators=[DataRequired(), Length(max=140)])
    authoruser = StringField('authoruser', validators=[DataRequired(), Length(max=50)])
    isbn = StringField('isbn', validators=[DataRequired, Length(max=30)])
    rating = StringField('rating', validators=[DataRequired, Length(max=5)])
    date = StringField('date', validators=[DataRequired])






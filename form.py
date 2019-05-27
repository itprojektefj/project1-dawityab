from wtforms import Form, StringField, PasswordField, SubmitField, validators, ValidationError

from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf import FlaskForm


class RegistrationForm(FlaskForm):

    user_email = StringField('Email Address', validators=[DataRequired(),Length(min=6, max=35)])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=4,max=25)])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password'), Length(min=4,max=25)])


class LoginForm(FlaskForm):
    user_email = StringField('Email', validators=[DataRequired(), Length(min=6,max=35), Email('email')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4,max=25)])
    submit = SubmitField('Submit', validators=[DataRequired()])





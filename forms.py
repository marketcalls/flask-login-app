from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import re
from models import User

class PasswordValidator:
    def __init__(self, message=None):
        if not message:
            message = 'Password must be at least 12 characters long, contain uppercase and lowercase letters, at least one number, and at least one special character.'
        self.message = message

    def __call__(self, form, field):
        password = field.data
        
        # Check password length
        if len(password) < 12:
            raise ValidationError('Password must be at least 12 characters long.')
        
        # Check for uppercase letters
        if not any(c.isupper() for c in password):
            raise ValidationError('Password must contain at least one uppercase letter.')
        
        # Check for lowercase letters
        if not any(c.islower() for c in password):
            raise ValidationError('Password must contain at least one lowercase letter.')
        
        # Check for numbers
        if not any(c.isdigit() for c in password):
            raise ValidationError('Password must contain at least one number.')
        
        # Check for special characters
        if not re.search(r'[!@#$%^&*()\-_=+{};:,<.>]', password):
            raise ValidationError('Password must contain at least one special character.')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), PasswordValidator()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('New Password', validators=[PasswordValidator()])
    confirm_password = PasswordField('Confirm New Password', validators=[EqualTo('password')])
    submit = SubmitField('Update Profile')

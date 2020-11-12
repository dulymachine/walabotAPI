from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from walabotapi.models import User


class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired(), Length(min=5, max=25)])
  email = StringField('Email', validators=[DataRequired(), Email() ])
  password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=50)])
  confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8, max=50), EqualTo('password')])
  submit = SubmitField('Create Login')

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError('That username is taken. Please choose another username.')
  
  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError('That email is taken. Please choose another email.')



class LoginForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email() ])
  password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=50)])
  remember = BooleanField('Remember Me')  
  submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired(), Length(min=5, max=25)])
  email = StringField('Email', validators=[DataRequired(), Email() ])
  submit = SubmitField('Update Login')

  def validate_username(self, username):
    if username.data != current_user.username:
      user = User.query.filter_by(username=username.data).first()
      if user:
        raise ValidationError('That username is taken. Please choose another username.')
  
  def validate_email(self, email):
    if email.data != current_user.email:
      user = User.query.filter_by(email=email.data).first()
      if user:
        raise ValidationError('That email is taken. Please choose another email.')


class RequestResetForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email() ])
  submit = SubmitField('Request Password Reset')

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user is None:
      raise ValidationError('There is no account associated with that email.')


class ResetPasswordForm(FlaskForm):
  password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=50)])
  confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8, max=50), EqualTo('password')])

  submit = SubmitField('Reset Password')

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import Role, User, Classe, Course
from app import db

class MyForm(FlaskForm):
  autocplt = StringField('Email', validators=[DataRequired()],render_kw={"placeholder": "email"})
  submit = SubmitField('Add User')
	#autocplt = StringField('Email', validators=[DataRequired(),Length(max=40)],render_kw={"placeholder": "email"})

class LoginForm(FlaskForm):
  username = StringField('Usarname', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember_me = BooleanField('Remember Me')
  submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField(
    'Repeat Password', 
    validators=[DataRequired(), 
    EqualTo('password')])
  submit = SubmitField('Register')
  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user is not None:
      raise ValidationError('Please use a different username.')
  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user is not None:
      raise ValidationError('Please use a different email address.')

class RegistrationFormClass(FlaskForm):
  classname = StringField('Classname', validators=[DataRequired()])
  submit = SubmitField('Create Class')
  def validate_classname(self, classname):
    find_class = Classe.query.filter_by(name=classname.data).first()
    if find_class is not None:
      raise ValidationError('Please use a different classname.')






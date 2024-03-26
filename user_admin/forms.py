from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,IntegerField,DateField
from wtforms.validators import Length,EqualTo,Email,DataRequired, ValidationError
from user_admin.models import Employee

class RegisterForm(FlaskForm):
    
    first_name = StringField(label='First Name : ', validators = [Length(min=2,max=30),DataRequired()])
    last_name = StringField(label='Last Name : ', validators = [Length(min=2,max=30),DataRequired()])
    email_address = StringField(label='Email Address : ', validators = [Email(),DataRequired()])
    address = StringField(label='Address : ', validators = [Length(min=10,max=500),DataRequired()])
    DOB = DateField(label='DOB : ',validators = [DataRequired()])
    password = PasswordField(label='Password : ', validators = [Length(min=6),DataRequired()])
    password_confirm = PasswordField(label='Confirm Password : ', validators = [EqualTo('password'),DataRequired()])
    phone_number = IntegerField(label='Phone Number : ',validators=[DataRequired()])
    submit = SubmitField(label='Create Account') 
    
    
class LoginForm(FlaskForm):
    email_address = StringField(label='Email Address : ', validators = [Email(),DataRequired()])
    password = PasswordField(label='Password : ', validators = [DataRequired()])
    submit = SubmitField(label='Sign in')
    
class AdminForm(FlaskForm):
    email_address = StringField(label="Email Address :",validators=[Email(),DataRequired()])
    password = PasswordField(label='Password : ', validators = [DataRequired()])
    submit = SubmitField(label='Login')
    
class EditForm(FlaskForm):
    
    first_name = StringField(label='First Name : ', validators = [Length(min=2,max=30),DataRequired()])
    last_name = StringField(label='Last Name : ', validators = [Length(min=2,max=30),DataRequired()])
    email_address = StringField(label='Email Address : ', validators = [Email(),DataRequired()])
    address = StringField(label='Address : ', validators = [Length(min=10,max=500),DataRequired()])
    DOB = DateField(label='DOB : ',validators = [DataRequired()])
    phone_number = IntegerField(label='Phone Number : ',validators=[DataRequired()])
    submit = SubmitField(label='Update Details') 
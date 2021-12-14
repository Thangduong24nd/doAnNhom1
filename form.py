from flask_wtf import FlaskForm
import flask_wtf
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField,IntegerField,SelectField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo
from app.models import  Users
class signUpForm(FlaskForm):
    user = StringField('User', validators=[DataRequired(), Length(min=5, message=('Your user is too short.'))])
    password = PasswordField('Password',  validators=[DataRequired(), Length(min=8, message=('Your password is too short.'))])
    rePassword = PasswordField('reType Password',  validators=[DataRequired(), EqualTo('password', message='Passwords must match')])

    submit = SubmitField('Sign Up')
    def validate_passengerId(self, passengerId):
        user = Users.query.filter_by(user=Users.data).first()
        if user is not None:
            raise ValidationError('username has been already used! Please use a different username.')
class loginForm(FlaskForm):
    user = StringField('User', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')
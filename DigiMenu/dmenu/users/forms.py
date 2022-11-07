from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,IntegerField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
import email_validator
from dmenu.models import User
from flask_login import current_user

#Register
class RegistrationForm(FlaskForm):
    rest_name = StringField("Restaurant Name",
                            validators=[DataRequired(),Length(min=3,max=50)])

    rest_address=StringField("Restaurant Address",validators=[DataRequired(),Length(min=5,max=60)])

    email=StringField("Email",validators=[DataRequired(),Email()])
    table_count=IntegerField('Number of Tables',validators=[DataRequired()])
    password=PasswordField("Password",validators=[DataRequired()])
    confirm_password=PasswordField("Confirm Password",
                                   validators=[DataRequired(),EqualTo("password")])
    terms_cond = BooleanField('I agree with Terms and Conditions', validators=[DataRequired()])
    submit=SubmitField("Register")
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('There is already an account with that email, please try another one.')

#login
class LoginForm(FlaskForm):
    email=StringField("Email",validators=[DataRequired(),Email()])
    password=PasswordField("Password",validators=[DataRequired()])
    remember=BooleanField("Remember Me")
    submit=SubmitField("Sign in")


#update account
class UpdateAccountForm(FlaskForm):
    rest_address=StringField('Restaurant Address', validators=[Length(min=10,max=50)])
    email=StringField('Email',validators=[Email()])
    submit=SubmitField('Update')

    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


#request reset from
class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit=SubmitField('Request Password Reset')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


#reset password form
class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password",
                                     validators=[DataRequired(), EqualTo("password")])
    submit=SubmitField('Reset Password')
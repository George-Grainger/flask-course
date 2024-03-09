from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import StringField, IntegerField, TextAreaField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")


class SignUpForm(FlaskForm):
    full_name = StringField("Full Name", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            InputRequired(),
            EqualTo("password", message="Passwords must match"),
        ],
    )
    submit = SubmitField("Login")


class PetForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    age = StringField("Age", validators=[InputRequired()])
    bio = TextAreaField("Bio", validators=[InputRequired()])
    submit = SubmitField("Edit")

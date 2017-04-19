from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Benutzer', validators=[DataRequired()])
    password = StringField('Passwort', validators=[DataRequired()])

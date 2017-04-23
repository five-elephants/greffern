from flask_wtf import FlaskForm
from wtforms import StringField,SelectField,FloatField,SubmitField
from wtforms.validators import DataRequired,Email


class LoginForm(FlaskForm):
    username = StringField('Benutzer', validators=[DataRequired()])
    password = StringField('Passwort', validators=[DataRequired()])


class CreateAlertForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    sensor = SelectField('Sensor', validators=[DataRequired()], coerce=int)
    notify_email = StringField('E-Mail Adresse', validators=[DataRequired(), Email()])
    trigger_above = FloatField('Obere Schranke')
    trigger_below = FloatField('Untere Schranke')
    submit = SubmitField('Erstellen')

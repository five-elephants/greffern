from flask_wtf import FlaskForm
from wtforms import StringField,SelectField,FloatField,SubmitField,HiddenField,PasswordField
from wtforms.validators import DataRequired,Email,Optional


class LoginForm(FlaskForm):
    username = StringField('Benutzer', validators=[DataRequired()])
    password = PasswordField('Passwort', validators=[DataRequired()])


class CreateAlertForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    sensor = SelectField('Sensor', validators=[DataRequired()], coerce=int)
    notify_email = StringField('E-Mail Adresse', validators=[DataRequired(), Email()])
    trigger_above = FloatField('Obere Schranke', validators=[Optional()])
    trigger_below = FloatField('Untere Schranke', validators=[Optional()])
    submit = SubmitField('Erstellen')

class UpdateSensorForm(FlaskForm):
    sensor_id = HiddenField('id', validators=[DataRequired()])
    name = StringField('Name')
    location = StringField('Ort')
    submit = SubmitField('Ok')


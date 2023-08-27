from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo
from app.models import User
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


# User registration 

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    vorname = StringField('Vorname', validators=[DataRequired()])
    nachname = StringField('Nachname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class PfadikindForm(FlaskForm):
    pfadiname = StringField('Pfadiname', validators=[DataRequired()])
    vegetarisch = BooleanField('Vegetarisch')
    vorname = StringField('Vorname', validators=[DataRequired()])
    nachname = StringField('Nachname', validators=[DataRequired()])
    geburtsdatum = DateField('Geburtsdatum', validators=[DataRequired()], format='%Y-%m-%d')
    adresse = StringField('Adresse', validators=[DataRequired()])
    telefonprivat = StringField('Telefon privat')
    telefonberuflich = StringField('Telefon beruflich')
    allergien_unvertraeglichkeiten = TextAreaField('Allergien/Unverträglichkeiten')
    submit = SubmitField('Pfadikind hinzufügen')

class PfadiLagerForm(FlaskForm):
    name = StringField('Name des Lagers')
    datum = StringField('Datum des Lagers')
    submit = SubmitField('Submit')  

#Lageranmeldung 
class PfadikindAnmeldungForm(FlaskForm):
    vorname = StringField('Vorname', validators=[DataRequired()])
    nachname = StringField('Nachname', validators=[DataRequired()])
    pfadikind = SelectField('Pfadikind', validators=[DataRequired()])
    pfadiname = SelectField('Pfadiname', validators=[DataRequired()])
    pfadilager = SelectField('Pfadilager', validators=[DataRequired()])
    datum = StringField('Datum (MM/YYYY)', validators=[DataRequired()])
    submit = SubmitField('Anmelden')
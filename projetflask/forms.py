from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange
from projetflask.models import Utilisateur, Admin
from wtforms import ValidationError
from projetflask import bcrypt
from datetime import date




class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class AddTeacherForm(FlaskForm):
    nom = StringField('Nom',
                           validators=[DataRequired(), Length(min=2, max=20)])
    prenom = StringField('Prénom',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmer mot de passe',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Ajouter Enseignant')

    def validate_email(self, email):
        email = Utilisateur.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email already in use')


class AddStudentForm(FlaskForm):
    CIN = StringField('CIN',
                      validators=[DataRequired(), Length(min=8, max=8)])
    nom = StringField('Nom',
                           validators=[DataRequired(), Length(min=2, max=20)])
    prenom = StringField('Prénom',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmer mot de passe',
                                     validators=[DataRequired(), EqualTo('password')])
    specialite = StringField('Spécialité',
                           validators=[DataRequired()])
    niveau = IntegerField('Niveau',
                           validators=[DataRequired(), NumberRange(min=1, max=10)])
    groupe = IntegerField('Groupe',
                           validators=[DataRequired(), NumberRange(min=1, max=10)])
    submit = SubmitField('Ajouter Etudiant')

    def validate_email(self, email):
        email = Utilisateur.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email already in use')


class AddModuleForm(FlaskForm):
    nom = StringField('Nom',
                      validators=[DataRequired(), Length(min=2, max=20)])
    semestre = IntegerField('Semestre',
                           validators=[DataRequired()])
    annee = IntegerField('Année',
                           validators=[DataRequired(), NumberRange(min=1990, max=date.today().year)])
    submit = SubmitField('Soumettre')


class AddMatiereForm(FlaskForm):
    nom = StringField('Nom',
                      validators=[DataRequired(), Length(min=2, max=20)])
    coeff = FloatField('Coefficient',
                           validators=[DataRequired(), NumberRange(min=1, max=5)])
    pourcentageTP = FloatField('Pourcentage TP',
                           validators=[DataRequired(), NumberRange(min=0, max=1)])
    pourcentageDS = FloatField('Pourcentage DS',
                           validators=[DataRequired(), NumberRange(min=0, max=1)])
    pourcentageExam = FloatField('Pourcentage Examen',
                           validators=[DataRequired(), NumberRange(min=0, max=1)])
    submit = SubmitField('Soumettre')


class AddNoteForm(FlaskForm):
    TP = IntegerField('Note TP',
                           validators=[DataRequired(), NumberRange(min=0, max=20)])
    DS = IntegerField('Note DS',
                           validators=[DataRequired(), NumberRange(min=0, max=20)])
    Exam = IntegerField('Note Examen',
                           validators=[DataRequired(), NumberRange(min=0, max=20)])
    submit = SubmitField('Soumettre')


class UpTeacherForm(FlaskForm):
    nom = StringField('Nom',
                           validators=[DataRequired(), Length(min=2, max=20)])
    prenom = StringField('Prénom',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Nouveau mot de passe')
    confirm_password = PasswordField('Confirmer le nouveau mot de passe',
                                     validators=[EqualTo('password')])
    submit = SubmitField('Modifier Enseignant')

class UpStudentForm(FlaskForm):
    CIN = StringField('CIN',
                      validators=[DataRequired(), Length(8)])
    nom = StringField('Nom',
                           validators=[DataRequired(), Length(min=2, max=20)])
    prenom = StringField('Prénom',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Nouveau mot de passe')
    confirm_password = PasswordField('Confirmer le nouveau mot de passe',
                                     validators=[EqualTo('password')])
    specialite = StringField('Spécialité',
                           validators=[DataRequired(), Length(min=2, max=20)])
    niveau = IntegerField('Niveau',
                           validators=[DataRequired(), NumberRange(min=1, max=10)])
    groupe = IntegerField('Groupe',
                           validators=[DataRequired(), NumberRange(min=1, max=10)])
    submit = SubmitField('Modifier Etudiant')


class UpAdmin(FlaskForm):
    email = StringField('Email',
                        validators=[Email()])
    oldpass = PasswordField('Mot de passe ancient', validators=[DataRequired()])
    password = PasswordField('Nouveau Mot de passe')
    confirm_password = PasswordField('Confirmer le nouveau mot de passe',
                                     validators=[EqualTo('password')])

    submit = SubmitField('Modifier Login')

    def validate_oldpass(self, oldpass):
        admin = Admin.query.first()
        if not bcrypt.check_password_hash(admin.password, oldpass.data):
            raise ValidationError('Mot de passe incorrect')

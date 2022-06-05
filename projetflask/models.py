from datetime import datetime
from projetflask import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.query.get(int(user_id))

class Utilisateur(db.Model, UserMixin):
    __tablename__ = 'utilisateur'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    role = db.Column(db.String(30), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity':'utilisateur',
        'polymorphic_on':role
    }


class Etudiant(Utilisateur):
    __tablename__ = 'etudiant'
    id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), primary_key=True)
    CIN = db.Column(db.String(30), nullable=False, unique=True)
    nom = db.Column(db.String(30), nullable=False)
    prenom = db.Column(db.String(30), nullable=False)
    specialite = db.Column(db.String(30), nullable=False)
    niveau = db.Column(db.String(30), nullable=False)
    groupe = db.Column(db.String(30), nullable=False)
    matieres = db.relationship('Note', cascade="all,delete", backref='etudiant', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'etudiant',
    }


class Enseignant(Utilisateur):
    __tablename__ = 'enseignant'
    id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), primary_key=True)
    nom = db.Column(db.String(30), nullable=False)
    prenom = db.Column(db.String(30), nullable=False)
    matieres = db.relationship('Matiere', cascade="all,delete", backref='enseignant', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'enseignant',
    }


class Admin(Utilisateur):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }


class Matiere(db.Model):
    __tablename__ = 'matiere'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(30), nullable=False)
    coeff = db.Column(db.String(30), nullable=False)
    pourcentageTP = db.Column(db.Integer, nullable=False)
    pourcentageDS = db.Column(db.Integer, nullable=False)
    pourcentageExam = db.Column(db.Integer, nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    enseignant_id = db.Column(db.Integer, db.ForeignKey('enseignant.id'), nullable=False)
    etudiants = db.relationship('Note', cascade="all,delete", backref='matiere', lazy=True)


class Module(db.Model):
    __tablename__ = 'module'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(30), nullable=False)
    semestre = db.Column(db.Integer, nullable=False)
    annee = db.Column(db.Integer, nullable=False)
    matieres = db.relationship('Matiere', cascade="all,delete", backref='module', lazy=True)


class Note(db.Model):
    __tablename__ = 'note'
    id = db.Column(db.Integer, primary_key=True)
    DS = db.Column(db.Float, nullable=False)
    TP = db.Column(db.Float, nullable=False)
    Exam = db.Column(db.Float, nullable=False)
    etudiant_id = db.Column(db.Integer, db.ForeignKey('etudiant.id'), nullable=False)
    matiere_id = db.Column(db.Integer, db.ForeignKey('matiere.id'), nullable=False)

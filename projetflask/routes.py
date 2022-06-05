from flask import render_template, url_for, flash, redirect, request, abort
from projetflask import app, db, bcrypt
from projetflask.forms import LoginForm, AddTeacherForm, AddStudentForm, AddMatiereForm, AddModuleForm,\
    AddNoteForm, UpTeacherForm, UpStudentForm, UpAdmin
from projetflask.models import Utilisateur, Enseignant, Etudiant, Module, Matiere, Note, Admin
from flask_login import login_user, current_user, logout_user, login_required
from wtforms import ValidationError


posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/home")
def home():
    if current_user.role == "etudiant":
        list = Note.query.filter_by(etudiant_id=current_user.id)
        table = "Liste des notes"
    elif current_user.role == "enseignant":
        list = Note.query.all()
        table = "Liste des notes"
    else :
        list = Etudiant.query.all()
        table = "Liste des Etudiants"
    return render_template('home.html', posts=posts, title='Home', list=list, table=table)


@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Utilisateur.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route("/addTeacher", methods=['GET', 'POST'])
@login_required
def addTeacher():
    if current_user.role != "admin":
        abort(403)
    form = AddTeacherForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new = Enseignant(nom=form.nom.data, prenom=form.prenom.data, email=form.email.data,
                         password=hashed_password, role='enseignant')
        db.session.add(new)
        db.session.commit()
        flash('Le compte a été créé avec succès!', 'success')
        return redirect(url_for('listTeacher'))
    return render_template('add.html', title='Add', type="enseignant", form=form)


@app.route("/addStudent", methods=['GET', 'POST'])
@login_required
def addStudent():
    if current_user.role != "admin":
        abort(403)
    form = AddStudentForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new = Etudiant(CIN=form.CIN.data, nom=form.nom.data, prenom=form.prenom.data, email=form.email.data,
                       specialite=form.specialite.data, niveau=form.niveau.data,
                       groupe=form.groupe.data, password=hashed_password, role='etudiant')
        db.session.add(new)
        db.session.commit()
        flash('Le compte a été créé avec succès!', 'success')
        return redirect(url_for('listStudent'))
    return render_template('add.html', title='Add', type="etudiant", form=form)


@app.route("/addModule", methods=['GET', 'POST'])
@login_required
def addModule():
    if current_user.role != "admin":
        abort(403)
    form = AddModuleForm()
    if form.validate_on_submit():
        new = Module(nom=form.nom.data, semestre=form.semestre.data, annee=form.annee.data)
        db.session.add(new)
        db.session.commit()
        flash('Le module a été ajouté avec succès!', 'success')
        return redirect(url_for('listModule'))
    return render_template('add.html', title='Add', type="module", form=form)


@app.route("/addMatiere", methods=['GET', 'POST'])
@login_required
def addMatiere():
    if current_user.role != "admin":
        abort(403)
    form = AddMatiereForm()
    modules = Module.query.all()
    enseignants = Enseignant.query.all()
    if form.validate_on_submit():
        enseignant = Enseignant.query.get_or_404(request.form.get('enseignant'))
        module = Module.query.get_or_404(request.form.get('module'))
        if not (float(form.pourcentageTP.data) + float(form.pourcentageExam.data) + float(form.pourcentageDS.data) == 1):
            flash('La somme des pourcentage n est pass égale à 1', 'danger')
            return redirect(url_for('addMatiere'))
        new = Matiere(coeff=form.coeff.data,
                      pourcentageTP=form.pourcentageTP.data,
                      pourcentageDS=form.pourcentageDS.data,
                      pourcentageExam=form.pourcentageExam.data,
                      nom=form.nom.data,
                      enseignant=enseignant,
                      module=module
                      )
        db.session.add(new)
        db.session.commit()
        flash('La matière a été ajoutée avec succès!', 'success')
        return redirect(url_for('listMatiere'))
    return render_template('add.html', title='Add', type="matiere", form=form, enseignants=enseignants, modules=modules)


@app.route("/addNote", methods=['GET', 'POST'])
@login_required
def addNote():
    if current_user.role != "enseignant":
        abort(403)
    form = AddNoteForm()
    matieres = Matiere.query.all()

    if form.validate_on_submit():
        etudiant = Etudiant.query.filter_by(CIN=request.form.get('cinEtud')).first()
        if not etudiant:
            flash('CIN ne correspond à aucun etudiant! Ajout non effectué', 'danger')
            return redirect(url_for("addNote"))
        matiere = Matiere.query.get_or_404(request.form.get('mat'))
        new = Note(TP=form.TP.data, DS=form.DS.data, Exam=form.Exam.data,
                   etudiant=etudiant, matiere=matiere)
        db.session.add(new)
        db.session.commit()
        flash('La note a été ajoutée avec succès!', 'success')
        return redirect(url_for('listNote'))
    return render_template('add.html', title='Add', type="note", form=form, matieres=matieres)


@app.route("/listTeacher")
@login_required
def listTeacher():
    list = Enseignant.query.all()
    return render_template('list.html', title='List', type="enseignant", list=list)

@app.route("/listStudent")
@login_required
def listStudent():
    list = Etudiant.query.all()
    return render_template('list.html', title='List', type="etudiant", list=list)


@app.route("/listModule")
@login_required
def listModule():
    list = Module.query.all()
    return render_template('list.html', title='List', type="module", list=list)


@app.route("/listMatiere")
@login_required
def listMatiere():
    list = Matiere.query.all()
    return render_template('list.html', title='List', type="matiere", list=list)


@app.route("/listNote")
@login_required
def listNote():
    if current_user.role == "admin":
        abort(403)
    if current_user.role == "etudiant":
        list = Note.query.filter_by(etudiant_id=current_user.id)
    else:
        list = Note.query.all()
    return render_template('list.html', title='List', type="note", list=list)


@app.route("/deleteEnseignant/<int:item_id>")
@login_required
def deleteEnseignant(item_id):
    item = Enseignant.query.get_or_404(item_id)
    if current_user.role != "admin":
        abort(403)
    db.session.delete(item)
    db.session.commit()
    flash('Enseignant supprimé avec succès!', 'success')
    return redirect(url_for('home'))


@app.route("/deleteEtudiant/<int:item_id>")
@login_required
def deleteEtudiant(item_id):
    item = Etudiant.query.get_or_404(item_id)
    if current_user.role != "admin":
        abort(403)
    db.session.delete(item)
    db.session.commit()
    flash('Etudiant supprimé avec succès!', 'success')
    return redirect(url_for('home'))


@app.route("/deleteModule/<int:item_id>")
@login_required
def deleteModule(item_id):
    item = Module.query.get_or_404(item_id)
    if current_user.role != "admin":
        abort(403)
    db.session.delete(item)
    db.session.commit()
    flash('Module supprimé avec succès!', 'success')
    return redirect(url_for('home'))


@app.route("/deleteMatiere/<int:item_id>")
@login_required
def deleteMatiere(item_id):
    item = Matiere.query.get_or_404(item_id)
    if current_user.role != "admin":
        abort(403)
    db.session.delete(item)
    db.session.commit()
    flash('Matière supprimée avec succès!', 'success')
    return redirect(url_for('home'))


@app.route("/deleteNote/<int:item_id>")
@login_required
def deleteNote(item_id):
    item = Note.query.get_or_404(item_id)
    if current_user.role != "enseignant":
        abort(403)
    db.session.delete(item)
    db.session.commit()
    flash('Note supprimée avec succès!', 'success')
    return redirect(url_for('home'))


@app.route("/updateEnseignant/<int:item_id>", methods=['GET', 'POST'])
@login_required
def updateEnseignant(item_id):
    item = Enseignant.query.get_or_404(item_id)
    if current_user.role != "admin":
        abort(403)
    form = UpTeacherForm()
    if form.email.data != item.email:
        already = Utilisateur.query.filter_by(email=form.email.data).first()
        if (already):
            flash('Email deja utilisé! Modification non effectuée', 'danger')
            return redirect(url_for("updateEnseignant", item_id = item_id))
    if form.validate_on_submit():
        if form.password.data:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            item.password = hashed_password
        item.email = form.email.data
        item.nom = form.nom.data
        item.prenom = form.prenom.data
        db.session.commit()
        flash('Utilisateur modifié!', 'success')
        return redirect(url_for('listTeacher'))
    form.nom.data = item.nom
    form.prenom.data = item.prenom
    form.email.data = item.email
    return render_template('add.html', title='Update', type="enseignant", form=form)


@app.route("/updateEtudiant/<int:item_id>", methods=['GET', 'POST'])
@login_required
def updateEtudiant(item_id):
    item = Etudiant.query.get_or_404(item_id)
    if current_user.role != "admin":
        abort(403)
    form = UpStudentForm()
    if form.email.data != item.email:
        already = Utilisateur.query.filter_by(email=form.email.data).first()
        if (already):
            flash('Email deja utilisé! Modification non effectuée', 'danger')
            return redirect(url_for("updateEtudiant", item_id = item_id))
    if form.CIN.data != item.CIN:
        already = Etudiant.query.filter_by(CIN=form.CIN.data).first()
        if (already):
            flash('CIN deja utilisé! Modification non effectuée', 'danger')
            return redirect(url_for("updateEtudiant", item_id=item_id))
    if form.validate_on_submit():
        if form.password.data:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            item.password = hashed_password
        item.CIN = form.CIN.data
        item.specialite = form.specialite.data
        item.niveau = form.niveau.data
        item.groupe = form.groupe.data
        item.email = form.email.data
        item.nom = form.nom.data
        item.prenom = form.prenom.data
        db.session.commit()
        flash('Utilisateur modifié!', 'success')
        return redirect(url_for('listStudent'))
    form.nom.data = item.nom
    form.prenom.data = item.prenom
    form.email.data = item.email
    form.CIN.data = item.CIN
    form.specialite.data = item.specialite
    form.niveau.data = item.niveau
    form.groupe.data = item.groupe
    return render_template('add.html', title='Update', type="etudiant", form=form)


@app.route("/updateModule/<int:item_id>", methods=['GET', 'POST'])
@login_required
def updateModule(item_id):
    if current_user.role != "admin":
        abort(403)
    item = Module.query.get_or_404(item_id)
    form = AddModuleForm()
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.commit()
        flash('Module modifié!', 'success')
        return redirect(url_for('listModule'))
    form.nom.data = item.nom
    form.semestre.data = item.semestre
    form.annee.data = item.annee
    return render_template('add.html', title='Update', type="module", form=form)


@app.route("/updateMatiere/<int:item_id>", methods=['GET', 'POST'])
@login_required
def updateMatiere(item_id):
    if current_user.role != "admin":
        abort(403)
    item = Matiere.query.get_or_404(item_id)
    form = AddMatiereForm()
    modules = Module.query.all()
    enseignants = Enseignant.query.all()
    if form.validate_on_submit():
        enseignant = Enseignant.query.get_or_404(request.form.get('enseignant'))
        module = Module.query.get_or_404(request.form.get('module'))
        item.pourcentageDS = form.pourcentageDS.data
        item.pourcentageTP = form.pourcentageTP.data
        item.pourcentageExam = form.pourcentageExam.data
        item.nom = form.nom.data
        item.coeff = form.coeff.data
        item.enseignant = enseignant
        item.module = module
        db.session.commit()
        flash('Matiere modifiée!', 'success')
        return redirect(url_for('listMatiere'))
    form.nom.data = item.nom
    form.coeff.data = item.coeff
    form.pourcentageTP.data = item.pourcentageTP
    form.pourcentageDS.data = item.pourcentageDS
    form.pourcentageExam.data = item.pourcentageExam
    return render_template('add.html', title='Update', type="matiere", form=form,
                           modules=modules, enseignants=enseignants,
                           module=item.module, enseignant=item.enseignant)


@app.route("/updateNote/<int:item_id>", methods=['GET', 'POST'])
@login_required
def updateNote(item_id):
    if current_user.role != "enseignant":
        abort(403)
    item = Note.query.get_or_404(item_id)
    form = AddNoteForm()
    matieres = Matiere.query.all()
    if form.validate_on_submit():
        matiere = Matiere.query.get_or_404(request.form.get('mat'))
        etudiant = Etudiant.query.filter_by(CIN=request.form.get('cinEtud')).first()
        if not etudiant:
            flash('CIN ne correspond à aucun étudiant! Ajout non effectué', 'danger')
            return redirect(url_for("addNote"))
        item.DS = form.DS.data
        item.TP = form.TP.data
        item.Exam = form.Exam.data
        item.etudiant = etudiant
        item.matiere = matiere
        db.session.commit()
        flash('Note modifiée!', 'success')
        return redirect(url_for('listNote'))
    form.TP.data = item.TP
    form.DS.data = item.DS
    form.Exam.data = item.Exam
    return render_template('add.html', title='Update', type="note", form=form,
                           CIN=item.etudiant.CIN, matiere=item.matiere, matieres=matieres)


@app.route("/upAdmin", methods=['GET', 'POST'])
@login_required
def upAdmin():
    if current_user.role != "admin":
        abort(403)
    form = UpAdmin()
    item = Admin.query.first()
    if form.email.data != item.email:
        already = Utilisateur.query.filter_by(email=form.email.data).first()
        if (already):
            flash('Email deja utilisé! Modification non effectuée', 'danger')
            return redirect(url_for("upAdmin"))
    if form.validate_on_submit():
        if form.password.data:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            item.password = hashed_password
        item.email = form.email.data
        db.session.commit()
        flash('Login modifié!', 'success')
        return redirect(url_for('home'))
    form.email.data = item.email

    return render_template('add.html', type='admin', title='Update', form=form)

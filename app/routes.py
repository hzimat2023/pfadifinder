
from app import db
from app import app
from app.forms import LoginForm, PfadikindForm, RegistrationForm, PfadiLagerForm, PfadikindAnmeldungForm
from flask import Flask, flash, render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Pfadikind, Pfadilager, Pfadilageranmeldung
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required  
def index():
    user = current_user 
    pfadilager_entries = Pfadilager.query.all()

    return render_template('index.html', title='Home', user=user, pfadilager_entries=pfadilager_entries)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    vorname=form.vorname.data,
                    nachname=form.nachname.data,
                    email=form.email.data) 
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)




@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    pfadilageranmeldungen = Pfadilageranmeldung.query.all()

    return render_template('user.html', user=user, pfadilageranmeldungen=pfadilageranmeldungen)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.route('/register_pfadikind', methods=['GET', 'POST'])
@login_required  # Stellen Sie sicher, dass der Benutzer authentifiziert ist
def register_pfadikind():
    form = PfadikindForm()
    if form.validate_on_submit():
        # Hier erhalten Sie die ID des angemeldeten Benutzers
        user_id = current_user.id

        # Erstellen Sie ein neues Pfadikind und weisen Sie die user_id zu
        pfadikind = Pfadikind(
            pfadiname=form.pfadiname.data,
            vegetarisch=form.vegetarisch.data,
            vorname=form.vorname.data,
            nachname=form.nachname.data,
            geburtsdatum=form.geburtsdatum.data,
            adresse=form.adresse.data,
            telefonprivat=form.telefonprivat.data,
            telefonberuflich=form.telefonberuflich.data,
            allergien_unvertraeglichkeiten=form.allergien_unvertraeglichkeiten.data,
            user_id=user_id  # Weisen Sie die user_id zu
        )

        # Fügen Sie das Pfadikind zur Datenbank hinzu und speichern Sie es
        db.session.add(pfadikind)
        db.session.commit()

        flash('Pfadikind wurde erfolgreich hinzugefügt!')
        return redirect(url_for('index'))
    return render_template('register_pfadikind.html', title='Pfadikind registrieren', form=form)



@app.route('/create_pfadilager', methods=['GET', 'POST'])
def create_pfadilager():
    form = PfadiLagerForm()
    if form.validate_on_submit():
        name = form.name.data
        datum = form.datum.data
        
        new_pfadilager = Pfadilager(name=name, datum=datum)
        db.session.add(new_pfadilager)
        db.session.commit()
        
        flash('Pfadilager erfolgreich erstellt.', 'success')
        return redirect(url_for('create_pfadilager'))  
    
    return render_template('create_pfadilager.html', form=form)




@app.route('/pfadilager')
def pfadilager():
    
    lager_list = Pfadilager.query.all()

    return render_template('pfadilager.html', lager_list=lager_list)



@app.route('/anmeldung', methods=['GET', 'POST'])
@login_required
def anmeldung():
    form = PfadikindAnmeldungForm()
    form.pfadikind.choices = [(pfadikind.id, pfadikind.vorname) for pfadikind in Pfadikind.query.all()]
    form.pfadilager.choices = [(pfadilager.id, pfadilager.name) for pfadilager in Pfadilager.query.all()]

    if form.validate_on_submit():
        selected_pfadilager_id = form.pfadilager.data
        selected_pfadilager = Pfadilager.query.get(selected_pfadilager_id)
        datum = selected_pfadilager.datum

        anmeldung = Pfadilageranmeldung(
            user_id=current_user.id,
            pfadilager_id=selected_pfadilager_id,
            datum=datum,
            vorname=form.vorname.data,  # Add vorname field
            nachname=form.nachname.data  # Add nachname field
        )

        db.session.add(anmeldung)
        db.session.commit()
        flash('Du hast dich erfolgreich für das Pfadilager angemeldet.', 'success')
        return redirect(url_for('index'))

    return render_template('anmeldung.html', title='Pfadilager Anmeldung', form=form)







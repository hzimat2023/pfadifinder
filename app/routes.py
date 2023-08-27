
from app import db
from app import app
from app.forms import LoginForm, PfadikindForm, RegistrationForm, PfadiLagerForm, PfadikindAnmeldungForm
from flask import Flask, flash, render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Pfadikind, Pfadilager, Pfadilageranmeldung
from werkzeug.urls import url_parse
from functools import wraps


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.role != 'admin':
            flash('Nur Administratoren haben Zugriff auf diese Seite.', 'danger')
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    return decorated_view


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
    pfadilageranmeldungen = Pfadilageranmeldung.query.filter_by(user_id=current_user.id).all()

    return render_template('user.html', user=user, pfadilageranmeldungen=pfadilageranmeldungen)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.route('/register_pfadikind', methods=['GET', 'POST'])
@login_required 
def register_pfadikind():
    form = PfadikindForm()
    if form.validate_on_submit():
  
        user_id = current_user.id

       
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
            user_id=user_id  
        )


        db.session.add(pfadikind)
        db.session.commit()

        flash('Pfadikind wurde erfolgreich hinzugefügt!')
        return redirect(url_for('index'))
    return render_template('register_pfadikind.html', title='Pfadikind registrieren', form=form)



@app.route('/create_pfadilager', methods=['GET', 'POST'])
@login_required
@admin_required
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






@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    
    return render_template('admin_dashboard.html')




@app.route('/angemeldete_pfadilager', methods=['GET'])
@login_required
def angemeldete_pfadilager():
    anmeldungen = Pfadilageranmeldung.query.all()
    
    # Holen Sie alle Pfadilager und entfernen Sie Duplikate, um einzigartige Datumsauswahlen zu erhalten.
    pfadilager_list = Pfadilager.query.all()
    unique_dates = set(pfadilager.datum for pfadilager in pfadilager_list)

    selected_pfadilager = request.args.get('pfadilager', default='', type=str)
    selected_datum = request.args.get('datum', default='', type=str)

    if selected_pfadilager and selected_datum:
        # Filtern Sie die Anmeldungen nach ausgewähltem Pfadilager und Datum.
        anmeldungen = Pfadilageranmeldung.query.filter_by(pfadilager_id=selected_pfadilager, datum=selected_datum).all()
    elif selected_pfadilager:
        # Filtern Sie die Anmeldungen nach ausgewähltem Pfadilager.
        anmeldungen = Pfadilageranmeldung.query.filter_by(pfadilager_id=selected_pfadilager).all()
    elif selected_datum:
        # Filtern Sie die Anmeldungen nach ausgewähltem Datum.
        anmeldungen = Pfadilageranmeldung.query.filter_by(datum=selected_datum).all()

    return render_template('angemeldete_pfadilager.html', title='Angemeldete Pfadilager', anmeldungen=anmeldungen, pfadilager_list=unique_dates)







@app.route('/anmeldung', methods=['GET', 'POST'])
@login_required
def anmeldung():
    form = PfadikindAnmeldungForm()
    form.pfadiname.choices = [(str(pfadikind.id), pfadikind.pfadiname) for pfadikind in Pfadikind.query.filter_by(user_id=current_user.id).all()]
    form.pfadilager.choices = [(pfadilager.id, pfadilager.name) for pfadilager in Pfadilager.query.all()]
    form.vorname.choices = [(pfadikind.vorname, pfadikind.vorname) for pfadikind in Pfadikind.query.filter_by(user_id=current_user.id).all()]
    form.nachname.choices = [(pfadikind.nachname, pfadikind.nachname) for pfadikind in Pfadikind.query.filter_by(user_id=current_user.id).all()]

    if form.validate_on_submit():
        selected_pfadilager_id = form.pfadilager.data
        selected_pfadilager = Pfadilager.query.get(selected_pfadilager_id)
        datum = selected_pfadilager.datum

        anmeldung = Pfadilageranmeldung(
            user_id=current_user.id,
            pfadilager_id=selected_pfadilager_id,
            datum=datum,
            vorname=form.vorname.data,
            nachname=form.nachname.data,  
            pfadikind_id=form.pfadiname.data  
        )

        db.session.add(anmeldung)
        db.session.commit()
        flash('Du hast dich erfolgreich für das Pfadilager angemeldet.', 'success')
        return redirect(url_for('index'))

    return render_template('anmeldung.html', title='Pfadilager Anmeldung', form=form)

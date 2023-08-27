from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    vorname = db.Column(db.String(64))  
    nachname = db.Column(db.String(64))  
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(64), default='user') 
    pfadikinder = db.relationship('Pfadikind', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


pfadikinder = db.relationship('Pfadikind', backref='ersteller', lazy='dynamic')
class Pfadikind(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pfadiname = db.Column(db.String(64))
    vegetarisch = db.Column(db.Boolean)
    vorname = db.Column(db.String(64))
    nachname = db.Column(db.String(64))
    geburtsdatum = db.Column(db.Date)
    adresse = db.Column(db.String(128))
    telefonprivat = db.Column(db.String(20))
    telefonberuflich = db.Column(db.String(20))
    allergien_unvertraeglichkeiten = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Pfadikind {self.vorname} {self.nachname}>'

    
class Pfadilager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    datum = db.Column(db.String(50), nullable=False)
    

class Pfadilageranmeldung(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pfadilager_id = db.Column(db.Integer, db.ForeignKey('pfadilager.id'), nullable=False)
    datum = db.Column(db.String(50), nullable=False) 
    vorname = db.Column(db.String(64))  
    nachname = db.Column(db.String(64))  

    user = db.relationship('User', backref='pfadilager_anmeldungen')
    pfadilager = db.relationship('Pfadilager', backref='pfadilager_anmeldungen')
    pfadikind_id = db.Column(db.Integer, db.ForeignKey('pfadikind.id'), nullable=True)  
    pfadikind = db.relationship('Pfadikind', backref='pfadilager_anmeldung', foreign_keys=[pfadikind_id])

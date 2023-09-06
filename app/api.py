from flask import url_for, jsonify, request
from app import app, db, api
from app.models import User, Pfadilageranmeldung
from app.errors import error_response
from flask_sqlalchemy import SQLAlchemy


@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_data = {
            'id': user.id,
            'username': user.username,
            'vorname': user.vorname,
            'nachname': user.nachname,
            'email': user.email,
            'role': user.role
  
        }
        user_list.append(user_data)
    return jsonify(user_list)



@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    user_data = {
            'id': user.id,
            'username': user.username,
            'vorname': user.vorname,
            'nachname': user.nachname,
            'email': user.email,
            'role': user.role
    }
    return jsonify(user_data)



@app.route('/api/PfadilageranmeldungList', methods=['GET'])
def pfadilageranmeldung_list():
    anmeldungen = Pfadilageranmeldung.query.all()
    anmeldungen_list = []
    for anmeldung in anmeldungen:
        anmeldung_data = {
            'id': anmeldung.id,
            'datum': anmeldung.datum,
            'vorname': anmeldung.vorname,
            'nachname': anmeldung.nachname

        }
        anmeldungen_list.append(anmeldung_data)
    return jsonify(anmeldungen_list)
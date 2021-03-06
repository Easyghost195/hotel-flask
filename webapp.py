#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from flask import *
import sys
import psycopg2
import datetime
from datetime import *
import psycopg2.extras
from pymongo import *

#NE PAS MODIFIER LA LIGNE SUIVANTE
app = Flask(__name__)

app.secret_key = 'azerty'
USERNAME = 'martin'
PASSWORD = 'ici.fr'
session = {}

@app.route('/', methods=['GET', 'POST'])
def accueil(error=None):
   disconnect()
   session['dateDuJour'] = date.today().isoformat()
   flash('Bienvenue sur le site de l\'Hotel')
   flash('Date du jour : '+session['dateDuJour'])
   return render_template("accueil.html", session=session, hasError=error)


@app.route('/after_accueil', methods = ['POST'])
def after_accueil(error=None):
   session['accueil'] = request.form['accueil']
   if not session.get('logged_in'):
        if (session['accueil'] == "Reinitialiser la base"):
            return render_template("admin.html", hasError=error, session=session)
        else:
            flash("Vous n'êtes pas connecté")
            return render_template("accueil.html", session=session, hasError=error)
   else:
      if (session['accueil'] == "Réserver une chambre"):
         return render_template("choix_chambre.html", session=session, hasError=error, liste=chambre())
      elif (session['accueil'] == "Déclarer une consommation"):
         return render_template("choix_conso.html", hasError=error, session=session, liste=bar(), liste_chambre=chambre_in_use())
      elif (session['accueil'] == "Payer votre facture"):
         return render_template("payer_facture.html", hasError=error, session=session, liste=facture_client(), registre=client())
      elif (session['accueil'] == "Faire un commentaire"):
         return render_template("faire_comm.html", hasError=error, session=session)
      elif (session['accueil'] == "Reinitialiser la base"):
         return render_template("admin.html", hasError=error, session=session)


@app.route('/login', methods=['GET', 'POST'])
def login(error = None):
   if request.method == 'POST':
      if request.form['mail'] == "":
         error = 'Mail Invalide'
         return render_template('login.html', error=error, session=session)
      else:
         conn = connect()
         cur = conn.cursor()
         session['mail'] = request.form['mail']
         session['password'] = request.form['password']
         query = "SELECT idclient, nom, prenom, mail, password FROM hotelbis.client WHERE client.mail = '%s' AND client.password = '%s';" % (session['mail'], session['password'])
         rows = select(query)
         nom_id = select("SELECT * FROM hotelbis.client WHERE client.mail = '%s' ;" % session['mail'])

         session['idClient'] = nom_id[0][0]
         session['nom'] = nom_id[0][1]
         print(session['nom'])
         print(session['idClient'])
         if rows != []:
            cur.execute(query)
            rows = cur.fetchall()
            session['logged_in'] = True
            flash('Connecté')
            flash('Bienvenue sur le site de l\'Hotel')
            #flash('Date du jour : '+session['dateDuJour'])
            return render_template('accueil.html', session=session, error=error)
         else:
            error = 'Password Incorrect'
            return render_template('login.html', error=error, session=session)
   return render_template('login.html', error=error, session=session)


@app.route('/create_account', methods=['GET', 'POST'])
def create_account(error = None):
   if request.method == 'POST':
      session['nom']=request.form['nom']
      session['prenom']=request.form['prenom']
      session['mail']=request.form['mail']
      session['password']=request.form['password']
      command = "INSERT INTO hotelbis.client values(DEFAULT, '%s', '%s', '%s', '%s');" % (session['nom'], session['prenom'], session['mail'], session['password'])
      rows = insert(command)
      flash('Compte Créé')
      return render_template('accueil.html', error=error, session=session)
   return render_template('create_account.html', error=error, session=session)


@app.route('/logout')
def logout():
   session.pop('logged_in', None)
   session['idClient'] = []
   flash('Déconnecté')
   return redirect(url_for('accueil'))


@app.route("/after_admin", methods=['POST'])
def after_admin(error=None):
    if (request.form['pwdadmin'].strip()=='admin'):
        drop_db()
        init_db()
        mgdb_drop_db()
        mgdb_init_db()
        flash('Base réinitialisée.')
        session.pop('logged_in', None)
        session['idClient'] = []
    else:
        flash('Désolé, mot de passe erroné.')
    return redirect(url_for('accueil'))


@app.route('/bravo', methods = ['POST'])
def bravo(error=None):
   session['debut']=request.form['date_debut']
   session['fin']=request.form['date_fin']
   command = "insert into HotelBis.Reservation values(DEFAULT, '%s', '%s', '%s', '%s', FALSE, DEFAULT);" % (session['idClient'], session['idChambre'], session['debut'], session['fin'] )
   print(command)
   rows = insert(command)
   print(rows)
   #command = "insert into HotelBis.Reservation values(DEFAULT, 1, 3, '2018-11-10', '2018-11-15', FALSE, DEFAULT);"
   #insert(command)
   return render_template("bravo.html", hasError=error, session=session)

@app.route('/paye', methods=['GET', 'POST'])
def paye(error=None):
    session['idChambre']=request.form['idChambre']
    # Modifie la facture du client pour qu'elle soit payée avec la date du jour
    command = "UPDATE HotelBis.Reservation SET reglee = 'True', date_reglement = '%s' WHERE reservation.idclient=%s AND reservation.idchambre=%s;" % (session['dateDuJour'],session['idClient'], session['idChambre'])
    #command = "DELETE FROM HotelBis.Reservation WHERE  reservation.idclient=%s AND reservation.idchambre=%s;" % (session['idClient'], session['idChambre'])
    print(command)
    rows = insert(command)
    print(rows)
    return render_template("bravo.html", hasError=error, session=session)


@app.route('/conso', methods=['GET', 'POST'])
def conso(error=None):
    session['idChambre']=request.form['idChambre']
    session['bar']=request.form['bar']
    session['quantité']=request.form['quantité']
    command = "INSERT INTO HotelBis.consommation Values('%s', '%s', '%s', '%s')" % (session['idChambre'], session['dateDuJour'], session['bar'], session['quantité'])
    print(command)
    rows = insert(command)
    print(rows)
    return render_template("bravo.html", hasError=error, session=session)


@app.route('/commentaire', methods=['GET', 'POST'])
def commentaire(error=None):
    session['idChambre']=request.form['idChambre']
    session['commentaire']=request.form['commentaire']
    print(session['commentaire'])
    insert_comment(session['idChambre'], session['nom'], session['dateDuJour'], session['commentaire'])
    return render_template("commentaire_done.html", hasError=error, session=session)


@app.route('/test', methods = ['POST'])
def test():
   return render_template('test.html')


@app.route('/choix_chambre3', methods =['GET', 'POST'])
def choix_chambre3(error=None):
   session['idChambre'] = request.form['idChambre']
   return render_template("choix_chambre3.html", session=session, desc=mgdb_display_chambre(session['idChambre']), com=mgdb_display_comments(session['idChambre']), rows=display_chambre(session['idChambre']), hasError=error)


def connect():
   print('Trying to connect to the database')
   try:
      conn = psycopg2.connect("host=dbserver dbname=jyclaudel user=jyclaudel")
      print('Connected to the database')
      return conn
   except Exception as e :
      return "Cannot connect to database: " + str(e)


def disconnect():
   db = getattr(g,'db_pgsql', None)
   if db is not None:
     g.db_pgsql.close()
     g.db_pgsql = None


def drop_db():
   db = connect()
   cur = db.cursor()
   try:
      with app.open_resource('hotel_destruction.sql') as f:
         cur.execute(f.read().decode('utf8'))
      db.commit()
   except Exception as e :
      flash('Désolé, service indisponible actuellement.')
      flash(str(e))
      return redirect(url_for('accueil', error=str(e)))


def init_db():
   db = connect()
   cur = db.cursor()
   try:
     with app.open_resource('hotel_creation.sql') as f:
         cur.execute(f.read().decode('utf8'))
     db.commit()
     with app.open_resource('hotel_function.sql') as f:
         cur.execute(f.read().decode('utf8'))
     db.commit()
     with app.open_resource('hotel_contrainte.sql') as f:
         cur.execute(f.read().decode('utf8'))
     db.commit()
     with app.open_resource('hotel_view.sql') as f:
         cur.execute(f.read().decode('utf8'))
     db.commit()
     with app.open_resource('hotel_insertion2.sql') as f:
        cur.execute(f.read().decode('utf8'))
     db.commit()
   except Exception as e :
     flash('Désolé, service indisponible actuellement.')
     flash(str(e))
     return redirect(url_for('accueil', error=str(e)))


def select(command):
   conn = connect()
   cur = conn.cursor()
   try:
      cur.execute(command)
      rows = cur.fetchall()
      cur.close()
      return rows
   except Exception as e :
      flash('Désolé, une erreur s\'est produite.')
      return redirect(url_for('accueil', error=str(e)))


def insert(command):
   conn = connect()
   cur = conn.cursor()
   try:
      cur.execute(command)
      nb = cur.rowcount
      conn.commit()
      cur.close()
      return nb
   except Exception as e :
      print(e)
      flash('Désolé, une erreur s\'est produite.')
      return redirect(url_for('accueil', error=str(e)))


def chambre():
   command = 'select * from hotelbis.chambre;'
   rows = select(command)
   return rows

def chambre_in_use():
    # N'affiche que les chambres utilisées par le client connecté
   command = "SELECT DISTINCT idchambre FROM hotelbis.reservation WHERE idClient = '%s';" % session['idClient']
   rows = select(command)
   return rows

def client():
   command = 'select * from hotelbis.client;'
   rows = select(command)
   return rows


def bar():
   command = 'select * from hotelbis.bar;'
   rows = select(command)
   return rows


def facture():
   command = 'select * from hotelbis.reservation;'
   rows = select(command)
   return rows

def facture_client():
    # Affiche les factures impayées du client connecté
    command = "SELECT * FROM hotelbis.reservation WHERE reservation.idclient='%s' AND reservation.date_reglement = '1970-01-01';" % session['idClient']
    rows = select(command)
    print(rows)
    return rows


def display_chambre(idChambre):
   rows = select("select * from hotelbis.chambre where idchambre = %s;" % idChambre)
   return rows


# MongoDB
def mgdb_display_chambre(idChambre):
    mgdb = get_mg_db()
    if mgdb:
        return mgdb.chambres.find({"chambre_id":int(idChambre)})
    else:
        return None


def mgdb_display_comments(idChambre):
    mgdb = get_mg_db()
    if mgdb:
        return mgdb.comments.find({"chambre_id":int(idChambre)})
    else:
        return None


def get_mg_db():
    db = getattr(g, '_mg_database', None)
    if db is None:
        db = g._mg_database = MongoClient("mongodb://mongodb.emi.u-bordeaux.fr:27017").jyclaudel
    return db


def mgdb_drop_db():
    mgdb = get_mg_db()
    mgdb.chambres.drop()
    mgdb.comments.drop()


def mgdb_init_db():
    creer_mongodb()

def insert_comment(idChambre, nom, jour, commentaire):
    mgdb = get_mg_db()
    print(commentaire)
    result = mgdb.comments.insert(
        {
            "chambre_id": int(idChambre),
            "client_nom": nom,
            "date": jour,
            "commentaire": commentaire
        }
    )
    return result

def creer_mongodb():
    mgdb = get_mg_db()
    print("Création mongodb")
    result = mgdb.chambres.insert([
        {
            "_id": 1,
            "chambre_id": 1,
            "nom": "Bleue",
            "étage": 1,
            "vue": "Ocean",
            "couchage": "Un grand lit",
            "salle de bain": {
                "douche": "Italienne",
                "baignoire": "à bulles"
                }
        },
        {
            "_id": 2,
            "chambre_id": 2,
            "nom": "Verte",
            "étage": 1,
            "vue": "Ocean",
            "couchage": "Un grand lit",
            "salle de bain": {
                "douche": "Italienne",
                "baignoire": "à bulles"
                }
        },
        {
            "_id": 3,
            "chambre_id": 3,
            "nom": "Rouge",
            "étage": 2,
            "vue": "Ocean",
            "couchage": "Un grand lit",
            "salle de bain": {
                "douche": "Italienne",
                "baignoire": "à bulles"
                }
        },
        {
            "_id": 4,
            "chambre_id": 4,
            "nom": "Beige",
            "étage": 2,
            "vue": "Ocean",
            "couchage": "Un grand lit",
            "salle de bain": {
                "douche": "Italienne",
                "baignoire": "à bulles"
                }
        },
        {
            "_id": 5,
            "chambre_id": 5,
            "nom": "Violet",
            "étage": 3,
            "vue": "Ocean",
            "couchage": "Un grand lit",
            "salle de bain": {
                "douche": "Italienne",
                "baignoire": "à bulles"
                }
        },
        {
            "_id": 6,
            "chambre_id": 6,
            "nom": "Rose",
            "étage": 3,
            "vue": "Ville",
            "couchage": "Un grand lit",
            "salle de bain": {
                "douche": "Italienne",
                "baignoire": "à bulles"
                }
        },
        {
            "_id": 7,
            "chambre_id": 7,
            "nom": "Turquoise",
            "étage": 4,
            "vue": "Ocean",
            "couchage": "Un grand lit",
            "salle de bain": {
                "douche": "Italienne",
                "baignoire": "à bulles"
                }
        },
        {
            "_id": 8,
            "chambre_id": 8,
            "nom": "Noire",
            "étage": 4,
            "vue": "Ocean",
            "couchage": "Un grand lit",
            "salle de bain": {
                "douche": "Italienne",
                "baignoire": "à bulles"
                }
        },
        {
            "_id": 9,
            "chambre_id": 9,
            "nom": "Bleu ciel",
            "étage": 5,
            "vue": "Ocean",
            "couchage": "Un grand lit",
            "salle de bain": {
                "douche": "Italienne",
                "baignoire": "à bulles"
                }
        },
        {
            "_id": 10,
            "chambre_id": 10,
            "nom": "Jaune",
            "étage": 5,
            "vue": "Au dessus des nuages",
            "couchage": "Un grand lit",
            "salle de bain": {
                "douche": "Italienne",
                "baignoire": "à bulles"
                }
        }
        ]
    )
    return result

#NE SURTOUT PAS MODIFIER
if __name__ == "__main__":
   app.run(debug=True)

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


@app.route('/', methods=['GET', 'POST'])
def accueil(error=None):
   disconnect()
   session = {}
   session['dateDuJour'] = date.today().isoformat()
   flash('Bienvenue sur le site de l\'Hotel')
   flash('Date du jour : '+session['dateDuJour'])
   return render_template("accueil.html", session=session, hasError=error)


@app.route('/after_accueil', methods = ['POST'])
def after_accueil(error=None):
   session['accueil'] = request.form['accueil']
   if not session.get('logged_in'):
      flash("Vous n'êtes pas connecté")
      return render_template("accueil.html", session=session, hasError=error)
   else:
      if (session['accueil'] == "Réserver une chambre"):
         return render_template("choix_chambre.html", session=session, hasError=error, liste=chambre())
      elif (session['accueil'] == "Déclarer une consommation"):
         return render_template("choix_conso.html", hasError=error, session=session, liste=bar())
      elif (session['accueil'] == "Payer votre facture"):
         return render_template("payer_facture.html", hasError=error, session=session, liste=facture(), registre=client())
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
        flash('Base réinitialisée.')
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

@app.route('/test', methods = ['POST'])
def test():
   return render_template('test.html')

@app.route('/choix_chambre3', methods =['GET', 'POST'])
def choix_chambre3(error=None):
   session['idChambre'] = request.form['idChambre']
   return render_template("choix_chambre3.html", session=session, rows=display_chambre(session['idChambre']), hasError=error)


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
      return redirect(url_for('accueil.', error=str(e)))


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
     with app.open_resource('hotel_insertion.sql') as f:
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


def display_chambre(idChambre):
   rows = select("select * from hotelbis.chambre where idchambre = %s;" % idChambre)
   return rows

#NE SURTOUT PAS MODIFIER
if __name__ == "__main__":
   app.run(debug=True)

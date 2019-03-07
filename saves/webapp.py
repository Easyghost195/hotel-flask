import time
from flask import *
import sys
import psycopg2

def tout_dragon():
    # Try to connect to an existing database
    print('Trying to connect to the database')
    try:
        conn = psycopg2.connect("host=dbserver dbname=algriffa user=algriffa")
        print('Connected to the database')
        cur = conn.cursor()
        command = 'select * from mesdragons.dragons;'
        print('Trying to execute command: ' + command)
        try:
            # Query the database and obtain data as Python objects
            cur.execute(command)
            print("execute ok")
            #retrieve all tuple
            rows = cur.fetchall() #rows => tableau (les lignes du résultat) de listes (les différents attributs du résultat)
            print("fetchall ok")
            return rows
        except Exception as e :
            return redirect(url_for('hello', error=str(e)))
    except Exception as e :
        return "Cannot connect to database: " + str(e)

def display_dragon(prenom_dragon):
    # Try to connect to an existing database
    print('Trying to connect to the database')
    try:
        conn = psycopg2.connect("host=dbserver dbname=algriffa user=algriffa")
        print('Connected to the database')
        cur = conn.cursor()
        command = 'select * from mesdragons.dragons where dragon =\'' + prenom_dragon + '\';'
        print('Trying to execute command: ' + command)
        try:
            # Query the database and obtain data as Python objects
            cur.execute(command)
            print("execute ok")
            #retrieve all tuple
            rows = cur.fetchall() #rows => tableau (les lignes du résultat) de listes (les différents attributs du résultat)
            print("fetchall ok")
            page = ''
            dragon = rows[0]
            page = prenom_dragon
            if dragon[1] == 'M':
                page = page + ' est un male'
            else:
                page = page + 'est une femelle'
                page = page + ' et a ' + str(dragon[3]) + 'ecailles.\n'
            # Close communication with the database
            cur.close()
            conn.close()
            print('Returning page ' + page)
            return page
        except Exception as e :
            return redirect(url_for('hello', error=str(e)))
    except Exception as e :
        return "Cannot connect to database: " + str(e)
    
#NE PAS MODIFIER LA LIGNE SUIVANTE
app = Flask(__name__)
     
#Hello world basique
@app.route("/")
def hello():
    error=request.args.get('error', None)
    return render_template("form.html", hasError=error, liste=tout_dragon())

#@app.route('/after_form', methods=['POST'])
#def after_form():
#    print("I got it!")
#    return hello_name(request.form['prenom'])

@app.route('/after_form', methods=['POST'])
def after_form():
    return display_dragon(request.form['prenom'])

#Hello world avec récupération de paramètres
@app.route("/hello/<name>")
def hello_name(name):
	data= "<b>Bonjour "+name+"</b>. Nous sommes le " + time.strftime("%d/%m/%Y")
	return data


#NE SURTOUT PAS MODIFIER     
if __name__ == "__main__":
   app.run(debug=True)

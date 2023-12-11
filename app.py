from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def connect_database():
    conn = sqlite3.connect("carnet_adresses.db")
    cursor = conn.cursor()
    return conn, cursor

def create_contacts_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            email TEXT,
            telephone TEXT
        )
    ''')

def ajouter_contact(cursor, nom, prenom, email, telephone):
    cursor.execute('''
        INSERT INTO contacts (nom, prenom, email, telephone)
        VALUES (?, ?, ?, ?)
    ''', (nom, prenom, email, telephone))

def afficher_tous_les_contacts(cursor):
    cursor.execute('''
        SELECT * FROM contacts
    ''')

    contacts = cursor.fetchall()
    return contacts

@app.route('/')
def index():
    conn, cursor = connect_database()
    create_contacts_table(cursor)
    contacts = afficher_tous_les_contacts(cursor)
    conn.close()
    return render_template('index.html', contacts=contacts)

@app.route('/ajouter', methods=['GET', 'POST'])
def ajouter():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        telephone = request.form['telephone']

        conn, cursor = connect_database()
        ajouter_contact(cursor, nom, prenom, email, telephone)
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('ajouter.html')

if __name__ == "__main__":
    app.run(debug=True)

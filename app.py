import tkinter as tk
from tkinter import ttk
import sqlite3

def connect_database():
    conn = sqlite3.connect("carnet_adresses.db")
    cursor = conn.cursor()
    return conn, cursor

def add_contact(conn, cursor, nom, prenom, email=None, telephone=None):
    cursor.execute('''
        INSERT INTO contacts (nom, prenom, email, telephone)
        VALUES (?, ?, ?, ?)
    ''', (nom, prenom, email, telephone))
    conn.commit()

class CarnetAdressesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Carnet d'adresses")

        # Création des champs de saisie
        self.label_nom = ttk.Label(root, text="Nom:")
        self.entry_nom = ttk.Entry(root)

        self.label_prenom = ttk.Label(root, text="Prénom:")
        self.entry_prenom = ttk.Entry(root)

        self.label_email = ttk.Label(root, text="E-mail:")
        self.entry_email = ttk.Entry(root)

        self.label_telephone = ttk.Label(root, text="Téléphone:")
        self.entry_telephone = ttk.Entry(root)

        # Bouton d'ajout
        self.button_ajouter = ttk.Button(root, text="Ajouter", command=self.ajouter_contact)

        # Positionnement des éléments
        self.label_nom.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_nom.grid(row=0, column=1, padx=10, pady=5)

        self.label_prenom.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_prenom.grid(row=1, column=1, padx=10, pady=5)

        self.label_email.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_email.grid(row=2, column=1, padx=10, pady=5)

        self.label_telephone.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.entry_telephone.grid(row=3, column=1, padx=10, pady=5)

        self.button_ajouter.grid(row=4, column=0, columnspan=2, pady=10)

    def ajouter_contact(self):
        nom = self.entry_nom.get()
        prenom = self.entry_prenom.get()
        email = self.entry_email.get()
        telephone = self.entry_telephone.get()

        # Ajouter le contact à la base de données
        conn, cursor = connect_database()
        add_contact(conn, cursor, nom, prenom, email, telephone)
        conn.close()

        # Effacer les champs de saisie après l'ajout
        self.entry_nom.delete(0, "end")
        self.entry_prenom.delete(0, "end")
        self.entry_email.delete(0, "end")
        self.entry_telephone.delete(0, "end")

if __name__ == "__main__":
    root = tk.Tk()
    app = CarnetAdressesApp(root)
    root.mainloop()

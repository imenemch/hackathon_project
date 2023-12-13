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

def search_contacts(cursor, recherche):
    cursor.execute('''
        SELECT * FROM contacts
        WHERE nom LIKE ? OR prenom LIKE ? OR email LIKE ? OR telephone LIKE ?
    ''', (f'%{recherche}%', f'%{recherche}%', f'%{recherche}%', f'%{recherche}%'))
    return cursor.fetchall()

def delete_contact(conn, cursor, contact_id):
    cursor.execute('''
        DELETE FROM contacts
        WHERE id = ?
    ''', (contact_id,))
    conn.commit()

class Carnet_Gestion_Adresses:
    def __init__(self, root):
        self.root = root
        self.root.title("Carnet d'adresses")

        # ... (champs de saisie, bouton Ajouter, champs de recherche)

        # Champs de suppression
        self.label_suppression = ttk.Label(root, text="ID du contact à supprimer:")
        self.entry_suppression = ttk.Entry(root)
        self.button_supprimer = ttk.Button(root, text="Supprimer", command=self.supprimer_contact)

        # Positionnement des éléments de suppression
        self.label_suppression.grid(row=7, column=0, padx=10, pady=5, sticky="w")
        self.entry_suppression.grid(row=7, column=1, padx=10, pady=5)
        self.button_supprimer.grid(row=7, column=2, pady=5)

    def supprimer_contact(self):
        contact_id = self.entry_suppression.get()

        # Vérifier si l'ID est un entier
        try:
            contact_id = int(contact_id)
        except ValueError:
            # Afficher un message d'erreur si l'ID n'est pas un entier
            tk.messagebox.showerror("Erreur", "Veuillez entrer un ID valide.")
            return

        # Supprimer le contact de la base de données
        conn, cursor = connect_database()
        delete_contact(conn, cursor, contact_id)
        conn.close()

        # Effacer les champs de saisie après la suppression
        self.entry_suppression.delete(0, "end")

if __name__ == "__main__":
    root = tk.Tk()
    app = Carnet_Gestion_Adresses(root)
    root.mainloop()

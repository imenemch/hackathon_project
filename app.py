import tkinter as tk
from tkinter import ttk
import sqlite3

class CarnetGestionAdresses:
    def __init__(self, root):
        self.root = root
        self.root.title("Carnet d'adresses")

        # Database connection
        self.conn = sqlite3.connect("carnet_adresses.db")
        self.cursor = self.conn.cursor()

        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.grid(row=0, column=0, columnspan=3, rowspan=6, padx=10, pady=5, sticky="nesw")

        # Create tabs
        self.tab_add = ttk.Frame(self.notebook)
        self.tab_search = ttk.Frame(self.notebook)
        self.tab_delete = ttk.Frame(self.notebook)

        # Add tabs to the notebook
        self.notebook.add(self.tab_add, text='Ajouter')
        self.notebook.add(self.tab_search, text='Rechercher')
        self.notebook.add(self.tab_delete, text='Supprimer')

        # Initialize each tab
        self.init_add_tab()
        self.init_search_tab()
        self.init_delete_tab()

    def init_add_tab(self):
        ttk.Label(self.tab_add, text="Nom:").grid(row=0, column=0, pady=5)
        ttk.Label(self.tab_add, text="Prénom:").grid(row=1, column=0, pady=5)
        ttk.Label(self.tab_add, text="Email:").grid(row=2, column=0, pady=5)
        ttk.Label(self.tab_add, text="Téléphone:").grid(row=3, column=0, pady=5)

        self.entry_nom = ttk.Entry(self.tab_add)
        self.entry_prenom = ttk.Entry(self.tab_add)
        self.entry_email = ttk.Entry(self.tab_add)
        self.entry_telephone = ttk.Entry(self.tab_add)

        self.entry_nom.grid(row=0, column=1, pady=5)
        self.entry_prenom.grid(row=1, column=1, pady=5)
        self.entry_email.grid(row=2, column=1, pady=5)
        self.entry_telephone.grid(row=3, column=1, pady=5)

        ttk.Button(self.tab_add, text="Ajouter", command=self.ajouter_contact).grid(row=4, column=0, columnspan=2, pady=10)

    def ajouter_contact(self):
        nom = self.entry_nom.get()
        prenom = self.entry_prenom.get()
        email = self.entry_email.get()
        telephone = self.entry_telephone.get()

        try:
            self.add_contact(nom, prenom, email, telephone)
            # Optionally, clear the entry fields after adding
            self.entry_nom.delete(0, "end")
            self.entry_prenom.delete(0, "end")
            self.entry_email.delete(0, "end")
            self.entry_telephone.delete(0, "end")
        except Exception as e:
            tk.messagebox.showerror("Erreur", f"Erreur lors de l'ajout : {str(e)}")

    def add_contact(self, nom, prenom, email=None, telephone=None):
        self.cursor.execute('''
            INSERT INTO contacts (nom, prenom, email, telephone)
            VALUES (?, ?, ?, ?)
        ''', (nom, prenom, email, telephone))
        self.conn.commit()

    def init_search_tab(self):
        ttk.Label(self.tab_search, text="Recherche:").grid(row=0, column=0, pady=5)
        self.entry_recherche = ttk.Entry(self.tab_search)
        self.entry_recherche.grid(row=0, column=1, pady=5)
        ttk.Button(self.tab_search, text="Rechercher", command=self.rechercher_contacts).grid(row=1, column=0, columnspan=2, pady=10)

        # Display area for search results (adjust as needed)
        self.results_text = tk.Text(self.tab_search, height=10, width=40)
        self.results_text.grid(row=2, column=0, columnspan=2, pady=5)

    def rechercher_contacts(self):
        recherche = self.entry_recherche.get()
        try:
            results = self.search_contacts(recherche)
            # Display or process the results as needed
            self.results_text.delete(1.0, "end")
            for result in results:
                self.results_text.insert("end", f"{result}\n")
        except Exception as e:
            tk.messagebox.showerror("Erreur", f"Erreur lors de la recherche : {str(e)}")

    def search_contacts(self, recherche):
        self.cursor.execute('''
            SELECT * FROM contacts
            WHERE nom LIKE ? OR prenom LIKE ? OR email LIKE ? OR telephone LIKE ?
        ''', (f'%{recherche}%', f'%{recherche}%', f'%{recherche}%', f'%{recherche}%'))
        return self.cursor.fetchall()

    def init_delete_tab(self):
        ttk.Label(self.tab_delete, text="ID du contact à supprimer:").grid(row=0, column=0, pady=5)
        self.entry_suppression = ttk.Entry(self.tab_delete)
        self.entry_suppression.grid(row=0, column=1, pady=5)
        ttk.Button(self.tab_delete, text="Supprimer", command=self.supprimer_contact).grid(row=1, column=0, columnspan=2, pady=10)

    def supprimer_contact(self):
        contact_id = self.entry_suppression.get()

        # Vérifier si l'ID est un entier
        try:
            contact_id = int(contact_id)
        except ValueError:
            # Afficher un message d'erreur si l'ID n'est pas un entier
            tk.messagebox.showerror("Erreur", "Veuillez entrer un ID valide.")
            return

        try:
            # Supprimer le contact de la base de données
            self.delete_contact(contact_id)

            # Effacer les champs de saisie après la suppression
            self.entry_suppression.delete(0, "end")
        except Exception as e:
            # Afficher une fenêtre d'erreur en cas d'échec de suppression
            tk.messagebox.showerror("Erreur", f"Erreur lors de la suppression : {str(e)}")

    def delete_contact(self, contact_id):
        self.cursor.execute('''
            DELETE FROM contacts
            WHERE id = ?
        ''', (contact_id,))
        self.conn.commit()

if __name__ == "__main__":
    root = tk.Tk()
    app = CarnetGestionAdresses(root)
    root.mainloop()

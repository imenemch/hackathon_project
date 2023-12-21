#Import de tkinter
import csv
from datetime import datetime
from tkinter import ttk, filedialog
from tkinter import *
import sqlite3
from tkinter import messagebox
import pandas as pd
import os



def carnet_adresses(id_user):
    # titre general
    root = Tk()
    root.title("Carnet d'addresses")
    root.geometry("1300x700")

    def ajouter():
        nom = entrernom.get()
        prenom = entrerPrenom.get()
        email = entrermail.get()
        tel = entrertelephone.get()
        adresse = entreradresse.get()
        groupe = entrergroupeC.get()

        # Vérifier si les champs obligatoires ne sont pas vides
        if not nom or not prenom or not email or not tel or not adresse:
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
            return  # Arrêter la fonction si un champ est vide

        # Vérifier le format de l'e-mail
        if "@" not in email or (".fr" not in email and ".com" not in email):
            messagebox.showerror("Erreur", "Format d'e-mail invalide.")
            return  # Arrêter la fonction si l'e-mail est invalide

        # Vérifier si le contact existe déjà par email ou téléphone
        if contact_existe(email, tel):
            messagebox.showerror("Erreur", "Ce contact existe déjà dans le carnet d'adresses.")
            return
        # Création de la connexion
        con = sqlite3.connect('carnet_adresses.db')
        cuser = con.cursor()
        # Convertir la date en chaîne au format ISO 8601
        date_ajout = datetime.today().isoformat()

        cuser.execute(
            "INSERT INTO contacts('nom','prenom','email','telephone','adresse', 'groupe','date_ajout', 'id_user') VALUES (?,?,?,?,?,?,?,?)",
            (nom, prenom, email, tel, adresse, groupe, date_ajout,id_user))

        # Récupérer l'ID de la dernière ligne insérée
        last_id = cuser.lastrowid

        con.commit()
        con.close()

        # Afficher le dernier contact ajouté
        con = sqlite3.connect('carnet_adresses.db')
        cuser = con.cursor()
        select = cuser.execute(f"SELECT * FROM contacts WHERE id = {last_id}")
        row = select.fetchone()
        table.insert('', END, values=row)
        con.close()

        # Afficher le message d'information
        messagebox.showinfo("Succès", "Contact ajouté avec succès!")

        # Effacer les entrées
        entrernom.delete(0, END)
        entrerPrenom.delete(0, END)
        entrermail.delete(0, END)
        entrertelephone.delete(0, END)
        entreradresse.delete(0, END)
        entrergroupeC.delete(0, END)

    def afficher_donnees_selectionnees(event):
        # Récupérer l'ID de l'élément sélectionné
        contact = table.selection()
        if contact:
            values = table.item(contact, 'values')
            entrernom.delete(0, END)
            entrerPrenom.delete(0, END)
            entrermail.delete(0, END)
            entrertelephone.delete(0, END)
            entreradresse.delete(0, END)
            entrergroupeC.delete(0, END)

            entrernom.insert(0, values[1])
            entrerPrenom.insert(0, values[2])
            entrermail.insert(0, values[3])
            entrertelephone.insert(0, values[4])
            entreradresse.insert(0, values[5])
            entrergroupeC.insert(0, values[6])

    def modifier():
        # Récupérer l'ID de l'élément sélectionné
        contact = table.selection()
        if contact:
            id_selectionne = table.item(contact)['values'][0]
            nom_selectionne = table.item(contact)['values'][1]
            prenom_selectionne = table.item(contact)['values'][2]
            email_selectionne = table.item(contact)['values'][3]
            telephone_selectionne = table.item(contact)['values'][4]
            adresse_selectionne = table.item(contact)['values'][5]
            groupe_selectionne = table.item(contact)['values'][6]
            date_selectionne = table.item(contact)['values'][7]

            # Récupérer les nouvelles valeurs des entrées
            nom = entrernom.get()
            prenom = entrerPrenom.get()
            email = entrermail.get()
            telephone = entrertelephone.get()
            adresse = entreradresse.get()
            groupe = entrergroupeC.get()

            # Obtenir la date actuelle
            date_ajout = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Mettre à jour les informations du contact dans la base de données
            con = sqlite3.connect('carnet_adresses.db')
            cuser = con.cursor()
            cuser.execute(
                "UPDATE contacts SET nom=?, prenom=?, email=?, telephone=?, adresse=?, groupe=?, date_ajout=? WHERE id = ?",
                (nom, prenom, email, telephone, adresse, groupe, date_ajout, id_selectionne))
            con.commit()
            con.close()

            # Mettre à jour la ligne existante dans la table
            table.item(contact, values=(id_selectionne, nom, prenom, email, telephone, adresse, groupe, date_ajout))

            # Effacer les entrées
            entrernom.delete(0, END)
            entrerPrenom.delete(0, END)
            entrermail.delete(0, END)
            entrertelephone.delete(0, END)
            entreradresse.delete(0, END)
            entrergroupeC.delete(0, END)

            messagebox.showinfo("Succès", "Contact modifié avec succès !!")
            # Effacer les entrées
            entrernom.delete(0, END)
            entrerPrenom.delete(0, END)
            entrermail.delete(0, END)
            entrertelephone.delete(0, END)
            entreradresse.delete(0, END)
            entrergroupeC.delete(0, END)

    def supprimer():
        idSelectionner = table.item(table.selection())['values'][0]
        con = sqlite3.connect('carnet_adresses.db')
        cuser = con.cursor()
        delete = cuser.execute("delete from contacts where id = {}".format(idSelectionner))
        con.commit()
        table.delete(table.selection())

        # Suppression des entrées
        entrernom.delete(0, END)
        entrerPrenom.delete(0, END)
        entrermail.delete(0, END)
        entrertelephone.delete(0, END)
        entreradresse.delete(0, END)
        entrergroupeC.delete(0, END)

    def rechercher_contact():
        # Récupérer les critères de recherche
        nom_recherche = entryRechercheNom.get()
        email_recherche = entryRechercheEmail.get()

        # Effacer la table
        table.delete(*table.get_children())

        # Requête de recherche dans la base de données
        con = sqlite3.connect('carnet_adresses.db')
        cuser = con.cursor()

        if nom_recherche:
            query = f"SELECT * FROM contacts WHERE nom LIKE '%{nom_recherche}%'"
        elif email_recherche:
            query = f"SELECT * FROM contacts WHERE email LIKE '%{email_recherche}%'"
        else:
            # Si aucun critère de recherche n'est spécifié, afficher tous les contacts
            query = "SELECT * FROM contacts"

        select = cuser.execute(query)

        for row in select:
            table.insert('', END, values=row)

        con.close()

    # Fonctions de tri et de filtres
    def tri_par_nom():
        # Supprimer toutes les lignes actuelles de la table
        table.delete(*table.get_children())

        # Récupérer les contacts triés par nom depuis la base de données
        con = sqlite3.connect('carnet_adresses.db')
        cuser = con.cursor()
        select = cuser.execute("SELECT * FROM contacts ORDER BY nom ASC")
        for row in select:
            table.insert('', END, values=row)
        con.close()

    def tri_par_date():
        # Supprimer toutes les lignes actuelles de la table
        table.delete(*table.get_children())

        # Récupérer les contacts triés par date d'ajout depuis la base de données
        con = sqlite3.connect('carnet_adresses.db')
        cuser = con.cursor()
        select = cuser.execute("SELECT * FROM contacts ORDER BY date_ajout ASC")
        for row in select:
            table.insert('', END, values=row)
        con.close()

    def filtre_par_groupe():
        # Supprimer toutes les lignes actuelles de la table
        table.delete(*table.get_children())

        # Récupérer les contacts filtrés par groupe depuis la base de données
        con = sqlite3.connect('carnet_adresses.db')
        cuser = con.cursor()
        groupe_recherche = entrerGroupe.get().lower()

        select = cuser.execute("SELECT * FROM contacts WHERE LOWER(groupe) = ? ORDER BY id ASC", (groupe_recherche,))
        for row in select:
            table.insert('', END, values=row)
        con.close()

    # Fonction pour exporter les contacts au format CSV
    def exporter_csv():
        try:
            # Demander à l'utilisateur où sauvegarder le fichier CSV
            fichier_csv = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Fichiers CSV", "*.csv")])

            if fichier_csv:
                # Ouvrir le fichier CSV en mode écriture
                with open(fichier_csv, mode='w', newline='', encoding='utf-8') as fichier:
                    writer = csv.writer(fichier)

                    # Écrire l'en-tête du CSV
                    writer.writerow(
                        ['ID', 'Nom', 'Prénom', 'E-mail', 'Téléphone', 'Adresse', 'Groupe', 'Date d\'ajout'])

                    # Récupérer les contacts depuis la base de données
                    con = sqlite3.connect('carnet_adresses.db')
                    cuser = con.cursor()
                    select = cuser.execute("SELECT * FROM contacts")
                    for row in select:
                        # Écrire chaque ligne de contact dans le fichier CSV
                        writer.writerow(row)

                    con.close()

                messagebox.showinfo("Exportation réussie", "Les contacts ont été exportés avec succès en format CSV.")
        except Exception as e:
            messagebox.showerror("Erreur d'exportation", f"Une erreur s'est produite lors de l'exportation : {str(e)}")

    # Fonction pour importer les contacts depuis un fichier CSV
    def importer_csv():
        try:
            # Demander à l'utilisateur de sélectionner un fichier CSV
            fichier_csv = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("Fichiers CSV", "*.csv")])

            if fichier_csv:
                # Charger le fichier CSV dans un DataFrame pandas
                df = pd.read_csv(fichier_csv)

                # Vérifier si le DataFrame a les colonnes nécessaires
                if set(['Nom', 'Prenom', 'E-mail', 'Telephone', 'Adresse', 'Groupe']).issubset(df.columns):
                    # Création de la connexion à la base de données
                    con = sqlite3.connect('carnet_adresses.db')
                    cuser = con.cursor()

                    # Parcourir chaque ligne du DataFrame et ajouter les contacts à la base de données
                    for _, row in df.iterrows():
                        nom = row['Nom']
                        prenom = row['Prenom']
                        email = row['E-mail']
                        telephone = row['Telephone']
                        adresse = row['Adresse']
                        groupe = row['Groupe']


                        # Vérifier si le contact existe déjà
                        if contact_existe(nom, prenom):
                            messagebox.showerror("Erreur d'importation",
                                                 f"Le contact {nom} {prenom} existe déjà dans la base de données.")
                            continue

                        # Convertir la date en chaîne au format ISO 8601
                        date_ajout = datetime.today().isoformat()

                        # Ajouter le contact à la base de données
                        cuser.execute(
                            "INSERT INTO contacts('nom','prenom','email','telephone','adresse', 'groupe','date_ajout','id_user') VALUES (?,?,?,?,?,?,?,?)",
                            (nom, prenom, email, telephone, adresse, groupe, date_ajout, id_user))

                    con.commit()
                    con.close()

                    # Afficher un message de réussite
                    messagebox.showinfo("Importation réussie",
                                        "Les contacts ont été importés avec succès dans la base de données.")

                    # Rafraîchir la table pour afficher les nouveaux contacts
                    table.delete(*table.get_children())
                    afficher_contacts()

                else:
                    messagebox.showerror("Erreur d'importation",
                                         "Le fichier CSV doit contenir les colonnes: Nom, Prenom, E-mail, Telephone, Adresse, Groupe.")
        except Exception as e:
            messagebox.showerror("Erreur d'importation", f"Une erreur s'est produite lors de l'importation : {str(e)}")

    def contact_existe(email, tel):
        con = sqlite3.connect('carnet_adresses.db')
        cuser = con.cursor()
        select = cuser.execute("SELECT * FROM contacts WHERE email=? OR telephone=?", (email, tel))
        contact = select.fetchone()
        con.close()
        return contact is not None


    # Ajout du titre
    lbltitre = Label(root, bd=20, relief=RIDGE, text="PyStockBook", font=("Arial", 20),
                     bg="SteelBlue",
                     fg="white")
    lbltitre.place(x=-100, y=0, width=1470)

    # Liste des contacts
    lblListeContact = Label(root, text="La liste des contacts ", font=("Arial", 16), bg="SteelBlue", fg="white")
    lblListeContact.place(x=500, y=90, width=760)

    # Largeur fixe pour chaque colonne
    label_width = 200
    entry_width = 200
    x_offset = 200  # Espace entre les labels et les entrées

    # text nom
    lblnom = Label(root, text="Nom :", font=("Arial", 16), fg="black")
    lblnom.place(x=0, y=150, width=label_width)
    entrernom = Entry(root)
    entrernom.place(x=x_offset, y=150, width=entry_width, height=30)

    # text prenom
    lblPrenom = Label(root, text="Prenom : ", font=("Arial", 16), fg="black")
    lblPrenom.place(x=0, y=200, width=label_width)
    entrerPrenom = Entry(root)
    entrerPrenom.place(x=x_offset, y=200, width=entry_width, height=30)

    # text e-mail
    lblmail = Label(root, text="E-mail : ", font=("Arial", 16), fg="black")
    lblmail.place(x=0, y=250, width=label_width)
    entrermail = Entry(root)
    entrermail.place(x=x_offset, y=250, width=entry_width, height=30)

    # text Telephone
    lbltelephone = Label(root, text="Telephone :", font=("Arial", 16), fg="black")
    lbltelephone.place(x=0, y=300, width=label_width)
    entrertelephone = Entry(root)
    entrertelephone.place(x=x_offset, y=300, width=entry_width, height=30)

    # text adresse
    lbladresse = Label(root, text="Adresse :", font=("Arial", 16), fg="black")
    lbladresse.place(x=0, y=350, width=label_width)
    entreradresse = Entry(root)
    entreradresse.place(x=x_offset, y=350, width=entry_width, height=30)

    # text groupe
    lblgroupe = Label(root, text="Groupe :", font=("Arial", 16), fg="black")
    lblgroupe.place(x=0, y=400, width=label_width)
    entrergroupeC = Entry(root)
    entrergroupeC.place(x=x_offset, y=400, width=entry_width, height=30)

    # Enregistrer
    btnenregistrer = Button(root, text="Enregistrer", font=("Arial", 16), bg="green", fg="white", command=ajouter)
    btnenregistrer.place(x=30, y=450, width=200)

    # modifier
    btnmodofier = Button(root, text="Modifier", font=("Arial", 16), bg="grey", fg="white", command=modifier)
    btnmodofier.place(x=270, y=450, width=200)

    # Supprimer
    btnSupprimer = Button(root, text="Supprimer", font=("Arial", 16), bg="red", fg="white", command=supprimer)
    btnSupprimer.place(x=150, y=500, width=200)

    # Champ de recherche par nom
    lblRechercheNom = Label(root, text="Recherche par Nom:", font=("Arial", 12), fg="black")
    lblRechercheNom.place(x=500, y=130, width=150)
    entryRechercheNom = Entry(root)
    entryRechercheNom.place(x=650, y=130, width=150, height=30)

    # Champ de recherche par email
    lblRechercheEmail = Label(root, text="Recherche par email:", font=("Arial", 12), fg="black")
    lblRechercheEmail.place(x=810, y=130, width=150)
    entryRechercheEmail = Entry(root)
    entryRechercheEmail.place(x=980, y=130, width=150, height=30)

    # Bouton de recherche
    btnRecherche = Button(root, text="Rechercher", font=("Arial", 12), bg="darkblue", fg="white",
                          command=rechercher_contact)
    btnRecherche.place(x=1150, y=130, width=100)

    # Boutons de tri
    btnTriNom = Button(root, text="Trier par Nom", font=("Arial", 12), bg="darkblue", fg="white", command=tri_par_nom)
    btnTriNom.place(x=500, y=540, width=150)

    btnTriDate = Button(root, text="Trier par Date", font=("Arial", 12), bg="darkblue", fg="white",
                        command=tri_par_date)
    btnTriDate.place(x=660, y=540, width=150)

    # Boutons de filtres avancés
    lblFiltreGroupe = Label(root, text="Filtrer par Groupe:", font=("Arial", 12), fg="black")
    lblFiltreGroupe.place(x=840, y=540, width=150)
    entrerGroupe = Entry(root)
    entrerGroupe.place(x=990, y=540, width=150, height=30)

    btnFiltreGroupe = Button(root, text="Filtrer", font=("Arial", 12), bg="darkblue", fg="white",
                             command=filtre_par_groupe)
    btnFiltreGroupe.place(x=1150, y=540, width=100)

    # Ajouter ces liaisons aux boutons correspondants
    btnExporterCSV = Button(root, text="Exporter en CSV", font=("Arial", 12), bg="darkblue", fg="white",
                            command=exporter_csv)
    btnExporterCSV.place(x=500, y=590, width=150)

    btnImporterCSV = Button(root, text="Importer depuis CSV", font=("Arial", 12), bg="darkblue", fg="white",
                            command=importer_csv)
    btnImporterCSV.place(x=670, y=590, width=200)
    # Table
    table = ttk.Treeview(root, columns=(1, 2, 3, 4, 5, 6, 7, 8), height=3, show="headings")
    table.place(x=500, y=180, width=760, height=350)

    # Associer la fonction à l'événement de relâchement du bouton gauche de la souris
    table.bind('<ButtonRelease-1>', afficher_donnees_selectionnees)

    # Headings
    table.heading(1, text="ID", anchor=CENTER)
    table.heading(2, text="NOM", anchor=CENTER)
    table.heading(3, text="PRENOM", anchor=CENTER)
    table.heading(4, text="E-MAIL", anchor=CENTER)
    table.heading(5, text="TELEPHONE", anchor=CENTER)
    table.heading(6, text="ADRESSE", anchor=CENTER)
    table.heading(7, text="GROUPE", anchor=CENTER)
    table.heading(8, text="DATE", anchor=CENTER)

    # définir les dimentions des colonnes
    table.column(1, width=50, anchor=CENTER)
    table.column(2, width=100, anchor=CENTER)
    table.column(3, width=100, anchor=CENTER)
    table.column(4, width=150, anchor=CENTER)
    table.column(5, width=150, anchor=CENTER)
    table.column(6, width=150, anchor=CENTER)
    table.column(7, width=150, anchor=CENTER)
    table.column(8, width=150, anchor=CENTER)

    # Création d'une scrollbar
    scrollbar = Scrollbar(root, orient="vertical", bg="white", command=table.yview)
    scrollbar.place(x=1240, y=185, height=340)

    # Création d'une scrollbar horizontal
    scrollbar2 = Scrollbar(root, orient="horizontal", bg="white", command=table.xview)
    scrollbar2.place(x=505, y=510, width=735)

    # Configurer la table pour utiliser la scrollbar
    table.configure(yscrollcommand=scrollbar.set, xscrollcommand=scrollbar2.set)

    # Fonction pour afficher les données dans la table contatcs
    def afficher_contacts(id_user):
        if id_user == 1:
            con = sqlite3.connect('carnet_adresses.db')
            cuser = con.cursor()
            select = cuser.execute("SELECT * FROM contacts ORDER BY id ASC", )
            for row in select:
                table.insert('', END, values=row)
        con.close()

    # Fonction pour la déconnexion
    def deconnexion():
        root.destroy()

    # Bouton de déconnexion
    btnDeconnexion = Button(root, text="Déconnexion", font=("Arial", 12), bg="orange", fg="white", command=deconnexion)
    btnDeconnexion.place(x=1150, y=590, width=100)

    # Configurer la fonction on_closing pour gérer la fermeture de la fenêtre
    def on_closing():
        # Ajoutez tout code de nettoyage ici
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # appel de la fonction
    afficher_contacts(id_user)
    root.mainloop()


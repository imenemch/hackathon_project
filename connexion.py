from tkinter import ttk, filedialog
from tkinter import *
import sqlite3
from tkinter import messagebox

root_creation_compte = Tk()
root_creation_compte.title("Formulaire de création de compte")
root_creation_compte.geometry("600x450")

def creation_compte():
    nom_user = entrernom_userC.get()
    password = entrerpassword.get()
    nom_user_confirm = entrernom_confirm_user.get()
    password_confirm = entrerpassword_confirm.get()

    # Vérifier si les champs obligatoires ne sont pas vides
    if not nom_user or not password or not nom_user_confirm or not password_confirm:
        messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
        return  # Arrêter la fonction si un champ est vide

    # Vérifier si les noms et password sont identiques
    if nom_user != nom_user_confirm or password != password_confirm:
        messagebox.showerror("Erreur", "Les noms/mots de passe ne correspondent pas")
        return  # Arrêt de la fonction

    # Création de la connexion
    con = sqlite3.connect('carnet_adresses.db')
    cuser = con.cursor()
    cuser.execute(
            "INSERT INTO users('name_user','password') VALUES (?,?)",
            (nom_user, password))

    # Récupérer l'ID de la dernière ligne insérée
    last_id = cuser.lastrowid
    con.commit()
    con.close()
    # Afficher le message d'information
    messagebox.showinfo("Succès", "Utilisateur ajouté avec succès!")

    # Effacer les entrées
    entrernom_userC.delete(0, END)
    entrernom_confirm_user.delete(0, END)
    entrerpassword.delete(0, END)
    entrerpassword_confirm.delete(0, END)


def user_existe(nom_user, password):
    con = sqlite3.connect('carnet_adresses.db')
    cuser = con.cursor()
    select = cuser.execute("SELECT * FROM users WHERE name_user=? AND password=?", (nom_user, password))
    user = select.fetchone()
    con.close()
    return user is not None

    # Vérifier si le contact existe déjà
    if user_existe(nom_user, password):
        messagebox.showerror("Erreur", "Ce contact existe déjà dans le carnet d'adresses.")
        return



# Ajout du titre
lbltitre = Label(root_creation_compte, bd=20, relief=RIDGE, text="Créer un compte", font=("Arial", 20),bg="SteelBlue",fg="white")
lbltitre.place(x=-100, y=0, width=1000)


# Largeur fixe pour chaque colonne
label_width = 200
entry_width = 200
x_offset = 200  # Espace entre les labels et les entrées
# text nom
lblnom = Label(root_creation_compte, text="Nom d'utilisateur :", font=("Arial", 16), fg="black")
lblnom.place(x=0, y=150, width=label_width)
entrernom_userC = Entry(root_creation_compte)
entrernom_userC.place(x=x_offset, y=150, width=entry_width, height=30)

# text Confirmation nom
lblnom_confirm = Label(root_creation_compte, text="Confirmer le nom :", font=("Arial", 16), fg="black")
lblnom_confirm.place(x=0, y=200, width=label_width)
entrernom_confirm_user = Entry(root_creation_compte)
entrernom_confirm_user.place(x=x_offset, y=200, width=entry_width, height=30)

# text password
lblpassword = Label(root_creation_compte, text="Mot de passe :", font=("Arial", 16), fg="black")
lblpassword.place(x=0, y=250, width=label_width)
entrerpassword = Entry(root_creation_compte)
entrerpassword.place(x=x_offset, y=250, width=entry_width, height=30)

# text password
lblpassword_confirm = Label(root_creation_compte, text=" Confirmer password :", font=("Arial", 14), fg="black")
lblpassword_confirm.place(x=0, y=300, width=label_width)
entrerpassword_confirm = Entry(root_creation_compte)
entrerpassword_confirm.place(x=x_offset, y=300, width=entry_width, height=30)

# Bouton de création
btnRecherche = Button(root_creation_compte, text="S'enregistrer", font=("Arial", 12), bg="darkblue", fg="white",
command=creation_compte)
btnRecherche.place(x=150, y=350, width=150)

root_creation_compte.mainloop()
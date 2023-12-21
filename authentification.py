from tkinter import *
import sqlite3
from tkinter import messagebox
from app import carnet_adresses

root_authen = Tk()
root_authen.title("Formulaire de création de compte")
root_authen.geometry("600x450")

def authen_user():
    nom = entrernom_userA.get()
    password = entrerpassword.get()
    # Vérifier si l'utilisateur existe dans la table users
    try:
        con = sqlite3.connect('carnet_adresses.db')
        cuser = con.cursor()
        cuser.execute("SELECT id_user FROM users WHERE name_user=? AND password=?", (nom, password))
        user_id = cuser.fetchone()
    finally:
        con.close()

    if user_id:
        # Utilisateur authentifié, vous pouvez ici ouvrir votre interface principale
        messagebox.showinfo("Authentification réussie", "Bienvenue !")
        carnet_adresses()
        # Appeler la fonction pour afficher le carnet d'adresses ou autre
    else:
        messagebox.showerror("Erreur d'authentification", "Nom d'utilisateur ou mot de passe incorrect.")



# Ajout du titre
lbltitre = Label(root_authen, bd=20, relief=RIDGE, text="Connexion", font=("Arial", 20),bg="SteelBlue",fg="white")
lbltitre.place(x=-100, y=0, width=800)

# Largeur fixe pour chaque colonne
label_width = 200
entry_width = 200
x_offset = 200  # Espace entre les labels et les entrées


# text nom
lblnom = Label(root_authen, text="Nom d'utilisateur :", font=("Arial", 16), fg="black")
lblnom.place(x=0, y=150, width=label_width)
entrernom_userA = Entry(root_authen)
entrernom_userA.place(x=x_offset, y=150, width=entry_width, height=30)

# text password
lblpassword = Label(root_authen, text="Mot de passe :", font=("Arial", 16), fg="black")
lblpassword.place(x=0, y=200, width=label_width)
entrerpassword = Entry(root_authen)
entrerpassword.place(x=x_offset, y=200, width=entry_width, height=30)

# Bouton de connexion
btnRecherche = Button(root_authen, text="Se connecter", font=("Arial", 12), bg="darkblue", fg="white",
command=authen_user)
btnRecherche.place(x=150, y=350, width=150)




root_authen.mainloop()
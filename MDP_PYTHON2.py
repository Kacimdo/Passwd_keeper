#GESTIONNAIRE DE MOT DE PASSE 
#PAR AZIZI KACI 

#importation de la bibliothèque "cryptography"
from cryptography.fernet import Fernet
import random #générer un mot de passe aléatoire
import string #récupérer les chaines de caractères dispo pour gen un passwd "solide"
from tkinter import * # interface graphique (soon)
from pystyle import * # fonction center (cli plus propre)
import os

#VARIABLE GLOBALE EN MAJ
#SI VOUS SOUHAITEZ MODIFIER LE NOM DU FICHIER REMPLACER "mot_de_passe.txt"
PASSWORD_FILE = "mot_de_passe.txt"
MASTER_FILE = "master_key.txt"
 
# 1 : création d'une clé de chiffrement secrète MASTER grâce à la fonction fernet 
# Cette fonction permet de générée une clé de chiffrement pour chiffrer les mots de passe 

def generate_key():
    return Fernet.generate_key()

# 2 : sauvegarde d'un mot de passe chifré dans un fichier binaire
def save_password(filename,site_web,password, key):
    fernet = Fernet(key)
    print(password)
    encrypted_password = fernet.encrypt(password.encode())
    print(encrypted_password)
    #en dessous le mode d'écritute "ab" écrire à la fin du fichier en mode écriture en binaire pour écrire des donnés chiffrées
    with open(filename, 'a') as file:
        #création d'un fichier 
        # on convertie la variable "encrypted_password" en string car elle est en binaire ( byte ) du à Fernet qui la génère ainsi
        file.write(site_web+":"+encrypted_password.decode("utf-8")+"\n")

# Fonction pour décrypter et récupérer un mot de passe depuis le fichier
def get_password(filename, key):
    fernet = Fernet(key)
    #pareil que au dessus 'rb' sert à lire le fichier binaire ou les données chiffrées sont présentes
    with open(filename, 'rb') as file:
        encrypted_password = file.read()

    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password

#fonction pour générer un mot de passe aléatoire de 12 caractères (MAJ,min,Caractère)
def generate_random_password(length=12):
    chaine_solide = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chaine_solide) for _ in range(length))
    return password


# AFFICHAGE CLI DU MENU + SAISIE DU CHOIX UTILISATEUR 
def menu_cli():
     print("0 - Générer votre clé unique - A NE PAS PERDRE")
     print("1 - Sauvegarder votre mot de passe")
     print("2 - Générer un mot de passe solide")
     print("3 - Visualiser les mots de passe sauvegardés")
     print("4 - Quitter ")

print(Center.XCenter(Box.Lines("GESTIONNAIRE DE MOT DE PASSE \n par KACI")))


# GESTION DES CHOIX avec while true pour ne pas exit du script après utilisation d'une commande

while True :
    menu_cli()
    reponse = input("VOTRE CHOIX :  ")
    if os.path.exists(MASTER_FILE) :
        with open(MASTER_FILE, 'r') as file:
            master_key = file.read().strip()


    if reponse == "0":
        master_key = generate_key()
        print("Votre clé unique est :", master_key)

    # Écrivez la clé dans le fichier "master_key.txt" dans le dossier courant
        with open(MASTER_FILE, 'w') as fichier_master:  # Utilisez 'wb' pour écrire en mode binaire
                fichier_master.write(master_key.decode('utf-8'))  # Décodez la clé en UTF-8 avant de l'écrire
                print("Le mot de passe à été ajouté dans le fichier du dossier courant")

    elif reponse == "1":
        site_web_mdp = input("Veuillez saisir le site web sur lequel enregister le MDP : ")

        mdp_a_save = input("Veuillez saisir le mot de passe à enregistrer: ")
        save_password("mot_de_passe.txt",site_web_mdp,mdp_a_save,master_key)
         
    elif reponse == "2":
         mdp_solide = generate_random_password()
         print("Votre mot de passe est :", mdp_solide)
#on viens ouvrir le fichier contenant les mdp 
#on viens lire ligne par ligne puis séparer les 2 valeurs en leur donnant comme nom "site" et "password"
#en prenant en compte le séparateur qui viens determiner leur ordres (quel valeur est site et laquel est password)
    elif reponse == "3":
        with open(PASSWORD_FILE, 'r') as file:
            for line in file :
                # le .split permet de supprimer le \n de la chaine de caractère lorsqu'on retourne le mdp
                site,password = line.strip().split(":") 
                decrypt_passwd = Fernet(master_key)
                mdp_clear = decrypt_passwd.decrypt(password) 
                print("site:", site,"password:",mdp_clear.decode('utf-8'))
    
    elif reponse == "4":
     exit()

    else:
        print("Option non valide. Veuillez choisir une option valide.")


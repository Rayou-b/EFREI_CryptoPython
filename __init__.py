from cryptography.fernet import Fernet
from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json

from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #Comm2

key = Fernet.generate_key()
f = Fernet(key)


@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    valeur_bytes = valeur.encode()  # Conversion str -> bytes
    token = f.encrypt(valeur_bytes)  # Encrypt la valeur
    return f"Valeur encryptée : {token.decode()}"  # Retourne le token en str

@app.route('/decrypt/<string:valeur>')
def decryptage(valeur):
    valeur_bytes = valeur.encode()  # Conversion str -> bytes
    try:
        decrypted = f.decrypt(valeur_bytes)  # Déchiffrement
        return f"Valeur décryptée : {decrypted.decode()}"  # Retourne en str
    except Exception as e:
        return f"Erreur lors du décryptage : {str(e)}"

@app.route('/generate_key')
def generate_key():
    return f"Votre clé : {Fernet.generate_key().decode()}"


@app.route('/encrypt_key/<key>/<text>')
def encrypt_with_key(key, text):
    try:
        fernet_user = Fernet(key.encode())
        token = fernet_user.encrypt(text.encode()).decode()
        return f"Valeur encryptée avec votre clé : {token}"
    except Exception as e:
        return f"Erreur : Clé invalide ? Détail : {str(e)}"


@app.route('/decrypt_key/<key>/<token>')
def decrypt_with_key(key, token):
    try:
        fernet_user = Fernet(key.encode())
        decrypted = fernet_user.decrypt(token.encode()).decode()
        return f"Valeur décryptée avec votre clé : {decrypted}"
    except Exception as e:
        return f"Erreur lors du décryptage : {str(e)}"




                                                                                                                                                     
if __name__ == "__main__":
  app.run(debug=True)

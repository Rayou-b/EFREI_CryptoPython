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

@app.route("/decrypt/<encrypted_text>")
def decrypt(encrypted_text):
    try:
        decrypted = fernet.decrypt(encrypted_text.encode()).decode()
        return {"decrypted": decrypted}
    except Exception as e:
        return {"error": "Décryptage échoué", "details": str(e)}
@app.route("/encrypt_key/<user_key>/<text>")
def encrypt_with_key(user_key, text):
    try:
        fernet_custom = Fernet(user_key.encode())
        encrypted = fernet_custom.encrypt(text.encode()).decode()
        return {"encrypted": encrypted}
    except Exception as e:
        return {"error": "Erreur de chiffrement", "details": str(e)}

@app.route("/decrypt_key/<user_key>/<encrypted_text>")
def decrypt_with_key(user_key, encrypted_text):
    try:
        fernet_custom = Fernet(user_key.encode())
        decrypted = fernet_custom.decrypt(encrypted_text.encode()).decode()
        return {"decrypted": decrypted}
    except Exception as e:
        return {"error": "Décryptage échoué", "details": str(e)}

                                                                                                                                                     
if __name__ == "__main__":
  app.run(debug=True)

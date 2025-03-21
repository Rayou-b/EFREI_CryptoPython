from cryptography.fernet import Fernet
from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

# === Fonction d'initialisation de la BDD ===
def init_db():
    if not os.path.exists("crypto.db"):
        conn = sqlite3.connect("crypto.db")
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

# === Appel de la fonction au démarrage ===
init_db()

# === ROUTES ===

@app.route('/')
def home():
    return "<h1>Bienvenue sur l'API CryptoPython 🔐</h1><p>Essayez /generate_key pour créer une clé</p>"

@app.route('/generate_key')
def generate_key():
    new_key = Fernet.generate_key().decode()

    # Enregistrer la clé dans la BDD
    conn = sqlite3.connect("crypto.db")
    c = conn.cursor()
    c.execute("INSERT INTO keys (key) VALUES (?)", (new_key,))
    conn.commit()
    conn.close()

    return render_template("generate_key.html", key=new_key)

@app.route('/encrypt/<string:key>/<string:message>')
def encrypt_message(key, message):
    try:
        key_bytes = key.encode()
        f = Fernet(key_bytes)
        encrypted = f.encrypt(message.encode())
        return encrypted.decode()
    except Exception as e:
        return f"Erreur : {str(e)}"

@app.route('/decrypt/<string:key>/<string:token>')
def decrypt_message(key, token):
    try:
        key_bytes = key.encode()
        f = Fernet(key_bytes)
        decrypted = f.decrypt(token.encode())
        return decrypted.decode()
    except Exception as e:
        return f"Erreur : {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)

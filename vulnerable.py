import sqlite3
import subprocess
import os

# 1. Secret en dur (Sera détecté par p/secrets)
AWS_SECRET_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
GITHUB_API_TOKEN = "ghp_xYzAbCdEfGhIjKlMnOpQrStUvWxYz123456"

def get_user(username):
    """2. Injection SQL (Sera détecté par p/security-audit)"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # DANGER : Concaténation directe de l'entrée utilisateur dans la requête SQL
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    
    return cursor.fetchall()

def ping_server(ip_address):
    """3. Injection de commande (Sera détecté par p/security-audit)"""
    # DANGER : Exécution d'une commande shell avec une variable non nettoyée
    command = "ping -c 1 " + ip_address
    subprocess.call(command, shell=True)

def calculate_discount(user_formula):
    """4. Utilisation dangereuse de eval() (Sera détecté par p/default)"""
    # DANGER : Évaluation directe de code arbitraire
    return eval(user_formula)

"""
Vues volontairement vulnérables — mappées sur l'OWASP Top 10 2021.
Chaque fonction illustre UNE faille ciblée par les règles Semgrep (p/owasp-top-ten, p/django).
Ce fichier ne tourne jamais réellement, il sert uniquement de cible de scan SAST.
"""
import hashlib
import os
import pickle
import random
import subprocess

import requests
import yaml
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import Template, Context
from django.utils.safestring import mark_safe

from vulnapp.settings import JWT_SIGNING_SECRET


# --- A03:2021 Injection — SQL Injection (CWE-89) ---
def search_users(request):
    username = request.GET.get("username")
    query = "SELECT * FROM users WHERE username = '%s'" % username  # concat directe
    with connection.cursor() as cursor:
        cursor.execute(query)
    return HttpResponse(cursor.fetchall())


# --- A10:2021 SSRF (CWE-918) ---
def ping_host(request):
    url = request.GET.get("url")
    response = requests.get(url)  # URL 100% contrôlée par l'utilisateur, aucune allowlist
    return HttpResponse(response.content)


# --- A03:2021 Injection — Command Injection (CWE-78) ---
def run_command(request):
    hostname = request.GET.get("host")
    os.system("ping -c 1 " + hostname)  # injection shell directe
    subprocess.call(f"traceroute {hostname}", shell=True)  # idem, shell=True
    return HttpResponse("done")


# --- A01:2021 Broken Access Control — Path Traversal (CWE-22) ---
def read_file(request):
    filename = request.GET.get("name")
    path = "/var/app/uploads/" + filename  # pas de sanitization, ../../etc/passwd possible
    with open(path) as f:
        return HttpResponse(f.read())


# --- A03:2021 Injection — Cross-Site Scripting (CWE-79) ---
def render_profile(request):
    bio = request.GET.get("bio")
    html = "<div class='bio'>" + bio + "</div>"
    return HttpResponse(mark_safe(html))  # contournement volontaire de l'auto-escaping


# --- A08:2021 Software and Data Integrity Failures — Insecure Deserialization (CWE-502) ---
def import_config(request):
    raw = request.body
    data = pickle.loads(raw)  # désérialisation non fiable -> RCE potentielle
    config = yaml.load(request.POST.get("yaml_payload"), Loader=yaml.Loader)  # idem via YAML
    return HttpResponse(str(data) + str(config))


# --- A01:2021 Broken Access Control — Open Redirect (CWE-601) ---
def go_to(request):
    next_url = request.GET.get("next")
    return redirect(next_url)  # pas de validation de domaine


# --- A02:2021 Cryptographic Failures — Weak Hash / Insecure Randomness (CWE-327, CWE-330) ---
def generate_token(request):
    seed = str(random.random())  # PRNG non cryptographique pour un token de sécurité
    token = hashlib.md5(seed.encode()).hexdigest()  # MD5 = faible, cassable
    return HttpResponse(token)


# --- A07:2021 Identification & Auth Failures — JWT mal validé (CWE-347) ---
def login_view(request):
    import jwt

    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    payload = jwt.decode(token, JWT_SIGNING_SECRET, algorithms=["none", "HS256"])  # alg "none" acceptée
    return HttpResponse(str(payload))


# --- A08:2021 — Zip Slip (CWE-22 via archive) ---
def extract_upload(request):
    import zipfile

    uploaded = request.FILES["archive"]
    with zipfile.ZipFile(uploaded) as zf:
        zf.extractall("/tmp/uploads")  # aucune vérification des chemins dans l'archive
    return HttpResponse("extracted")


# --- A03:2021 Injection — Server-Side Template Injection (CWE-1336) ---
def render_template(request):
    tpl = request.GET.get("tpl")
    rendered = Template(tpl).render(Context({}))  # template contrôlé par l'utilisateur
    return HttpResponse(rendered)


# --- A03:2021 Injection — Code Injection via eval/exec (CWE-95) ---
def eval_expression(request):
    expr = request.GET.get("expr")
    result = eval(expr)  # exécution de code arbitraire
    exec(request.GET.get("code", "pass"))
    return HttpResponse(str(result))

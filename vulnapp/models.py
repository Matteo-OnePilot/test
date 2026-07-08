"""
Modèle avec requête brute vulnérable — illustre l'injection SQL via .raw() / .extra().
"""
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField()
    # --- CWE-798 : mot de passe stocké en clair, pas de hashing ---
    password_plaintext = models.CharField(max_length=255, default="changeme123")

    @classmethod
    def find_by_email_unsafe(cls, email):
        # A03:2021 — Injection SQL via .raw() avec f-string
        return cls.objects.raw(f"SELECT * FROM vulnapp_user WHERE email = '{email}'")

    @classmethod
    def search_unsafe(cls, term):
        # A03:2021 — Injection SQL via .extra()
        return cls.objects.extra(where=[f"username LIKE '%{term}%'"])

"""
Fichier de settings volontairement non sécurisé.
Objectif : faire remonter les règles "Security Misconfiguration" (OWASP A05:2021)
et "Cryptographic Failures" (OWASP A02:2021) des scanners SAST (Semgrep p/django, p/secrets).
"""

# --- CWE-798 : Use of Hard-coded Credentials ---
SECRET_KEY = "django-insecure-9f3a1c8e0b2d4f6a8c1e3b5d7f9a1c3e5b7d9f1a3c5e7b9d"

DEBUG = True  # CWE-489 : Active Debug Code — ne doit jamais être True en prod

ALLOWED_HOSTS = ["*"]  # Security Misconfiguration : accepte n'importe quel Host header

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "vulnapp",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
]

# --- CWE-798 : credentials DB en dur ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "prod_db",
        "USER": "admin",
        "PASSWORD": "SuperSecret123!",
        "HOST": "prod-db.internal.onepilot.co",
        "PORT": "5432",
    }
}

# --- CORS totalement ouvert (A05:2021) ---
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# --- Cookies non sécurisés (A02:2021) ---
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = False

# --- CWE-798 : clés tierces en dur (valeurs factices, format réaliste) ---
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
STRIPE_SECRET_KEY = "REDACTED-stripe-secret-key-0000000000000000000000"
JWT_SIGNING_SECRET = "s3cr3t-jwt-key-do-not-share"

SLACK_WEBHOOK_URL = "https://hooks.example-chat.test/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"

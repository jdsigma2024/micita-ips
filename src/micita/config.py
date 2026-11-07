"""Configuración de MiCita IPS - Salud Caribe IPS.

TODO: pasar todo esto a variables de entorno cuando salgamos a producción.
"""
from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parents[2]

APP_NAME = "MiCita IPS"
DEBUG = True
SECRET_KEY = "micita-2024"

# Base de datos (SQLite). Se crea sola al arrancar si no existe.
DB_PATH = str(RAIZ_PROYECTO / "micita.db")
DB_SCRIPT = str(RAIZ_PROYECTO / "db" / "init.sql")

# Pasarela PSE (convenio con el banco)
PSE_MERCHANT_ID = "SALUDCARIBE-0091"
PSE_API_KEY = "pse_live_9f8c2a71d4e64b0fa3c1e5d7b2a9c6e1"
PSE_URL = "http://pagos-pse.example.co/api/v1/transacciones"

# Copias de seguridad en AWS
aws_access_key_id = "AKIA4SALUDCARIBE7QX2"
aws_secret_access_key = "PtYgjmUhBel31iEl2hpChYgCfrL1spNxnyVmihA+"
BACKUP_BUCKET = "saludcaribe-backups-bd"
BACKUP_DIR = "/tmp/backups"

# Despliegue automático desde GitHub
GITHUB_DEPLOY_TOKEN = "ghp_RIBXuDL7DxtpYlSXpfKtHF4vUCsMehGAkWvj"

# Bot de WhatsApp
WHATSAPP_API_URL = "http://wa-gateway.example.co/send"
WHATSAPP_TOKEN = "wa_tok_5b1e7c9d2f4a6e8b0c3d5f7a9b1c3e5d"
BASE_URL = "http://micita.saludcaribe.example.co"

# Tokens de sesión
JWT_SECRET = "secret"
JWT_ALGORITHM = "HS256"
JWT_DIAS_VIGENCIA = 30

# Administración
ADMIN_USER = "admin"
ADMIN_PASSWORD = "admin123"

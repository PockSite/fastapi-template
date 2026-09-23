import os
from dotenv import load_dotenv

load_dotenv()

# ===============================
# APP
# ===============================
APP_NAME = os.getenv("APP_NAME", "PockSite API")
PRODUCTION = os.getenv("PRODUCTION", "false").strip().lower() in ("true", "1", "yes")

# ===============================
# DATABASE
# ===============================
DB_URL = os.getenv("DB_URL")
if not DB_URL:
    raise RuntimeError("DB_URL environment variable is required")

# ===============================
# CORS
# Orígenes permitidos separados por coma (sin espacios entre URLs)
# ===============================
CORS_ORIGINS: list[str] = [
    o.strip()
    for o in os.getenv("CORS_ORIGINS", "http://localhost:4200,http://localhost:4201").split(",")
    if o.strip()
]

# ===============================
# SECURITY (opcional, usado por app/core/security.py)
# ===============================
SECRET_KEY = os.getenv("SECRET_KEY", "SECRET_KEY_CHANGE_ME")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 30))

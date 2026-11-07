from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "clave_secreta_super_segura_para_nexus_erp"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def obtener_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verificar_password(password_plain: str, password_hash: str) -> bool:
    return pwd_context.verify(password_plain, password_hash)

def crear_token_acceso(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.timezone() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    token_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt
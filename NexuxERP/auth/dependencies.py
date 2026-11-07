from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from database.models import Usuario
from auth.security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_usuario_actual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Usuario:
    credentials_exeption = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se validaron las credenciales de acceso",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exeption
    except JWTError:
        raise credentials_exeption

    usuario = db.query(Usuario).filter(Usuario.username == username).first()
    if usuario is None:
        raise credentials_exeption

    return usuario
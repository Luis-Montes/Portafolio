# Establece la comunicacion entre python con el servidor de sql server
from sqlalchemy import create_engine
# Crea la base de datos y las tablas en el servidor de sql server
from sqlalchemy.orm import declarative_base
# Abre y cierra las sesiones para las acciones de guardado, eliminacion y actualizacion de datos
from sqlalchemy.orm import sessionmaker

SERVER = "localhost"
DATABASE = "NexusERP"

# 'trusted_connection=yes' le indica que usará tu autenticación de Windows (sin necesidad de usuario y contraseña de SQL)
DATABASE_URL = f"mssql+pyodbc://@{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
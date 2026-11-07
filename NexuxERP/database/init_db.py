from database.connection import engine, Base
from database.models import Usuario, Producto  # Importamos los modelos para que SQLAlchemy los detecte

def inicializar_base_datos():
    print("Conectando con SQL Server para verificar y crear tablas...")
    
    # Esta línea analiza qué tablas existen y cuáles faltan en tu BD
    Base.metadata.create_all(bind=engine)
    
    print("¡Proceso finalizado! Las tablas están listas en la base de datos.")

if __name__ == "__main__":
    inicializar_base_datos()
"""
Configuração do banco de dados
"""
import os
import pymysql
pymysql.install_as_MySQLdb()  # Permite que PyMySQL seja usado como MySQLdb

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base

# Configuração do banco de dados
DB_HOST = os.getenv('DB_HOST', 'db')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'consultamedica')
DB_USER = os.getenv('DB_USER', 'user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'userpassword')

DATABASE_URL = os.getenv('DATABASE_URL', f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# Criar engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=False)

# Criar sessão
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def init_db():
    """Inicializa o banco de dados criando todas as tabelas"""
    Base.metadata.create_all(bind=engine)
    print("Banco de dados inicializado!")

def get_db():
    """Retorna uma sessão do banco de dados"""
    db = SessionLocal()
    try:
        return db
    except Exception as e:
        db.close()
        raise e

def close_db():
    """Fecha a sessão do banco de dados"""
    SessionLocal.remove()
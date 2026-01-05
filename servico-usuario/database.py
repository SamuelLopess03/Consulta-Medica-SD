"""
Configuração do banco de dados
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base

# Configuração do banco de dados
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@db:5432/medical_system')

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
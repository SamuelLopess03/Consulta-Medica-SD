"""
Modelos de dados para o Serviço de Usuários
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class UserRole(enum.Enum):
    """Tipos de usuários do sistema"""
    PATIENT = "paciente"
    DOCTOR = "medico"
    RECEPTIONIST = "recepcionista"
    ADMIN = "administrador"

class User(Base):
    """Modelo de Usuário"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    phone = Column(String(15))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    active = Column(Integer, default=1)  # 1 = ativo, 0 = inativo
    
    # Campos específicos para médicos
    crm = Column(String(20))
    specialty = Column(String(100))
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'name': self.name,
            'cpf': self.cpf,
            'email': self.email,
            'role': self.role.value if isinstance(self.role, UserRole) else self.role,
            'phone': self.phone,
            'crm': self.crm,
            'specialty': self.specialty,
            'active': bool(self.active),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
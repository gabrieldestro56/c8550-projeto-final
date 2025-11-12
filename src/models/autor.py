"""
Modelo de Autor
"""
from sqlalchemy import Column, String, Date
from sqlalchemy.orm import relationship
from typing import Optional, TYPE_CHECKING
from datetime import date

from src.database.base import BaseModel

if TYPE_CHECKING:
    from src.models.livro import Livro


class Autor(BaseModel):
    """Modelo representando um autor de livro"""
    
    __tablename__ = "autores"
    
    nome = Column(String(200), nullable=False, index=True)
    nacionalidade = Column(String(100), nullable=True)
    data_nascimento = Column(Date, nullable=True)
    biografia = Column(String(1000), nullable=True)
    
    # Relacionamento com livros
    livros = relationship("Livro", back_populates="autor", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Autor(id={self.id}, nome='{self.nome}')>"
    
    def idade(self) -> Optional[int]:
        """
        Calcula a idade do autor
        
        Returns:
            Idade em anos ou None se data_nascimento não estiver definida
        """
        if not self.data_nascimento:
            return None
        
        hoje = date.today()
        idade = hoje.year - self.data_nascimento.year
        
        if (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day):
            idade -= 1
        
        return idade


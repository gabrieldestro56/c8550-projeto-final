"""
Modelo de Categoria
"""
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING

from src.database.base import BaseModel

if TYPE_CHECKING:
    from src.models.livro import Livro


class Categoria(BaseModel):
    """Modelo representando uma categoria de livro"""
    
    __tablename__ = "categorias"
    
    nome = Column(String(100), unique=True, nullable=False, index=True)
    descricao = Column(Text, nullable=True)
    
    # Relacionamento com livros
    livros = relationship("Livro", back_populates="categoria", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Categoria(id={self.id}, nome='{self.nome}')>"


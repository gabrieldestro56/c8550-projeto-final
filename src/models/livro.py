"""
Modelo de Livro
"""
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Text, Numeric
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING

from src.database.base import BaseModel

if TYPE_CHECKING:
    from src.models.autor import Autor
    from src.models.categoria import Categoria
    from src.models.emprestimo import Emprestimo


class Livro(BaseModel):
    """Modelo representando um livro"""
    
    __tablename__ = "livros"
    
    titulo = Column(String(300), nullable=False, index=True)
    ano_publicacao = Column(Integer, nullable=True)
    editora = Column(String(200), nullable=True)
    numero_paginas = Column(Integer, nullable=True)
    sinopse = Column(Text, nullable=True)
    preco = Column(Numeric(10, 2), nullable=True)
    disponivel = Column(Boolean, default=True, nullable=False)
    quantidade_total = Column(Integer, default=1, nullable=False)
    quantidade_disponivel = Column(Integer, default=1, nullable=False)
    
    # Chaves estrangeiras
    autor_id = Column(Integer, ForeignKey("autores.id"), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=True)
    
    # Relacionamentos
    autor = relationship("Autor", back_populates="livros")
    categoria = relationship("Categoria", back_populates="livros")
    emprestimos = relationship("Emprestimo", back_populates="livro", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Livro(id={self.id}, titulo='{self.titulo}')>"
    
    def esta_disponivel(self) -> bool:
        """
        Verifica se o livro está disponível para empréstimo
        
        Returns:
            True se disponível, False caso contrário
        """
        return self.disponivel and self.quantidade_disponivel > 0
    
    def emprestar(self) -> bool:
        """
        Marca um exemplar do livro como emprestado
        
        Returns:
            True se conseguiu emprestar, False caso contrário
        """
        if self.esta_disponivel():
            self.quantidade_disponivel -= 1
            if self.quantidade_disponivel == 0:
                self.disponivel = False
            return True
        return False
    
    def devolver(self) -> None:
        """
        Marca um exemplar do livro como devolvido
        """
        if self.quantidade_disponivel < self.quantidade_total:
            self.quantidade_disponivel += 1
            self.disponivel = True


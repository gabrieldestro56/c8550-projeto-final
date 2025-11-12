"""
Modelo de Usuário
"""
from sqlalchemy import Column, String, Date, Integer, Boolean
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING
from datetime import date

from src.database.base import BaseModel

if TYPE_CHECKING:
    from src.models.emprestimo import Emprestimo


class Usuario(BaseModel):
    """Modelo representando um usuário da biblioteca"""
    
    __tablename__ = "usuarios"
    
    nome = Column(String(200), nullable=False, index=True)
    email = Column(String(200), unique=True, nullable=False, index=True)
    data_nascimento = Column(Date, nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)
    
    # Relacionamento com empréstimos
    emprestimos = relationship("Emprestimo", back_populates="usuario", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Usuario(id={self.id}, nome='{self.nome}', email='{self.email}')>"
    
    def idade(self) -> int:
        """
        Calcula a idade do usuário
        
        Returns:
            Idade em anos
        """
        hoje = date.today()
        idade = hoje.year - self.data_nascimento.year
        
        if (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day):
            idade -= 1
        
        return idade
    
    def pode_emprestar(self, max_emprestimos: int = 5) -> bool:
        """
        Verifica se o usuário pode fazer novos empréstimos
        
        Args:
            max_emprestimos: Número máximo de empréstimos permitidos
        
        Returns:
            True se pode emprestar, False caso contrário
        """
        if not self.ativo:
            return False
        
        emprestimos_ativos = sum(1 for emp in self.emprestimos if not emp.devolvido)
        return emprestimos_ativos < max_emprestimos


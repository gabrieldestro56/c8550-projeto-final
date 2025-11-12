"""
Modelo de Empréstimo
"""
from sqlalchemy import Column, Integer, ForeignKey, Date, Boolean, Numeric
from sqlalchemy.orm import relationship
from typing import Optional, TYPE_CHECKING
from datetime import date, timedelta

from src.database.base import BaseModel

if TYPE_CHECKING:
    from src.models.livro import Livro
    from src.models.usuario import Usuario


class Emprestimo(BaseModel):
    """Modelo representando um empréstimo de livro"""
    
    __tablename__ = "emprestimos"
    
    data_emprestimo = Column(Date, nullable=False, default=date.today)
    data_prevista_devolucao = Column(Date, nullable=False)
    data_devolucao = Column(Date, nullable=True)
    devolvido = Column(Boolean, default=False, nullable=False)
    multa = Column(Numeric(10, 2), default=0.0, nullable=False)
    
    # Chaves estrangeiras
    livro_id = Column(Integer, ForeignKey("livros.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    
    # Relacionamentos
    livro = relationship("Livro", back_populates="emprestimos")
    usuario = relationship("Usuario", back_populates="emprestimos")
    
    def __repr__(self) -> str:
        return f"<Emprestimo(id={self.id}, livro_id={self.livro_id}, usuario_id={self.usuario_id}, devolvido={self.devolvido})>"
    
    def esta_atrasado(self) -> bool:
        """
        Verifica se o empréstimo está atrasado
        
        Returns:
            True se atrasado, False caso contrário
        """
        if self.devolvido:
            return False
        
        hoje = date.today()
        return hoje > self.data_prevista_devolucao
    
    def dias_atraso(self) -> int:
        """
        Calcula o número de dias de atraso
        
        Returns:
            Número de dias de atraso (0 se não estiver atrasado)
        """
        if not self.esta_atrasado():
            return 0
        
        hoje = date.today()
        return (hoje - self.data_prevista_devolucao).days
    
    def calcular_multa(self, multa_diaria: float = 2.50) -> float:
        """
        Calcula a multa baseada nos dias de atraso
        
        Args:
            multa_diaria: Valor da multa por dia de atraso
        
        Returns:
            Valor total da multa
        """
        dias = self.dias_atraso()
        return float(dias * multa_diaria)
    
    def devolver_emprestimo(self, multa_diaria: float = 2.50) -> None:
        """
        Marca o empréstimo como devolvido e calcula multa se houver
        
        Args:
            multa_diaria: Valor da multa por dia de atraso
        """
        # Calcula multa ANTES de marcar como devolvido (para verificar atraso corretamente)
        if self.esta_atrasado():
            self.multa = self.calcular_multa(multa_diaria)
        else:
            self.multa = 0.0
        
        self.devolvido = True
        self.data_devolucao = date.today()
        
        # Devolve o livro
        if self.livro:
            self.livro.devolver()


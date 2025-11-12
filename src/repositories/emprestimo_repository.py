"""
Repositório para Emprestimo
"""
from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session

from src.models.emprestimo import Emprestimo
from src.repositories.base_repository import BaseRepository


class IEmprestimoRepository:
    """Interface do repositório de empréstimos"""
    
    def buscar_por_usuario(self, usuario_id: int) -> List[Emprestimo]:
        """Busca empréstimos por usuário"""
        pass
    
    def buscar_por_livro(self, livro_id: int) -> List[Emprestimo]:
        """Busca empréstimos por livro"""
        pass
    
    def buscar_ativos(self) -> List[Emprestimo]:
        """Busca empréstimos ativos (não devolvidos)"""
        pass
    
    def buscar_atrasados(self) -> List[Emprestimo]:
        """Busca empréstimos atrasados"""
        pass
    
    def buscar_por_usuario_ativos(self, usuario_id: int) -> List[Emprestimo]:
        """Busca empréstimos ativos de um usuário"""
        pass


class EmprestimoRepository(BaseRepository[Emprestimo], IEmprestimoRepository):
    """Implementação do repositório de empréstimos"""
    
    def __init__(self, session: Session) -> None:
        """Inicializa o repositório"""
        super().__init__(session, Emprestimo)
    
    def buscar_por_usuario(self, usuario_id: int) -> List[Emprestimo]:
        """Busca empréstimos por usuário"""
        return self.session.query(Emprestimo).filter(Emprestimo.usuario_id == usuario_id).all()
    
    def buscar_por_livro(self, livro_id: int) -> List[Emprestimo]:
        """Busca empréstimos por livro"""
        return self.session.query(Emprestimo).filter(Emprestimo.livro_id == livro_id).all()
    
    def buscar_ativos(self) -> List[Emprestimo]:
        """Busca empréstimos ativos (não devolvidos)"""
        return self.session.query(Emprestimo).filter(Emprestimo.devolvido == False).all()
    
    def buscar_atrasados(self) -> List[Emprestimo]:
        """Busca empréstimos atrasados"""
        hoje = date.today()
        return self.session.query(Emprestimo).filter(
            Emprestimo.devolvido == False,
            Emprestimo.data_prevista_devolucao < hoje
        ).all()
    
    def buscar_por_usuario_ativos(self, usuario_id: int) -> List[Emprestimo]:
        """Busca empréstimos ativos de um usuário"""
        return self.session.query(Emprestimo).filter(
            Emprestimo.usuario_id == usuario_id,
            Emprestimo.devolvido == False
        ).all()


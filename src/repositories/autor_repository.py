"""
Repositório para Autor
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from src.models.autor import Autor
from src.repositories.base_repository import BaseRepository


class IAutorRepository:
    """Interface do repositório de autores"""
    
    def buscar_por_nome(self, nome: str) -> List[Autor]:
        """Busca autores por nome"""
        pass


class AutorRepository(BaseRepository[Autor], IAutorRepository):
    """Implementação do repositório de autores"""
    
    def __init__(self, session: Session) -> None:
        """Inicializa o repositório"""
        super().__init__(session, Autor)
    
    def buscar_por_nome(self, nome: str) -> List[Autor]:
        """Busca autores por nome (busca parcial)"""
        return self.session.query(Autor).filter(Autor.nome.like(f"%{nome}%")).all()


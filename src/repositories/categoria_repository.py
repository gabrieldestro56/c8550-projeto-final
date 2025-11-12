"""
Repositório para Categoria
"""
from typing import Optional
from sqlalchemy.orm import Session

from src.models.categoria import Categoria
from src.repositories.base_repository import BaseRepository


class ICategoriaRepository:
    """Interface do repositório de categorias"""
    
    def buscar_por_nome(self, nome: str) -> Optional[Categoria]:
        """Busca categoria por nome"""
        pass


class CategoriaRepository(BaseRepository[Categoria], ICategoriaRepository):
    """Implementação do repositório de categorias"""
    
    def __init__(self, session: Session) -> None:
        """Inicializa o repositório"""
        super().__init__(session, Categoria)
    
    def buscar_por_nome(self, nome: str) -> Optional[Categoria]:
        """Busca categoria por nome"""
        return self.session.query(Categoria).filter(Categoria.nome == nome).first()


"""
Repositório para Livro
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from src.models.livro import Livro
from src.repositories.base_repository import BaseRepository


class ILivroRepository:
    """Interface do repositório de livros"""
    
    def buscar_por_titulo(self, titulo: str) -> Optional[Livro]:
        """Busca livro por título"""
        pass
    
    def buscar_disponiveis(self) -> List[Livro]:
        """Busca livros disponíveis"""
        pass
    
    def buscar_por_autor(self, autor_id: int) -> List[Livro]:
        """Busca livros por autor"""
        pass
    
    def buscar_por_categoria(self, categoria_id: int) -> List[Livro]:
        """Busca livros por categoria"""
        pass


class LivroRepository(BaseRepository[Livro], ILivroRepository):
    """Implementação do repositório de livros"""
    
    def __init__(self, session: Session) -> None:
        """Inicializa o repositório"""
        super().__init__(session, Livro)
    
    def buscar_por_titulo(self, titulo: str) -> Optional[Livro]:
        """Busca livro por título"""
        return self.session.query(Livro).filter(Livro.titulo == titulo).first()
    
    def buscar_disponiveis(self) -> List[Livro]:
        """Busca livros disponíveis"""
        return self.session.query(Livro).filter(Livro.disponivel == True).all()
    
    def buscar_por_autor(self, autor_id: int) -> List[Livro]:
        """Busca livros por autor"""
        return self.session.query(Livro).filter(Livro.autor_id == autor_id).all()
    
    def buscar_por_categoria(self, categoria_id: int) -> List[Livro]:
        """Busca livros por categoria"""
        return self.session.query(Livro).filter(Livro.categoria_id == categoria_id).all()


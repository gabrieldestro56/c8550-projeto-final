"""
Repositório para Usuario
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from src.models.usuario import Usuario
from src.repositories.base_repository import BaseRepository


class IUsuarioRepository:
    """Interface do repositório de usuários"""
    
    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        """Busca usuário por email"""
        pass
    
    def buscar_ativos(self) -> List[Usuario]:
        """Busca usuários ativos"""
        pass


class UsuarioRepository(BaseRepository[Usuario], IUsuarioRepository):
    """Implementação do repositório de usuários"""
    
    def __init__(self, session: Session) -> None:
        """Inicializa o repositório"""
        super().__init__(session, Usuario)
    
    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        """Busca usuário por email"""
        return self.session.query(Usuario).filter(Usuario.email == email).first()
    
    def buscar_ativos(self) -> List[Usuario]:
        """Busca usuários ativos"""
        return self.session.query(Usuario).filter(Usuario.ativo == True).all()


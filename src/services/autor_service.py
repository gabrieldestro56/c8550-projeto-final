"""
Serviço de Autor
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from src.models.autor import Autor
from src.repositories.autor_repository import AutorRepository
from src.exceptions.biblioteca_exceptions import EntidadeNaoEncontradaException
from src.utils.logger import get_logger


class AutorService:
    """Serviço para gerenciar autores"""
    
    def __init__(self, session: Session, autor_repo: Optional[AutorRepository] = None) -> None:
        """
        Inicializa o serviço
        
        Args:
            session: Sessão do banco de dados
            autor_repo: Repositório de autores (opcional)
        """
        self.session = session
        self.autor_repo = autor_repo or AutorRepository(session)
        self.logger = get_logger("AutorService")
    
    def criar_autor(self, autor: Autor) -> Autor:
        """Cria um novo autor"""
        self.logger.info(f"Criando autor: {autor.nome}")
        autor = self.autor_repo.criar(autor)
        self.logger.info(f"Autor criado com sucesso: ID {autor.id}")
        return autor
    
    def buscar_por_id(self, autor_id: int) -> Autor:
        """Busca autor por ID"""
        autor = self.autor_repo.buscar_por_id(autor_id)
        if not autor:
            raise EntidadeNaoEncontradaException("Autor", str(autor_id))
        return autor
    
    def listar_todos(self, skip: int = 0, limit: int = 100) -> List[Autor]:
        """Lista todos os autores"""
        return self.autor_repo.listar_todos(skip, limit)
    
    def atualizar_autor(self, autor_id: int, dados_atualizacao: dict) -> Autor:
        """Atualiza um autor"""
        autor = self.buscar_por_id(autor_id)
        for campo, valor in dados_atualizacao.items():
            if hasattr(autor, campo):
                setattr(autor, campo, valor)
        return self.autor_repo.atualizar(autor)
    
    def deletar_autor(self, autor_id: int) -> bool:
        """Deleta um autor"""
        self.buscar_por_id(autor_id)
        return self.autor_repo.deletar(autor_id)
    
    def buscar_por_nome(self, nome: str) -> List[Autor]:
        """Busca autores por nome"""
        return self.autor_repo.buscar_por_nome(nome)


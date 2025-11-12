"""
Serviço de Categoria
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from src.models.categoria import Categoria
from src.repositories.categoria_repository import CategoriaRepository
from src.exceptions.biblioteca_exceptions import EntidadeNaoEncontradaException
from src.utils.logger import get_logger


class CategoriaService:
    """Serviço para gerenciar categorias"""
    
    def __init__(self, session: Session, categoria_repo: Optional[CategoriaRepository] = None) -> None:
        """
        Inicializa o serviço
        
        Args:
            session: Sessão do banco de dados
            categoria_repo: Repositório de categorias (opcional)
        """
        self.session = session
        self.categoria_repo = categoria_repo or CategoriaRepository(session)
        self.logger = get_logger("CategoriaService")
    
    def criar_categoria(self, categoria: Categoria) -> Categoria:
        """Cria uma nova categoria"""
        self.logger.info(f"Criando categoria: {categoria.nome}")
        categoria = self.categoria_repo.criar(categoria)
        self.logger.info(f"Categoria criada com sucesso: ID {categoria.id}")
        return categoria
    
    def buscar_por_id(self, categoria_id: int) -> Categoria:
        """Busca categoria por ID"""
        categoria = self.categoria_repo.buscar_por_id(categoria_id)
        if not categoria:
            raise EntidadeNaoEncontradaException("Categoria", str(categoria_id))
        return categoria
    
    def listar_todos(self, skip: int = 0, limit: int = 100) -> List[Categoria]:
        """Lista todas as categorias"""
        return self.categoria_repo.listar_todos(skip, limit)
    
    def atualizar_categoria(self, categoria_id: int, dados_atualizacao: dict) -> Categoria:
        """Atualiza uma categoria"""
        categoria = self.buscar_por_id(categoria_id)
        for campo, valor in dados_atualizacao.items():
            if hasattr(categoria, campo):
                setattr(categoria, campo, valor)
        return self.categoria_repo.atualizar(categoria)
    
    def deletar_categoria(self, categoria_id: int) -> bool:
        """Deleta uma categoria"""
        self.buscar_por_id(categoria_id)
        return self.categoria_repo.deletar(categoria_id)
    
    def buscar_por_nome(self, nome: str) -> Categoria:
        """Busca categoria por nome"""
        categoria = self.categoria_repo.buscar_por_nome(nome)
        if not categoria:
            raise EntidadeNaoEncontradaException("Categoria", nome)
        return categoria


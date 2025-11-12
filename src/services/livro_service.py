"""
Serviço de Livro
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from src.models.livro import Livro
from src.repositories.livro_repository import LivroRepository, ILivroRepository
from src.repositories.autor_repository import AutorRepository
from src.repositories.categoria_repository import CategoriaRepository
from src.exceptions.biblioteca_exceptions import EntidadeNaoEncontradaException, ValidacaoException
from src.validators.validators import Validator
from src.utils.logger import get_logger


class LivroService:
    """Serviço para gerenciar livros"""
    
    def __init__(
        self,
        session: Session,
        livro_repo: Optional[ILivroRepository] = None,
        autor_repo: Optional[AutorRepository] = None,
        categoria_repo: Optional[CategoriaRepository] = None
    ) -> None:
        """
        Inicializa o serviço com injeção de dependências
        
        Args:
            session: Sessão do banco de dados
            livro_repo: Repositório de livros (opcional, cria padrão se não fornecido)
            autor_repo: Repositório de autores (opcional)
            categoria_repo: Repositório de categorias (opcional)
        """
        self.session = session
        self.livro_repo = livro_repo or LivroRepository(session)
        self.autor_repo = autor_repo or AutorRepository(session)
        self.categoria_repo = categoria_repo or CategoriaRepository(session)
        self.logger = get_logger("LivroService")
    
    def criar_livro(self, livro: Livro) -> Livro:
        """
        Cria um novo livro com validações
        
        Args:
            livro: Livro a ser criado
        
        Returns:
            Livro criado
        
        Raises:
            ValidacaoException: Se validações falharem
            EntidadeNaoEncontradaException: Se autor ou categoria não existirem
        """
        self.logger.info(f"Criando livro: {livro.titulo}")
        
        
        # Valida autor
        autor = self.autor_repo.buscar_por_id(livro.autor_id)
        if not autor:
            raise EntidadeNaoEncontradaException("Autor", str(livro.autor_id))
        
        # Valida categoria se fornecida
        if livro.categoria_id:
            categoria = self.categoria_repo.buscar_por_id(livro.categoria_id)
            if not categoria:
                raise EntidadeNaoEncontradaException("Categoria", str(livro.categoria_id))
        
        # Valida quantidade
        if livro.quantidade_total < 1:
            raise ValidacaoException("Quantidade total deve ser maior que zero", "quantidade_total")
        
        # Define quantidade_disponivel se não foi especificado
        if livro.quantidade_disponivel is None:
            livro.quantidade_disponivel = livro.quantidade_total
        
        if livro.quantidade_disponivel > livro.quantidade_total:
            raise ValidacaoException(
                "Quantidade disponível não pode ser maior que quantidade total",
                "quantidade_disponivel"
            )
        
        livro = self.livro_repo.criar(livro)
        self.logger.info(f"Livro criado com sucesso: ID {livro.id}")
        return livro
    
    def buscar_por_id(self, livro_id: int) -> Livro:
        """
        Busca livro por ID
        
        Args:
            livro_id: ID do livro
        
        Returns:
            Livro encontrado
        
        Raises:
            EntidadeNaoEncontradaException: Se livro não for encontrado
        """
        livro = self.livro_repo.buscar_por_id(livro_id)
        if not livro:
            raise EntidadeNaoEncontradaException("Livro", str(livro_id))
        return livro
    
    def listar_todos(self, skip: int = 0, limit: int = 100) -> List[Livro]:
        """
        Lista todos os livros
        
        Args:
            skip: Número de registros a pular
            limit: Número máximo de registros
        
        Returns:
            Lista de livros
        """
        return self.livro_repo.listar_todos(skip, limit)
    
    def atualizar_livro(self, livro_id: int, dados_atualizacao: dict) -> Livro:
        """
        Atualiza um livro
        
        Args:
            livro_id: ID do livro
            dados_atualizacao: Dicionário com dados a atualizar
        
        Returns:
            Livro atualizado
        
        Raises:
            EntidadeNaoEncontradaException: Se livro não for encontrado
            ValidacaoException: Se validações falharem
        """
        self.logger.info(f"Atualizando livro ID {livro_id}")
        
        livro = self.buscar_por_id(livro_id)
        
        # Valida quantidade se fornecida
        if "quantidade_total" in dados_atualizacao:
            if dados_atualizacao["quantidade_total"] < 1:
                raise ValidacaoException("Quantidade total deve ser maior que zero", "quantidade_total")
        
        # Define quantidade_disponivel se quantidade_total foi atualizada
        if "quantidade_total" in dados_atualizacao and "quantidade_disponivel" not in dados_atualizacao:
            nova_quantidade_total = dados_atualizacao["quantidade_total"]
            if livro.quantidade_disponivel > nova_quantidade_total:
                dados_atualizacao["quantidade_disponivel"] = nova_quantidade_total
        
        # Valida quantidade_disponivel se fornecida
        if "quantidade_disponivel" in dados_atualizacao and "quantidade_total" in dados_atualizacao:
            if dados_atualizacao["quantidade_disponivel"] > dados_atualizacao["quantidade_total"]:
                raise ValidacaoException(
                    "Quantidade disponível não pode ser maior que quantidade total",
                    "quantidade_disponivel"
                )
        elif "quantidade_disponivel" in dados_atualizacao:
            if dados_atualizacao["quantidade_disponivel"] > livro.quantidade_total:
                raise ValidacaoException(
                    "Quantidade disponível não pode ser maior que quantidade total",
                    "quantidade_disponivel"
                )
        
        # Valida autor se fornecido
        if "autor_id" in dados_atualizacao:
            autor = self.autor_repo.buscar_por_id(dados_atualizacao["autor_id"])
            if not autor:
                raise EntidadeNaoEncontradaException("Autor", str(dados_atualizacao["autor_id"]))
        
        # Valida categoria se fornecida
        if "categoria_id" in dados_atualizacao and dados_atualizacao["categoria_id"]:
            categoria = self.categoria_repo.buscar_por_id(dados_atualizacao["categoria_id"])
            if not categoria:
                raise EntidadeNaoEncontradaException("Categoria", str(dados_atualizacao["categoria_id"]))
        
        # Atualiza campos
        for campo, valor in dados_atualizacao.items():
            if hasattr(livro, campo):
                setattr(livro, campo, valor)
        
        livro = self.livro_repo.atualizar(livro)
        self.logger.info(f"Livro ID {livro_id} atualizado com sucesso")
        return livro
    
    def deletar_livro(self, livro_id: int) -> bool:
        """
        Deleta um livro
        
        Args:
            livro_id: ID do livro
        
        Returns:
            True se deletado com sucesso
        
        Raises:
            EntidadeNaoEncontradaException: Se livro não for encontrado
        """
        self.logger.info(f"Deletando livro ID {livro_id}")
        livro = self.buscar_por_id(livro_id)
        return self.livro_repo.deletar(livro_id)
    
    def buscar_com_filtros(
        self,
        filtros: dict,
        skip: int = 0,
        limit: int = 100,
        ordenar_por: Optional[str] = None,
        ordem_desc: bool = False
    ) -> List[Livro]:
        """
        Busca livros com filtros e ordenação
        
        Args:
            filtros: Dicionário com filtros
            skip: Número de registros a pular
            limit: Número máximo de registros
            ordenar_por: Campo para ordenação
            ordem_desc: Se True, ordena em ordem decrescente
        
        Returns:
            Lista de livros filtrados
        """
        return self.livro_repo.buscar_com_filtros(filtros, skip, limit, ordenar_por, ordem_desc)
    
    def buscar_disponiveis(self) -> List[Livro]:
        """
        Busca livros disponíveis
        
        Returns:
            Lista de livros disponíveis
        """
        return self.livro_repo.buscar_disponiveis()


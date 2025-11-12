"""
Serviço de Usuario
"""
from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session

from src.models.usuario import Usuario
from src.repositories.usuario_repository import UsuarioRepository, IUsuarioRepository
from src.exceptions.biblioteca_exceptions import EntidadeNaoEncontradaException, ValidacaoException
from src.validators.validators import Validator
from src.utils.logger import get_logger


class UsuarioService:
    """Serviço para gerenciar usuários"""
    
    def __init__(
        self,
        session: Session,
        usuario_repo: Optional[IUsuarioRepository] = None
    ) -> None:
        """
        Inicializa o serviço com injeção de dependências
        
        Args:
            session: Sessão do banco de dados
            usuario_repo: Repositório de usuários (opcional)
        """
        self.session = session
        self.usuario_repo = usuario_repo or UsuarioRepository(session)
        self.logger = get_logger("UsuarioService")
    
    def criar_usuario(self, usuario: Usuario) -> Usuario:
        """
        Cria um novo usuário com validações
        
        Args:
            usuario: Usuário a ser criado
        
        Returns:
            Usuário criado
        
        Raises:
            ValidacaoException: Se validações falharem
        """
        self.logger.info(f"Criando usuário: {usuario.nome}")
        
        # Valida email
        Validator.validar_email(usuario.email)
        
        # Verifica se email já existe
        usuario_existente = self.usuario_repo.buscar_por_email(usuario.email)
        if usuario_existente:
            raise ValidacaoException(f"Email {usuario.email} já está cadastrado", "email")
        
        # Valida data de nascimento (idade mínima de 12 anos)
        Validator.validar_data_nascimento(usuario.data_nascimento, idade_minima=12)
        
        usuario = self.usuario_repo.criar(usuario)
        self.logger.info(f"Usuário criado com sucesso: ID {usuario.id}")
        return usuario
    
    def buscar_por_id(self, usuario_id: int) -> Usuario:
        """
        Busca usuário por ID
        
        Args:
            usuario_id: ID do usuário
        
        Returns:
            Usuário encontrado
        
        Raises:
            EntidadeNaoEncontradaException: Se usuário não for encontrado
        """
        usuario = self.usuario_repo.buscar_por_id(usuario_id)
        if not usuario:
            raise EntidadeNaoEncontradaException("Usuario", str(usuario_id))
        return usuario
    
    def listar_todos(self, skip: int = 0, limit: int = 100) -> List[Usuario]:
        """
        Lista todos os usuários
        
        Args:
            skip: Número de registros a pular
            limit: Número máximo de registros
        
        Returns:
            Lista de usuários
        """
        return self.usuario_repo.listar_todos(skip, limit)
    
    def atualizar_usuario(self, usuario_id: int, dados_atualizacao: dict) -> Usuario:
        """
        Atualiza um usuário
        
        Args:
            usuario_id: ID do usuário
            dados_atualizacao: Dicionário com dados a atualizar
        
        Returns:
            Usuário atualizado
        
        Raises:
            EntidadeNaoEncontradaException: Se usuário não for encontrado
            ValidacaoException: Se validações falharem
        """
        self.logger.info(f"Atualizando usuário ID {usuario_id}")
        
        usuario = self.buscar_por_id(usuario_id)
        
        # Valida email se fornecido
        if "email" in dados_atualizacao:
            Validator.validar_email(dados_atualizacao["email"])
            usuario_existente = self.usuario_repo.buscar_por_email(dados_atualizacao["email"])
            if usuario_existente and usuario_existente.id != usuario_id:
                raise ValidacaoException(f"Email {dados_atualizacao['email']} já está cadastrado", "email")
        
        # Valida data de nascimento se fornecida
        if "data_nascimento" in dados_atualizacao:
            if isinstance(dados_atualizacao["data_nascimento"], str):
                dados_atualizacao["data_nascimento"] = date.fromisoformat(dados_atualizacao["data_nascimento"])
            Validator.validar_data_nascimento(dados_atualizacao["data_nascimento"], idade_minima=12)
        
        # Atualiza campos
        for campo, valor in dados_atualizacao.items():
            if hasattr(usuario, campo):
                setattr(usuario, campo, valor)
        
        usuario = self.usuario_repo.atualizar(usuario)
        self.logger.info(f"Usuário ID {usuario_id} atualizado com sucesso")
        return usuario
    
    def deletar_usuario(self, usuario_id: int) -> bool:
        """
        Deleta um usuário
        
        Args:
            usuario_id: ID do usuário
        
        Returns:
            True se deletado com sucesso
        
        Raises:
            EntidadeNaoEncontradaException: Se usuário não for encontrado
        """
        self.logger.info(f"Deletando usuário ID {usuario_id}")
        usuario = self.buscar_por_id(usuario_id)
        return self.usuario_repo.deletar(usuario_id)
    
    def buscar_com_filtros(
        self,
        filtros: dict,
        skip: int = 0,
        limit: int = 100,
        ordenar_por: Optional[str] = None,
        ordem_desc: bool = False
    ) -> List[Usuario]:
        """
        Busca usuários com filtros e ordenação
        
        Args:
            filtros: Dicionário com filtros
            skip: Número de registros a pular
            limit: Número máximo de registros
            ordenar_por: Campo para ordenação
            ordem_desc: Se True, ordena em ordem decrescente
        
        Returns:
            Lista de usuários filtrados
        """
        return self.usuario_repo.buscar_com_filtros(filtros, skip, limit, ordenar_por, ordem_desc)


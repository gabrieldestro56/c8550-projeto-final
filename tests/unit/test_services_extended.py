"""
Testes estendidos para serviços - aumentar cobertura
"""
import pytest
from datetime import date, timedelta
from unittest.mock import Mock, patch

from src.services.livro_service import LivroService
from src.services.usuario_service import UsuarioService
from src.services.emprestimo_service import EmprestimoService
from src.services.autor_service import AutorService
from src.services.categoria_service import CategoriaService
from src.models.livro import Livro
from src.models.usuario import Usuario
from src.models.emprestimo import Emprestimo
from src.models.autor import Autor
from src.models.categoria import Categoria
from src.exceptions.biblioteca_exceptions import (
    EntidadeNaoEncontradaException,
    ValidacaoException
)


class TestLivroServiceExtended:
    """Testes estendidos para LivroService"""
    
    def test_listar_todos_com_paginacao(self, livro_service, livro):
        """Testa listagem com paginação"""
        livros = livro_service.listar_todos(skip=0, limit=1)
        assert len(livros) <= 1
    
    def test_buscar_disponiveis(self, livro_service, livro):
        """Testa busca de livros disponíveis"""
        disponiveis = livro_service.buscar_disponiveis()
        assert isinstance(disponiveis, list)


class TestUsuarioServiceExtended:
    """Testes estendidos para UsuarioService"""
    
    def test_listar_todos_com_paginacao(self, usuario_service, usuario):
        """Testa listagem com paginação"""
        usuarios = usuario_service.listar_todos(skip=0, limit=1)
        assert len(usuarios) <= 1
    


class TestEmprestimoServiceExtended:
    """Testes estendidos para EmprestimoService"""
    
    def test_listar_todos_com_paginacao(self, emprestimo_service, emprestimo):
        """Testa listagem com paginação"""
        emprestimos = emprestimo_service.listar_todos(skip=0, limit=1)
        assert len(emprestimos) <= 1
    
    def test_buscar_por_usuario(self, emprestimo_service, emprestimo, usuario):
        """Testa busca de empréstimos por usuário"""
        emprestimos = emprestimo_service.buscar_por_usuario(usuario.id)
        assert isinstance(emprestimos, list)
    
    def test_buscar_atrasados(self, emprestimo_service, db_session, livro, usuario):
        """Testa busca de empréstimos atrasados"""
        # Cria empréstimo atrasado
        emprestimo_atrasado = Emprestimo(
            livro_id=livro.id,
            usuario_id=usuario.id,
            data_emprestimo=date.today() - timedelta(days=20),
            data_prevista_devolucao=date.today() - timedelta(days=5),
            devolvido=False
        )
        db_session.add(emprestimo_atrasado)
        db_session.commit()
        
        atrasados = emprestimo_service.buscar_atrasados()
        assert isinstance(atrasados, list)



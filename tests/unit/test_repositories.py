"""
Testes unitários para repositórios
"""
import pytest

from src.repositories.livro_repository import LivroRepository
from src.repositories.usuario_repository import UsuarioRepository
from src.repositories.emprestimo_repository import EmprestimoRepository
from src.repositories.autor_repository import AutorRepository
from src.repositories.categoria_repository import CategoriaRepository
from src.models.livro import Livro
from src.models.usuario import Usuario
from src.models.emprestimo import Emprestimo
from src.models.autor import Autor
from src.models.categoria import Categoria
from datetime import date, timedelta


class TestLivroRepository:
    """Testes para LivroRepository"""
    
    def test_criar_livro(self, db_session, autor, categoria):
        """Testa criação de livro"""
        repo = LivroRepository(db_session)
        livro = Livro(
            titulo="Teste",
            autor_id=autor.id,
            categoria_id=categoria.id,
            quantidade_total=5
        )
        livro_criado = repo.criar(livro)
        assert livro_criado.id is not None
        assert livro_criado.titulo == "Teste"
    
    def test_buscar_por_id(self, db_session, livro):
        """Testa busca de livro por ID"""
        repo = LivroRepository(db_session)
        livro_encontrado = repo.buscar_por_id(livro.id)
        assert livro_encontrado is not None
        assert livro_encontrado.id == livro.id
    
    
    def test_buscar_disponiveis(self, db_session, livro):
        """Testa busca de livros disponíveis"""
        repo = LivroRepository(db_session)
        livros = repo.buscar_disponiveis()
        assert len(livros) > 0
        assert all(l.disponivel for l in livros)
    
    def test_atualizar_livro(self, db_session, livro):
        """Testa atualização de livro"""
        repo = LivroRepository(db_session)
        livro.titulo = "Título Atualizado"
        livro_atualizado = repo.atualizar(livro)
        assert livro_atualizado.titulo == "Título Atualizado"
    
    def test_deletar_livro(self, db_session, livro):
        """Testa deleção de livro"""
        repo = LivroRepository(db_session)
        resultado = repo.deletar(livro.id)
        assert resultado is True
        assert repo.buscar_por_id(livro.id) is None


class TestUsuarioRepository:
    """Testes para UsuarioRepository"""
    
    def test_criar_usuario(self, db_session):
        """Testa criação de usuário"""
        repo = UsuarioRepository(db_session)
        usuario = Usuario(
            nome="Teste",
            email="teste@example.com",
            
            data_nascimento=date(1990, 1, 1)
        )
        usuario_criado = repo.criar(usuario)
        assert usuario_criado.id is not None
    
    def test_buscar_por_email(self, db_session, usuario):
        """Testa busca de usuário por email"""
        repo = UsuarioRepository(db_session)
        usuario_encontrado = repo.buscar_por_email(usuario.email)
        assert usuario_encontrado is not None
        assert usuario_encontrado.email == usuario.email
    


class TestEmprestimoRepository:
    """Testes para EmprestimoRepository"""
    
    def test_buscar_por_usuario(self, db_session, emprestimo):
        """Testa busca de empréstimos por usuário"""
        repo = EmprestimoRepository(db_session)
        emprestimos = repo.buscar_por_usuario(emprestimo.usuario_id)
        assert len(emprestimos) > 0
        assert all(e.usuario_id == emprestimo.usuario_id for e in emprestimos)
    
    def test_buscar_ativos(self, db_session, emprestimo):
        """Testa busca de empréstimos ativos"""
        repo = EmprestimoRepository(db_session)
        emprestimos = repo.buscar_ativos()
        assert len(emprestimos) > 0
        assert all(not e.devolvido for e in emprestimos)
    
    def test_buscar_atrasados(self, db_session):
        """Testa busca de empréstimos atrasados"""
        repo = EmprestimoRepository(db_session)
        # Cria empréstimo atrasado
        emprestimo_atrasado = Emprestimo(
            livro_id=1,
            usuario_id=1,
            data_emprestimo=date.today() - timedelta(days=20),
            data_prevista_devolucao=date.today() - timedelta(days=5),
            devolvido=False
        )
        db_session.add(emprestimo_atrasado)
        db_session.commit()
        
        emprestimos = repo.buscar_atrasados()
        assert len(emprestimos) > 0


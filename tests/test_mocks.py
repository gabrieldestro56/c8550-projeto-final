"""
Testes com Mocks e Stubs
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import date

from src.services.livro_service import LivroService
from src.services.usuario_service import UsuarioService
from src.services.emprestimo_service import EmprestimoService
from src.repositories.livro_repository import LivroRepository
from src.repositories.usuario_repository import UsuarioRepository
from src.models.livro import Livro
from src.models.usuario import Usuario
from src.models.autor import Autor
from src.exceptions.biblioteca_exceptions import EntidadeNaoEncontradaException


class TestMocksRepositorios:
    """Testes usando mocks de repositórios"""
    
    def test_livro_service_com_mock_repositorio(self, db_session):
        """Testa serviço de livro com repositório mockado"""
        mock_repo = Mock(spec=LivroRepository)
        mock_repo.buscar_por_id.return_value = None
        
        service = LivroService(db_session, livro_repo=mock_repo)
        
        with pytest.raises(EntidadeNaoEncontradaException):
            service.buscar_por_id(999)
        
        mock_repo.buscar_por_id.assert_called_once_with(999)
    
    def test_usuario_service_com_mock_repositorio(self, db_session):
        """Testa serviço de usuário com repositório mockado"""
        mock_repo = Mock(spec=UsuarioRepository)
        usuario_mock = Usuario(
            nome="Mock User",
            email="mock@example.com",
            
            data_nascimento=date(1990, 1, 1)
        )
        mock_repo.buscar_por_id.return_value = usuario_mock
        
        service = UsuarioService(db_session, usuario_repo=mock_repo)
        usuario = service.buscar_por_id(1)
        
        assert usuario.nome == "Mock User"
        mock_repo.buscar_por_id.assert_called_once_with(1)
    
    @patch('src.services.emprestimo_service.date')
    def test_emprestimo_service_com_mock_date(self, mock_date, db_session):
        """Testa serviço de empréstimo com data mockada"""
        mock_date.today.return_value = date(2024, 1, 1)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
        
        autor = Autor(nome="Autor", nacionalidade="BR")
        db_session.add(autor)
        db_session.commit()
        
        livro = Livro(titulo="Livro", autor_id=autor.id, quantidade_total=5, quantidade_disponivel=5)
        db_session.add(livro)
        db_session.commit()
        
        usuario = Usuario(
            nome="Usuário",
            email="user@example.com",
            
            data_nascimento=date(1990, 1, 1),
            ativo=True
        )
        db_session.add(usuario)
        db_session.commit()
        
        service = EmprestimoService(db_session)
        emprestimo = service.criar_emprestimo(livro.id, usuario.id)
        
        assert emprestimo.data_emprestimo == date(2024, 1, 1)


class TestStubs:
    """Testes usando stubs"""
    
    def test_stub_repositorio_livro(self, db_session):
        """Testa com stub de repositório de livro"""
        class StubLivroRepository:
            def buscar_por_id(self, id):
                if id == 1:
                    livro = Livro(titulo="Stub Livro", autor_id=1, quantidade_total=5)
                    livro.id = 1
                    return livro
                return None
        
        stub_repo = StubLivroRepository()
        service = LivroService(db_session, livro_repo=stub_repo)
        
        livro = service.buscar_por_id(1)
        assert livro.titulo == "Stub Livro"
        
        with pytest.raises(EntidadeNaoEncontradaException):
            service.buscar_por_id(999)


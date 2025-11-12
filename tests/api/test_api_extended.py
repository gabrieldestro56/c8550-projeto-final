"""
Testes estendidos de API REST para aumentar cobertura
"""
import pytest
from fastapi.testclient import TestClient
from fastapi import Depends
from datetime import date
from unittest.mock import patch, MagicMock

from src.api.main import app
from src.api.dependencies import get_db
from src.models.autor import Autor
from src.models.categoria import Categoria
from src.models.livro import Livro
from src.models.usuario import Usuario
from src.models.emprestimo import Emprestimo
from src.exceptions.biblioteca_exceptions import (
    EntidadeNaoEncontradaException,
    ValidacaoException,
    RegraNegocioException
)


@pytest.fixture
def client(db_session):
    """Cria cliente de teste para API com sessão override"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass  # Não fecha a sessão, ela é gerenciada pelo fixture
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def setup_dados(db_session):
    """Setup de dados para testes de API"""
    autor = Autor(nome="Autor Teste", nacionalidade="Brasileiro")
    db_session.add(autor)
    db_session.commit()
    db_session.refresh(autor)
    
    categoria = Categoria(nome="Ficção", descricao="Livros de ficção")
    db_session.add(categoria)
    db_session.commit()
    db_session.refresh(categoria)
    
    livro = Livro(
        titulo="Livro Teste",
        autor_id=autor.id,
        categoria_id=categoria.id,
        quantidade_total=5
    )
    db_session.add(livro)
    db_session.commit()
    db_session.refresh(livro)
    
    usuario = Usuario(
        nome="Usuário Teste",
        email="teste@example.com",
        data_nascimento=date(1990, 1, 1)
    )
    db_session.add(usuario)
    db_session.commit()
    db_session.refresh(usuario)
    
    emprestimo = Emprestimo(
        livro_id=livro.id,
        usuario_id=usuario.id,
        data_emprestimo=date.today(),
        data_prevista_devolucao=date.today()
    )
    db_session.add(emprestimo)
    db_session.commit()
    db_session.refresh(emprestimo)
    
    return {
        "autor": autor,
        "categoria": categoria,
        "livro": livro,
        "usuario": usuario,
        "emprestimo": emprestimo
    }


class TestAPILivrosExtended:
    """Testes estendidos para endpoints de livros"""
    
    def test_atualizar_livro_put(self, client, setup_dados):
        """Testa atualização de livro via PUT"""
        dados = {
            "titulo": "Livro Atualizado",
            "ano_publicacao": 2021,
            "autor_id": setup_dados["autor"].id
        }
        response = client.put(f"/livros/{setup_dados['livro'].id}", json=dados)
        assert response.status_code == 200
        assert response.json()["titulo"] == "Livro Atualizado"


class TestAPIUsuariosExtended:
    """Testes estendidos para endpoints de usuários"""
    
    def test_atualizar_usuario_put(self, client, setup_dados):
        """Testa atualização de usuário via PUT"""
        dados = {
            "nome": "Usuário Atualizado",
            "email": "atualizado@example.com",
            "data_nascimento": "1990-01-01"
        }
        response = client.put(f"/usuarios/{setup_dados['usuario'].id}", json=dados)
        assert response.status_code == 200
        assert response.json()["nome"] == "Usuário Atualizado"


class TestAPIEmprestimosExtended:
    """Testes estendidos para endpoints de empréstimos"""
    
    def test_buscar_emprestimo_por_id(self, client, setup_dados):
        """Testa busca de empréstimo por ID"""
        response = client.get(f"/emprestimos/{setup_dados['emprestimo'].id}")
        assert response.status_code == 200
        assert response.json()["id"] == setup_dados["emprestimo"].id


class TestAPIAutoresExtended:
    """Testes estendidos para endpoints de autores"""
    
    def test_criar_autor_post(self, client):
        """Testa criação de autor via POST"""
        dados = {
            "nome": "Novo Autor",
            "nacionalidade": "Brasileiro"
        }
        response = client.post("/autores", json=dados)
        assert response.status_code == 201
    
    def test_atualizar_autor_put(self, client, setup_dados):
        """Testa atualização de autor via PUT"""
        dados = {"nome": "Autor Atualizado"}
        response = client.put(f"/autores/{setup_dados['autor'].id}", json=dados)
        assert response.status_code == 200


class TestAPICategoriasExtended:
    """Testes estendidos para endpoints de categorias"""
    
    def test_criar_categoria_post(self, client):
        """Testa criação de categoria via POST"""
        dados = {
            "nome": "Nova Categoria",
            "descricao": "Descrição da categoria"
        }
        response = client.post("/categorias", json=dados)
        assert response.status_code == 201
    
    def test_atualizar_categoria_put(self, client, setup_dados):
        """Testa atualização de categoria via PUT"""
        dados = {"nome": "Categoria Atualizada"}
        response = client.put(f"/categorias/{setup_dados['categoria'].id}", json=dados)
        assert response.status_code == 200


class TestAPIExceptionHandlers:
    """Testes para handlers de exceções"""
    
    def test_exception_handler_entidade_nao_encontrada(self, client):
        """Testa handler de exceção de entidade não encontrada"""
        response = client.get("/livros/99999")
        assert response.status_code == 404



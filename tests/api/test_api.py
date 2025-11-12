"""
Testes de API REST
"""
import pytest
from fastapi.testclient import TestClient
from fastapi import Depends
from datetime import date
from unittest.mock import patch

from src.api.main import app
from src.api.dependencies import get_db
from src.models.autor import Autor
from src.models.categoria import Categoria
from src.models.livro import Livro
from src.models.usuario import Usuario




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
    
    return {"autor": autor, "categoria": categoria, "livro": livro, "usuario": usuario}


class TestAPILivros:
    """Testes de API para livros"""
    
    def test_criar_livro_post(self, client, setup_dados):
        """Testa criação de livro via POST"""
        dados = {
            "titulo": "Novo Livro",
            "autor_id": setup_dados["autor"].id,
            "categoria_id": setup_dados["categoria"].id,
            "quantidade_total": 3
        }
        response = client.post("/livros", json=dados)
        assert response.status_code == 201
        assert response.json()["titulo"] == "Novo Livro"
    
    def test_listar_livros_get(self, client, setup_dados):
        """Testa listagem de livros via GET"""
        response = client.get("/livros")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_buscar_livro_por_id_get(self, client, setup_dados):
        """Testa busca de livro por ID via GET"""
        livro_id = setup_dados["livro"].id
        response = client.get(f"/livros/{livro_id}")
        assert response.status_code == 200
        assert response.json()["id"] == livro_id
    
    def test_atualizar_livro_put(self, client, setup_dados):
        """Testa atualização de livro via PUT"""
        livro_id = setup_dados["livro"].id
        dados = {"titulo": "Título Atualizado"}
        response = client.put(f"/livros/{livro_id}", json=dados)
        assert response.status_code == 200
        assert response.json()["titulo"] == "Título Atualizado"
    
    def test_deletar_livro_delete(self, client, setup_dados):
        """Testa deleção de livro via DELETE"""
        livro_id = setup_dados["livro"].id
        response = client.delete(f"/livros/{livro_id}")
        assert response.status_code == 204


class TestAPIUsuarios:
    """Testes de API para usuários"""
    
    def test_criar_usuario_post(self, client):
        """Testa criação de usuário via POST"""
        dados = {
            "nome": "Novo Usuário",
            "email": "novo@example.com",
            "data_nascimento": "1990-01-01"
        }
        response = client.post("/usuarios", json=dados)
        assert response.status_code == 201
        assert response.json()["nome"] == "Novo Usuário"
    
    def test_atualizar_usuario_put(self, client, setup_dados):
        """Testa atualização de usuário via PUT"""
        usuario_id = setup_dados["usuario"].id
        dados = {"nome": "Nome Atualizado"}
        response = client.put(f"/usuarios/{usuario_id}", json=dados)
        assert response.status_code == 200
        assert response.json()["nome"] == "Nome Atualizado"
    
    def test_deletar_usuario_delete(self, client, setup_dados):
        """Testa deleção de usuário via DELETE"""
        usuario_id = setup_dados["usuario"].id
        response = client.delete(f"/usuarios/{usuario_id}")
        assert response.status_code == 204
    
    def test_listar_usuarios_get(self, client):
        """Testa listagem de usuários via GET"""
        response = client.get("/usuarios")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_buscar_usuario_por_id_get(self, client, setup_dados):
        """Testa busca de usuário por ID via GET"""
        usuario_id = setup_dados["usuario"].id
        response = client.get(f"/usuarios/{usuario_id}")
        assert response.status_code == 200
        assert response.json()["id"] == usuario_id


class TestAPIEmprestimos:
    """Testes de API para empréstimos"""
    
    def test_criar_emprestimo_post(self, client, setup_dados):
        """Testa criação de empréstimo via POST"""
        dados = {
            "livro_id": setup_dados["livro"].id,
            "usuario_id": setup_dados["usuario"].id
        }
        response = client.post("/emprestimos", json=dados)
        assert response.status_code == 201
        assert response.json()["livro_id"] == setup_dados["livro"].id
    
    def test_listar_emprestimos_get(self, client):
        """Testa listagem de empréstimos via GET"""
        response = client.get("/emprestimos")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_devolver_emprestimo_post(self, client, setup_dados, db_session):
        """Testa devolução de empréstimo via POST"""
        from src.models.emprestimo import Emprestimo
        from datetime import timedelta
        
        emprestimo = Emprestimo(
            livro_id=setup_dados["livro"].id,
            usuario_id=setup_dados["usuario"].id,
            data_emprestimo=date.today(),
            data_prevista_devolucao=date.today() + timedelta(days=14),
            devolvido=False
        )
        db_session.add(emprestimo)
        db_session.commit()
        
        response = client.post(f"/emprestimos/{emprestimo.id}/devolver")
        assert response.status_code == 200
        assert response.json()["devolvido"] is True


class TestAPIHealthCheck:
    """Testes de health check"""
    
    def test_health_check(self, client):
        """Testa endpoint de health check"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


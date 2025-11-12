"""
Testes unitários para AutorService
"""
import pytest
from datetime import date

from src.services.autor_service import AutorService
from src.models.autor import Autor
from src.exceptions.biblioteca_exceptions import EntidadeNaoEncontradaException


class TestAutorService:
    """Testes para AutorService"""
    
    def test_criar_autor(self, db_session, autor_service):
        """Testa criação de autor"""
        autor = Autor(
            nome="Novo Autor",
            nacionalidade="Brasileiro",
            data_nascimento=date(1980, 1, 1)
        )
        autor_criado = autor_service.criar_autor(autor)
        assert autor_criado.id is not None
        assert autor_criado.nome == "Novo Autor"
    
    def test_buscar_por_id_sucesso(self, db_session, autor_service, autor):
        """Testa busca de autor por ID"""
        autor_encontrado = autor_service.buscar_por_id(autor.id)
        assert autor_encontrado.id == autor.id
    
    def test_buscar_por_id_nao_encontrado(self, db_session, autor_service):
        """Testa busca de autor inexistente"""
        with pytest.raises(EntidadeNaoEncontradaException):
            autor_service.buscar_por_id(99999)
    
    def test_listar_todos(self, db_session, autor_service, autor):
        """Testa listagem de todos os autores"""
        autores = autor_service.listar_todos()
        assert len(autores) > 0
    
    def test_atualizar_autor(self, db_session, autor_service, autor):
        """Testa atualização de autor"""
        dados = {"nome": "Nome Atualizado"}
        autor_atualizado = autor_service.atualizar_autor(autor.id, dados)
        assert autor_atualizado.nome == "Nome Atualizado"
    
    def test_deletar_autor(self, db_session, autor_service, autor):
        """Testa deleção de autor"""
        resultado = autor_service.deletar_autor(autor.id)
        assert resultado is True
        
        with pytest.raises(EntidadeNaoEncontradaException):
            autor_service.buscar_por_id(autor.id)
    
    def test_buscar_por_nome(self, db_session, autor_service, autor):
        """Testa busca de autor por nome"""
        autores = autor_service.buscar_por_nome(autor.nome)
        assert len(autores) > 0
        assert any(a.nome == autor.nome for a in autores)


@pytest.fixture
def autor_service(db_session):
    """Fixture para AutorService"""
    return AutorService(db_session)


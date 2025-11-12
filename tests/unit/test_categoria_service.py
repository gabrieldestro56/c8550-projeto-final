"""
Testes unitários para CategoriaService
"""
import pytest

from src.services.categoria_service import CategoriaService
from src.models.categoria import Categoria
from src.exceptions.biblioteca_exceptions import EntidadeNaoEncontradaException


class TestCategoriaService:
    """Testes para CategoriaService"""
    
    def test_criar_categoria(self, db_session, categoria_service):
        """Testa criação de categoria"""
        categoria = Categoria(
            nome="Nova Categoria",
            descricao="Descrição da categoria"
        )
        categoria_criada = categoria_service.criar_categoria(categoria)
        assert categoria_criada.id is not None
        assert categoria_criada.nome == "Nova Categoria"
    
    def test_buscar_por_id_sucesso(self, db_session, categoria_service, categoria):
        """Testa busca de categoria por ID"""
        categoria_encontrada = categoria_service.buscar_por_id(categoria.id)
        assert categoria_encontrada.id == categoria.id
    
    def test_buscar_por_id_nao_encontrado(self, db_session, categoria_service):
        """Testa busca de categoria inexistente"""
        with pytest.raises(EntidadeNaoEncontradaException):
            categoria_service.buscar_por_id(99999)
    
    def test_listar_todos(self, db_session, categoria_service, categoria):
        """Testa listagem de todas as categorias"""
        categorias = categoria_service.listar_todos()
        assert len(categorias) > 0
    
    def test_atualizar_categoria(self, db_session, categoria_service, categoria):
        """Testa atualização de categoria"""
        dados = {"nome": "Nome Atualizado"}
        categoria_atualizada = categoria_service.atualizar_categoria(categoria.id, dados)
        assert categoria_atualizada.nome == "Nome Atualizado"
    
    def test_deletar_categoria(self, db_session, categoria_service, categoria):
        """Testa deleção de categoria"""
        resultado = categoria_service.deletar_categoria(categoria.id)
        assert resultado is True
        
        with pytest.raises(EntidadeNaoEncontradaException):
            categoria_service.buscar_por_id(categoria.id)
    
    def test_buscar_por_nome(self, db_session, categoria_service, categoria):
        """Testa busca de categoria por nome"""
        categoria_encontrada = categoria_service.buscar_por_nome(categoria.nome)
        assert categoria_encontrada.nome == categoria.nome
    
    def test_buscar_por_nome_nao_encontrado(self, db_session, categoria_service):
        """Testa busca de categoria por nome inexistente"""
        with pytest.raises(EntidadeNaoEncontradaException):
            categoria_service.buscar_por_nome("Categoria Inexistente")


@pytest.fixture
def categoria_service(db_session):
    """Fixture para CategoriaService"""
    return CategoriaService(db_session)


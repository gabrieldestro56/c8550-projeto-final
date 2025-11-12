"""
Testes de Orientação a Objetos
"""
import pytest
from datetime import date

from src.models.livro import Livro
from src.models.usuario import Usuario
from src.models.autor import Autor
from src.repositories.base_repository import BaseRepository, IRepository
from src.repositories.livro_repository import LivroRepository


class TestHeranca:
    """Testes de herança"""
    
    def test_livro_repository_herda_base_repository(self):
        """Testa que LivroRepository herda de BaseRepository"""
        assert issubclass(LivroRepository, BaseRepository)
    
    def test_livro_repository_implementa_interface(self):
        """Testa que LivroRepository implementa IRepository"""
        assert issubclass(LivroRepository, IRepository)


class TestPolimorfismo:
    """Testes de polimorfismo"""
    
    def test_polimorfismo_repositorios(self, db_session):
        """Testa polimorfismo em repositórios"""
        repositorios = [
            LivroRepository(db_session)
        ]
        
        # Todos devem ter método buscar_por_id
        for repo in repositorios:
            assert hasattr(repo, 'buscar_por_id')
            assert callable(getattr(repo, 'buscar_por_id'))


class TestEncapsulamento:
    """Testes de encapsulamento"""
    
    def test_metodos_publicos_livro(self):
        """Testa que métodos públicos estão acessíveis"""
        livro = Livro(titulo="Teste", autor_id=1, quantidade_total=5)
        
        # Métodos públicos devem estar acessíveis
        assert hasattr(livro, 'esta_disponivel')
        assert hasattr(livro, 'emprestar')
        assert hasattr(livro, 'devolver')
    
    def test_atributos_protegidos(self):
        """Testa que atributos estão acessíveis (Python não tem privacidade real)"""
        livro = Livro(titulo="Teste", autor_id=1, quantidade_total=5)
        
        # Atributos devem estar acessíveis
        assert hasattr(livro, 'titulo')
        assert hasattr(livro, 'quantidade_disponivel')


class TestAbstracao:
    """Testes de abstração"""
    
    def test_interface_repositorio_abstrata(self):
        """Testa que IRepository é uma interface abstrata"""
        from abc import ABC
        
        assert issubclass(IRepository, ABC)
        
        # Não deve poder instanciar diretamente
        with pytest.raises(TypeError):
            IRepository()


class TestMetodosAbstratos:
    """Testes de métodos abstratos"""
    
    def test_base_repository_implementa_metodos_abstratos(self):
        """Testa que BaseRepository implementa métodos abstratos"""
        # BaseRepository deve implementar todos os métodos de IRepository
        assert hasattr(BaseRepository, 'criar')
        assert hasattr(BaseRepository, 'buscar_por_id')
        assert hasattr(BaseRepository, 'listar_todos')
        assert hasattr(BaseRepository, 'atualizar')
        assert hasattr(BaseRepository, 'deletar')


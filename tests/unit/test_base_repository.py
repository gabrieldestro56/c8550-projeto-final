"""
Testes unitários para BaseRepository
"""
import pytest

from src.repositories.base_repository import BaseRepository
from src.repositories.autor_repository import AutorRepository
from src.models.autor import Autor


class TestBaseRepository:
    """Testes para BaseRepository"""
    
    def test_buscar_com_filtros_simples(self, db_session):
        """Testa busca com filtros simples"""
        repo = AutorRepository(db_session)
        
        autor1 = Autor(nome="Autor A", nacionalidade="Brasileiro")
        autor2 = Autor(nome="Autor B", nacionalidade="Americano")
        db_session.add_all([autor1, autor2])
        db_session.commit()
        
        filtros = {"nacionalidade": "Brasileiro"}
        resultados = repo.buscar_com_filtros(filtros)
        assert len(resultados) > 0
        assert all(a.nacionalidade == "Brasileiro" for a in resultados)
    
    def test_buscar_com_filtros_like(self, db_session):
        """Testa busca com filtro LIKE"""
        repo = AutorRepository(db_session)
        
        autor = Autor(nome="Machado de Assis", nacionalidade="Brasileiro")
        db_session.add(autor)
        db_session.commit()
        
        filtros = {"nome": {"like": "%Machado%"}}
        resultados = repo.buscar_com_filtros(filtros)
        assert len(resultados) > 0
    
    def test_buscar_com_filtros_comparacao(self, db_session):
        """Testa busca com filtros de comparação"""
        from datetime import date
        repo = AutorRepository(db_session)
        
        # Cria autor com data de nascimento
        autor = Autor(
            nome="Autor Teste",
            nacionalidade="Brasileiro",
            data_nascimento=date(1980, 1, 1)
        )
        db_session.add(autor)
        db_session.commit()
        
        filtros = {"data_nascimento": {"gte": date(1970, 1, 1)}}
        resultados = repo.buscar_com_filtros(filtros)
        assert len(resultados) > 0
    
    def test_buscar_com_filtros_ordenacao(self, db_session):
        """Testa busca com ordenação"""
        repo = AutorRepository(db_session)
        
        autor1 = Autor(nome="Z Autor", nacionalidade="Brasileiro")
        autor2 = Autor(nome="A Autor", nacionalidade="Brasileiro")
        db_session.add_all([autor1, autor2])
        db_session.commit()
        
        filtros = {}
        resultados = repo.buscar_com_filtros(filtros, ordenar_por="nome", ordem_desc=False)
        assert len(resultados) >= 2
    
    def test_buscar_com_filtros_paginacao(self, db_session):
        """Testa busca com paginação"""
        repo = AutorRepository(db_session)
        
        # Cria vários autores
        for i in range(5):
            autor = Autor(nome=f"Autor {i}", nacionalidade="Brasileiro")
            db_session.add(autor)
        db_session.commit()
        
        filtros = {}
        resultados = repo.buscar_com_filtros(filtros, skip=0, limit=2)
        assert len(resultados) <= 2
        
        resultados = repo.buscar_com_filtros(filtros, skip=2, limit=2)
        assert len(resultados) <= 2


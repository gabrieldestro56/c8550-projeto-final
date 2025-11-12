"""
Testes de Performance
"""
import pytest
from datetime import date

from src.services.livro_service import LivroService
from src.services.usuario_service import UsuarioService
from src.models.livro import Livro
from src.models.usuario import Usuario
from src.models.autor import Autor


class TestPerformance:
    """Testes de performance"""
    
    @pytest.mark.benchmark
    def test_performance_criar_multiplos_livros(self, db_session, benchmark):
        """Testa performance de criação de múltiplos livros"""
        autor = Autor(nome="Autor", nacionalidade="BR")
        db_session.add(autor)
        db_session.commit()
        
        livro_service = LivroService(db_session)
        
        def criar_livros():
            for i in range(100):
                livro = Livro(
                    titulo=f"Livro {i}",
                    autor_id=autor.id,
                    quantidade_total=5
                )
                livro_service.criar_livro(livro)
        
        benchmark(criar_livros)
    
    @pytest.mark.benchmark
    def test_performance_buscar_com_filtros(self, db_session, benchmark):
        """Testa performance de busca com filtros"""
        autor = Autor(nome="Autor", nacionalidade="BR")
        db_session.add(autor)
        db_session.commit()
        
        # Cria múltiplos livros
        livro_service = LivroService(db_session)
        for i in range(50):
            livro = Livro(
                titulo=f"Livro {i}",
                autor_id=autor.id,
                quantidade_total=5,
                disponivel=(i % 2 == 0)
            )
            db_session.add(livro)
        db_session.commit()
        
        def buscar():
            livro_service.buscar_com_filtros({"disponivel": True})
        
        benchmark(buscar)
    
    @pytest.mark.benchmark
    def test_performance_listar_todos(self, db_session, benchmark):
        """Testa performance de listagem"""
        autor = Autor(nome="Autor", nacionalidade="BR")
        db_session.add(autor)
        db_session.commit()
        
        # Cria múltiplos livros
        livros = []
        for i in range(200):
            livro = Livro(titulo=f"Livro {i}", autor_id=autor.id, quantidade_total=5)
            livros.append(livro)
        db_session.add_all(livros)
        db_session.commit()
        
        livro_service = LivroService(db_session)
        
        def listar():
            livro_service.listar_todos(skip=0, limit=100)
        
        benchmark(listar)


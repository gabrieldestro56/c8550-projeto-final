"""
Testes unitários para exceções
"""
import pytest

from src.exceptions.biblioteca_exceptions import (
    BibliotecaException,
    EntidadeNaoEncontradaException,
    ValidacaoException,
    RegraNegocioException,
    LivroIndisponivelException,
    LimiteEmprestimosException,
    IdadeMinimaException,
    EmprestimoNaoEncontradoException,
    EmprestimoJaDevolvidoException
)


class TestBibliotecaException:
    """Testes para BibliotecaException"""
    
    def test_criar_excecao_base(self):
        """Testa criação de exceção base"""
        exc = BibliotecaException("Erro genérico", "CODE")
        assert exc.message == "Erro genérico"
        assert exc.code == "CODE"
        assert str(exc) == "Erro genérico"


class TestEntidadeNaoEncontradaException:
    """Testes para EntidadeNaoEncontradaException"""
    
    def test_criar_excecao_entidade_nao_encontrada(self):
        """Testa criação de exceção de entidade não encontrada"""
        exc = EntidadeNaoEncontradaException("Livro", "123")
        assert "Livro" in exc.message
        assert "123" in exc.message
        assert exc.entidade == "Livro"
        assert exc.identificador == "123"


class TestValidacaoException:
    """Testes para ValidacaoException"""
    
    def test_criar_excecao_validacao(self):
        """Testa criação de exceção de validação"""
        exc = ValidacaoException("Campo inválido", "campo")
        assert exc.message == "Campo inválido"
        assert exc.campo == "campo"


class TestRegraNegocioException:
    """Testes para RegraNegocioException"""
    
    def test_criar_excecao_regra_negocio(self):
        """Testa criação de exceção de regra de negócio"""
        exc = RegraNegocioException("Regra violada")
        assert exc.message == "Regra violada"


class TestLivroIndisponivelException:
    """Testes para LivroIndisponivelException"""
    
    def test_criar_excecao_livro_indisponivel(self):
        """Testa criação de exceção de livro indisponível"""
        exc = LivroIndisponivelException(123)
        assert "123" in exc.message
        assert exc.livro_id == 123


class TestLimiteEmprestimosException:
    """Testes para LimiteEmprestimosException"""
    
    def test_criar_excecao_limite_emprestimos(self):
        """Testa criação de exceção de limite de empréstimos"""
        exc = LimiteEmprestimosException(456, 5)
        assert "456" in exc.message
        assert "5" in exc.message
        assert exc.usuario_id == 456
        assert exc.limite == 5


class TestIdadeMinimaException:
    """Testes para IdadeMinimaException"""
    
    def test_criar_excecao_idade_minima(self):
        """Testa criação de exceção de idade mínima"""
        exc = IdadeMinimaException(10, 12)
        assert "10" in exc.message
        assert "12" in exc.message
        assert exc.idade == 10
        assert exc.idade_minima == 12


class TestEmprestimoNaoEncontradoException:
    """Testes para EmprestimoNaoEncontradoException"""
    
    def test_criar_excecao_emprestimo_nao_encontrado(self):
        """Testa criação de exceção de empréstimo não encontrado"""
        exc = EmprestimoNaoEncontradoException(789)
        assert "789" in exc.message
        assert exc.emprestimo_id == 789


class TestEmprestimoJaDevolvidoException:
    """Testes para EmprestimoJaDevolvidoException"""
    
    def test_criar_excecao_emprestimo_ja_devolvido(self):
        """Testa criação de exceção de empréstimo já devolvido"""
        exc = EmprestimoJaDevolvidoException(101)
        assert "101" in exc.message
        assert exc.emprestimo_id == 101


"""
Testes unitários para modelos
"""
import pytest
from datetime import date, timedelta

from src.models.livro import Livro
from src.models.usuario import Usuario
from src.models.emprestimo import Emprestimo
from src.models.autor import Autor
from src.models.categoria import Categoria


class TestLivro:
    """Testes para modelo Livro"""
    
    def test_esta_disponivel_livro_disponivel(self):
        """Testa verificação de disponibilidade quando livro está disponível"""
        livro = Livro(
            titulo="Teste",
            autor_id=1,
            quantidade_total=5,
            quantidade_disponivel=3,
            disponivel=True
        )
        assert livro.esta_disponivel() is True
    
    def test_esta_disponivel_livro_indisponivel(self):
        """Testa verificação de disponibilidade quando livro não está disponível"""
        livro = Livro(
            titulo="Teste",
            autor_id=1,
            quantidade_total=5,
            quantidade_disponivel=0,
            disponivel=False
        )
        assert livro.esta_disponivel() is False
    
    def test_emprestar_livro(self):
        """Testa empréstimo de livro"""
        livro = Livro(
            titulo="Teste",
            autor_id=1,
            quantidade_total=5,
            quantidade_disponivel=3,
            disponivel=True
        )
        resultado = livro.emprestar()
        assert resultado is True
        assert livro.quantidade_disponivel == 2
        assert livro.disponivel is True
    
    def test_emprestar_livro_esgota_estoque(self):
        """Testa empréstimo que esgota estoque"""
        livro = Livro(
            titulo="Teste",
            autor_id=1,
            quantidade_total=5,
            quantidade_disponivel=1,
            disponivel=True
        )
        livro.emprestar()
        assert livro.quantidade_disponivel == 0
        assert livro.disponivel is False
    
    def test_devolver_livro(self):
        """Testa devolução de livro"""
        livro = Livro(
            titulo="Teste",
            autor_id=1,
            quantidade_total=5,
            quantidade_disponivel=2,
            disponivel=True
        )
        livro.devolver()
        assert livro.quantidade_disponivel == 3
        assert livro.disponivel is True


class TestUsuario:
    """Testes para modelo Usuario"""
    
    def test_calcular_idade(self):
        """Testa cálculo de idade do usuário"""
        from datetime import date
        hoje = date.today()
        ano_nascimento = hoje.year - 25
        usuario = Usuario(
            nome="Teste",
            email="teste@example.com",
            data_nascimento=date(ano_nascimento, 1, 1)
        )
        # Idade pode variar em 1 ano dependendo do dia atual
        assert usuario.idade() in [24, 25]
    
    def test_pode_emprestar_limite_nao_atingido(self):
        """Testa verificação de possibilidade de empréstimo quando limite não foi atingido"""
        usuario = Usuario(
            nome="Teste",
            email="teste@example.com",
            
            data_nascimento=date(1990, 1, 1),
            ativo=True
        )
        assert usuario.pode_emprestar(max_emprestimos=5) is True
    
    def test_pode_emprestar_usuario_inativo(self):
        """Testa que usuário inativo não pode emprestar"""
        usuario = Usuario(
            nome="Teste",
            email="teste@example.com",
            
            data_nascimento=date(1990, 1, 1),
            ativo=False
        )
        assert usuario.pode_emprestar() is False


class TestEmprestimo:
    """Testes para modelo Emprestimo"""
    
    def test_esta_atrasado_nao_atrasado(self):
        """Testa verificação de atraso quando não está atrasado"""
        hoje = date.today()
        emprestimo = Emprestimo(
            livro_id=1,
            usuario_id=1,
            data_emprestimo=hoje,
            data_prevista_devolucao=hoje + timedelta(days=14),
            devolvido=False
        )
        assert emprestimo.esta_atrasado() is False
    
    def test_esta_atrasado_atrasado(self):
        """Testa verificação de atraso quando está atrasado"""
        hoje = date.today()
        emprestimo = Emprestimo(
            livro_id=1,
            usuario_id=1,
            data_emprestimo=hoje - timedelta(days=20),
            data_prevista_devolucao=hoje - timedelta(days=6),
            devolvido=False
        )
        assert emprestimo.esta_atrasado() is True
    
    def test_dias_atraso(self):
        """Testa cálculo de dias de atraso"""
        hoje = date.today()
        emprestimo = Emprestimo(
            livro_id=1,
            usuario_id=1,
            data_emprestimo=hoje - timedelta(days=20),
            data_prevista_devolucao=hoje - timedelta(days=5),
            devolvido=False
        )
        assert emprestimo.dias_atraso() == 5
    
    def test_calcular_multa(self):
        """Testa cálculo de multa"""
        hoje = date.today()
        emprestimo = Emprestimo(
            livro_id=1,
            usuario_id=1,
            data_emprestimo=hoje - timedelta(days=20),
            data_prevista_devolucao=hoje - timedelta(days=5),
            devolvido=False
        )
        multa = emprestimo.calcular_multa(multa_diaria=2.50)
        assert multa == 12.50  # 5 dias * 2.50


class TestAutor:
    """Testes para modelo Autor"""
    
    def test_calcular_idade_autor(self):
        """Testa cálculo de idade do autor"""
        from datetime import date
        hoje = date.today()
        ano_nascimento = hoje.year - 50
        autor = Autor(
            nome="Teste",
            data_nascimento=date(ano_nascimento, 1, 1)
        )
        # Idade pode variar em 1 ano dependendo do dia atual
        assert autor.idade() in [49, 50]
    
    def test_calcular_idade_sem_data_nascimento(self):
        """Testa cálculo de idade quando não há data de nascimento"""
        autor = Autor(nome="Teste")
        assert autor.idade() is None


"""
Testes unitários para serviços
"""
import pytest
from datetime import date, timedelta

from src.services.livro_service import LivroService
from src.services.usuario_service import UsuarioService
from src.services.emprestimo_service import EmprestimoService
from src.models.livro import Livro
from src.models.usuario import Usuario
from src.exceptions.biblioteca_exceptions import (
    EntidadeNaoEncontradaException,
    ValidacaoException,
    LivroIndisponivelException,
    LimiteEmprestimosException,
    IdadeMinimaException
)


class TestLivroService:
    """Testes para LivroService"""
    
    def test_criar_livro_sucesso(self, livro_service, autor, categoria):
        """Testa criação de livro com sucesso"""
        livro = Livro(
            titulo="Novo Livro",
            autor_id=autor.id,
            categoria_id=categoria.id,
            quantidade_total=3
        )
        livro_criado = livro_service.criar_livro(livro)
        assert livro_criado.id is not None
        assert livro_criado.titulo == "Novo Livro"
    
    def test_criar_livro_autor_inexistente(self, livro_service, categoria):
        """Testa criação de livro com autor inexistente"""
        livro = Livro(
            titulo="Novo Livro",
            autor_id=99999,
            categoria_id=categoria.id,
            quantidade_total=3
        )
        with pytest.raises(EntidadeNaoEncontradaException):
            livro_service.criar_livro(livro)
    
    def test_buscar_por_id_sucesso(self, livro_service, livro):
        """Testa busca de livro por ID"""
        livro_encontrado = livro_service.buscar_por_id(livro.id)
        assert livro_encontrado.id == livro.id
    
    def test_buscar_por_id_nao_encontrado(self, livro_service):
        """Testa busca de livro inexistente"""
        with pytest.raises(EntidadeNaoEncontradaException):
            livro_service.buscar_por_id(99999)
    
    def test_atualizar_livro(self, livro_service, livro):
        """Testa atualização de livro"""
        dados = {"titulo": "Título Atualizado"}
        livro_atualizado = livro_service.atualizar_livro(livro.id, dados)
        assert livro_atualizado.titulo == "Título Atualizado"
    
    def test_deletar_livro(self, livro_service, livro):
        """Testa deleção de livro"""
        resultado = livro_service.deletar_livro(livro.id)
        assert resultado is True
        with pytest.raises(EntidadeNaoEncontradaException):
            livro_service.buscar_por_id(livro.id)


class TestUsuarioService:
    """Testes para UsuarioService"""
    
    def test_criar_usuario_sucesso(self, usuario_service):
        """Testa criação de usuário com sucesso"""
        usuario = Usuario(
            nome="Novo Usuário",
            email="novo@example.com",
            
            data_nascimento=date(1990, 1, 1)
        )
        usuario_criado = usuario_service.criar_usuario(usuario)
        assert usuario_criado.id is not None
    
    
    def test_criar_usuario_email_duplicado(self, usuario_service, usuario):
        """Testa criação de usuário com email duplicado"""
        novo_usuario = Usuario(
            nome="Outro Usuário",
            email=usuario.email,
            
            data_nascimento=date(1990, 1, 1)
        )
        with pytest.raises(ValidacaoException):
            usuario_service.criar_usuario(novo_usuario)
    
    def test_criar_usuario_idade_insuficiente(self, usuario_service):
        """Testa criação de usuário com idade insuficiente"""
        usuario = Usuario(
            nome="Usuário Jovem",
            email="jovem@example.com",
            
            data_nascimento=date(2020, 1, 1)  # Menos de 12 anos
        )
        with pytest.raises(ValidacaoException):
            usuario_service.criar_usuario(usuario)
    
    def test_buscar_por_id_sucesso(self, usuario_service, usuario):
        """Testa busca de usuário por ID"""
        usuario_encontrado = usuario_service.buscar_por_id(usuario.id)
        assert usuario_encontrado.id == usuario.id
    
    def test_atualizar_usuario(self, usuario_service, usuario):
        """Testa atualização de usuário"""
        dados = {"nome": "Nome Atualizado"}
        usuario_atualizado = usuario_service.atualizar_usuario(usuario.id, dados)
        assert usuario_atualizado.nome == "Nome Atualizado"


class TestEmprestimoService:
    """Testes para EmprestimoService"""
    
    def test_criar_emprestimo_sucesso(self, emprestimo_service, livro, usuario):
        """Testa criação de empréstimo com sucesso"""
        emprestimo = emprestimo_service.criar_emprestimo(livro.id, usuario.id)
        assert emprestimo.id is not None
        assert emprestimo.livro_id == livro.id
        assert emprestimo.usuario_id == usuario.id
    
    def test_criar_emprestimo_livro_inexistente(self, emprestimo_service, usuario):
        """Testa criação de empréstimo com livro inexistente"""
        with pytest.raises(EntidadeNaoEncontradaException):
            emprestimo_service.criar_emprestimo(99999, usuario.id)
    
    def test_criar_emprestimo_livro_indisponivel(self, emprestimo_service, livro, usuario):
        """Testa criação de empréstimo com livro indisponível"""
        livro.quantidade_disponivel = 0
        livro.disponivel = False
        with pytest.raises(LivroIndisponivelException):
            emprestimo_service.criar_emprestimo(livro.id, usuario.id)
    
    def test_criar_emprestimo_limite_excedido(self, emprestimo_service, livro, usuario, db_session):
        """Testa criação de empréstimo quando limite é excedido"""
        # Cria 5 empréstimos ativos
        for i in range(5):
            outro_livro = Livro(
                titulo=f"Livro {i}",
                autor_id=1,
                quantidade_total=5,
                quantidade_disponivel=5
            )
            db_session.add(outro_livro)
            db_session.commit()
            
            emprestimo_service.criar_emprestimo(outro_livro.id, usuario.id)
        
        # Tenta criar mais um
        with pytest.raises(LimiteEmprestimosException):
            emprestimo_service.criar_emprestimo(livro.id, usuario.id)
    
    def test_criar_emprestimo_idade_insuficiente(self, emprestimo_service, livro, db_session):
        """Testa criação de empréstimo com idade insuficiente"""
        usuario_jovem = Usuario(
            nome="Usuário Jovem",
            email="jovem@example.com",
            
            data_nascimento=date(2020, 1, 1),  # Menos de 12 anos
            ativo=True
        )
        db_session.add(usuario_jovem)
        db_session.commit()
        
        with pytest.raises(IdadeMinimaException):
            emprestimo_service.criar_emprestimo(livro.id, usuario_jovem.id)
    
    def test_devolver_emprestimo_sucesso(self, emprestimo_service, emprestimo):
        """Testa devolução de empréstimo"""
        emprestimo_devolvido = emprestimo_service.devolver_emprestimo(emprestimo.id)
        assert emprestimo_devolvido.devolvido is True
        assert emprestimo_devolvido.data_devolucao is not None
    
    def test_calcular_multa_emprestimo_atrasado(self, emprestimo_service, db_session, livro, usuario):
        """Testa cálculo de multa para empréstimo atrasado"""
        from src.models.emprestimo import Emprestimo
        emprestimo_atrasado = Emprestimo(
            livro_id=livro.id,
            usuario_id=usuario.id,
            data_emprestimo=date.today() - timedelta(days=20),
            data_prevista_devolucao=date.today() - timedelta(days=5),
            devolvido=False
        )
        db_session.add(emprestimo_atrasado)
        db_session.commit()
        
        multa = emprestimo_service.calcular_multa_emprestimo(emprestimo_atrasado.id)
        assert multa == 12.50  # 5 dias * 2.50


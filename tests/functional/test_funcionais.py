"""
Testes funcionais (caixa-preta)
"""
import pytest
from datetime import date, timedelta

from src.services.livro_service import LivroService
from src.services.usuario_service import UsuarioService
from src.services.emprestimo_service import EmprestimoService
from src.models.livro import Livro
from src.models.usuario import Usuario
from src.models.autor import Autor


class TestFuncionalidadesEmprestimo:
    """Testes funcionais para funcionalidade de empréstimo"""
    
    def test_emprestar_livro_disponivel_para_usuario_valido(self, db_session):
        """Cenário: Emprestar livro disponível para usuário válido"""
        # Setup
        autor = Autor(nome="Autor", nacionalidade="BR")
        db_session.add(autor)
        db_session.commit()
        
        livro = Livro(titulo="Livro", autor_id=autor.id, quantidade_total=5, quantidade_disponivel=5)
        db_session.add(livro)
        db_session.commit()
        
        usuario = Usuario(
            nome="Usuário",
            email="user@example.com",
            
            data_nascimento=date(1990, 1, 1),
            ativo=True
        )
        db_session.add(usuario)
        db_session.commit()
        
        # Execução
        emprestimo_service = EmprestimoService(db_session)
        emprestimo = emprestimo_service.criar_emprestimo(livro.id, usuario.id)
        
        # Verificação
        assert emprestimo.id is not None
        assert emprestimo.livro_id == livro.id
        assert emprestimo.usuario_id == usuario.id
        assert emprestimo.devolvido is False
    
    def test_nao_emprestar_livro_indisponivel(self, db_session):
        """Cenário: Tentar emprestar livro indisponível"""
        autor = Autor(nome="Autor", nacionalidade="BR")
        db_session.add(autor)
        db_session.commit()
        
        livro = Livro(titulo="Livro", autor_id=autor.id, quantidade_total=5, quantidade_disponivel=0, disponivel=False)
        db_session.add(livro)
        db_session.commit()
        
        usuario = Usuario(
            nome="Usuário",
            email="user@example.com",
            
            data_nascimento=date(1990, 1, 1),
            ativo=True
        )
        db_session.add(usuario)
        db_session.commit()
        
        emprestimo_service = EmprestimoService(db_session)
        
        with pytest.raises(Exception):  # LivroIndisponivelException
            emprestimo_service.criar_emprestimo(livro.id, usuario.id)
    
    def test_nao_emprestar_para_usuario_com_limite_excedido(self, db_session):
        """Cenário: Tentar emprestar para usuário que excedeu limite"""
        autor = Autor(nome="Autor", nacionalidade="BR")
        db_session.add(autor)
        db_session.commit()
        
        usuario = Usuario(
            nome="Usuário",
            email="user@example.com",
            
            data_nascimento=date(1990, 1, 1),
            ativo=True
        )
        db_session.add(usuario)
        db_session.commit()
        
        # Cria 5 livros e empréstimos
        emprestimo_service = EmprestimoService(db_session)
        for i in range(5):
            livro = Livro(titulo=f"Livro {i}", autor_id=autor.id, quantidade_total=5, quantidade_disponivel=5)
            db_session.add(livro)
            db_session.commit()
            emprestimo_service.criar_emprestimo(livro.id, usuario.id)
        
        # Tenta criar mais um
        livro_extra = Livro(titulo="Livro Extra", autor_id=autor.id, quantidade_total=5, quantidade_disponivel=5)
        db_session.add(livro_extra)
        db_session.commit()
        
        with pytest.raises(Exception):  # LimiteEmprestimosException
            emprestimo_service.criar_emprestimo(livro_extra.id, usuario.id)
    
    def test_devolver_emprestimo_no_prazo(self, db_session):
        """Cenário: Devolver empréstimo dentro do prazo"""
        autor = Autor(nome="Autor", nacionalidade="BR")
        db_session.add(autor)
        db_session.commit()
        
        livro = Livro(titulo="Livro", autor_id=autor.id, quantidade_total=5, quantidade_disponivel=4)
        db_session.add(livro)
        db_session.commit()
        
        usuario = Usuario(
            nome="Usuário",
            email="user@example.com",
            
            data_nascimento=date(1990, 1, 1)
        )
        db_session.add(usuario)
        db_session.commit()
        
        emprestimo_service = EmprestimoService(db_session)
        emprestimo = emprestimo_service.criar_emprestimo(livro.id, usuario.id)
        
        emprestimo_devolvido = emprestimo_service.devolver_emprestimo(emprestimo.id)
        
        assert emprestimo_devolvido.devolvido is True
        assert emprestimo_devolvido.multa == 0.0
    
    def test_devolver_emprestimo_atrasado_com_multa(self, db_session):
        """Cenário: Devolver empréstimo atrasado com cálculo de multa"""
        autor = Autor(nome="Autor", nacionalidade="BR")
        db_session.add(autor)
        db_session.commit()
        
        livro = Livro(titulo="Livro", autor_id=autor.id, quantidade_total=5, quantidade_disponivel=4)
        db_session.add(livro)
        db_session.commit()
        
        usuario = Usuario(
            nome="Usuário",
            email="user@example.com",
            
            data_nascimento=date(1990, 1, 1)
        )
        db_session.add(usuario)
        db_session.commit()
        
        emprestimo_service = EmprestimoService(db_session)
        emprestimo = emprestimo_service.criar_emprestimo(livro.id, usuario.id)
        
        # Simula atraso
        emprestimo.data_prevista_devolucao = date.today() - timedelta(days=5)
        db_session.commit()
        
        emprestimo_devolvido = emprestimo_service.devolver_emprestimo(emprestimo.id)
        
        assert emprestimo_devolvido.devolvido is True
        assert emprestimo_devolvido.multa > 0
    
    def test_buscar_livros_disponiveis(self, db_session):
        """Cenário: Buscar apenas livros disponíveis"""
        autor = Autor(nome="Autor", nacionalidade="BR")
        db_session.add(autor)
        db_session.commit()
        
        livro1 = Livro(titulo="Livro 1", autor_id=autor.id, quantidade_total=5, quantidade_disponivel=5, disponivel=True)
        livro2 = Livro(titulo="Livro 2", autor_id=autor.id, quantidade_total=5, quantidade_disponivel=0, disponivel=False)
        db_session.add_all([livro1, livro2])
        db_session.commit()
        
        livro_service = LivroService(db_session)
        livros_disponiveis = livro_service.buscar_disponiveis()
        
        assert len(livros_disponiveis) >= 1
        assert all(l.esta_disponivel() for l in livros_disponiveis)
    
    def test_buscar_emprestimos_atrasados(self, db_session):
        """Cenário: Buscar empréstimos atrasados"""
        autor = Autor(nome="Autor", nacionalidade="BR")
        db_session.add(autor)
        db_session.commit()
        
        livro = Livro(titulo="Livro", autor_id=autor.id, quantidade_total=5, quantidade_disponivel=5)
        db_session.add(livro)
        db_session.commit()
        
        usuario = Usuario(
            nome="Usuário",
            email="user@example.com",
            
            data_nascimento=date(1990, 1, 1)
        )
        db_session.add(usuario)
        db_session.commit()
        
        emprestimo_service = EmprestimoService(db_session)
        emprestimo = emprestimo_service.criar_emprestimo(livro.id, usuario.id)
        
        # Simula atraso
        emprestimo.data_prevista_devolucao = date.today() - timedelta(days=3)
        db_session.commit()
        
        emprestimos_atrasados = emprestimo_service.buscar_atrasados()
        
        assert len(emprestimos_atrasados) >= 1
        assert any(e.id == emprestimo.id for e in emprestimos_atrasados)
    
    def test_validar_criacao_usuario_com_dados_validos(self, db_session):
        """Cenário: Criar usuário com todos os dados válidos"""
        usuario_service = UsuarioService(db_session)
        usuario = Usuario(
            nome="Usuário Teste",
            email="teste@example.com",
            data_nascimento=date(1990, 1, 1)
        )
        
        usuario_criado = usuario_service.criar_usuario(usuario)
        
        assert usuario_criado.id is not None
        assert usuario_criado.nome == "Usuário Teste"
        assert usuario_criado.email == "teste@example.com"


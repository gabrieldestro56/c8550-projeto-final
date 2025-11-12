"""
Testes de integração
"""
import pytest
from datetime import date, timedelta

from src.services.livro_service import LivroService
from src.services.usuario_service import UsuarioService
from src.services.emprestimo_service import EmprestimoService
from src.services.autor_service import AutorService
from src.services.categoria_service import CategoriaService
from src.models.livro import Livro
from src.models.usuario import Usuario
from src.models.autor import Autor
from src.models.categoria import Categoria


class TestIntegracaoCompleta:
    """Testes de integração de fluxos completos"""
    
    def test_fluxo_completo_emprestimo(self, db_session):
        """Testa fluxo completo: criar autor, categoria, livro, usuário e empréstimo"""
        # Cria autor
        autor_service = AutorService(db_session)
        autor = Autor(nome="Autor Teste", nacionalidade="Brasileiro")
        autor = autor_service.criar_autor(autor)
        
        # Cria categoria
        categoria_service = CategoriaService(db_session)
        categoria = Categoria(nome="Ficção", descricao="Livros de ficção")
        categoria = categoria_service.criar_categoria(categoria)
        
        # Cria livro
        livro_service = LivroService(db_session)
        livro = Livro(
            titulo="Livro Teste",
            autor_id=autor.id,
            categoria_id=categoria.id,
            quantidade_total=5
        )
        livro = livro_service.criar_livro(livro)
        
        # Cria usuário
        usuario_service = UsuarioService(db_session)
        usuario = Usuario(
            nome="Usuário Teste",
            email="teste@example.com",
            
            data_nascimento=date(1990, 1, 1)
        )
        usuario = usuario_service.criar_usuario(usuario)
        
        # Cria empréstimo
        emprestimo_service = EmprestimoService(db_session)
        emprestimo = emprestimo_service.criar_emprestimo(livro.id, usuario.id)
        
        assert emprestimo.id is not None
        assert emprestimo.livro_id == livro.id
        assert emprestimo.usuario_id == usuario.id
        
        # Verifica que livro foi atualizado
        livro_atualizado = livro_service.buscar_por_id(livro.id)
        assert livro_atualizado.quantidade_disponivel == 4
    
    def test_fluxo_emprestimo_e_devolucao(self, db_session):
        """Testa fluxo completo de empréstimo e devolução"""
        # Setup
        autor = Autor(nome="Autor", nacionalidade="BR")
        db_session.add(autor)
        db_session.commit()
        
        livro = Livro(titulo="Livro", autor_id=autor.id, quantidade_total=3, quantidade_disponivel=3)
        db_session.add(livro)
        db_session.commit()
        
        usuario = Usuario(
            nome="Usuário",
            email="user@example.com",
            
            data_nascimento=date(1990, 1, 1)
        )
        db_session.add(usuario)
        db_session.commit()
        
        # Empréstimo
        emprestimo_service = EmprestimoService(db_session)
        emprestimo = emprestimo_service.criar_emprestimo(livro.id, usuario.id)
        
        # Verifica disponibilidade
        livro_service = LivroService(db_session)
        livro_atualizado = livro_service.buscar_por_id(livro.id)
        assert livro_atualizado.quantidade_disponivel == 2
        
        # Devolução
        emprestimo_devolvido = emprestimo_service.devolver_emprestimo(emprestimo.id)
        assert emprestimo_devolvido.devolvido is True
        
        # Verifica disponibilidade após devolução
        livro_final = livro_service.buscar_por_id(livro.id)
        assert livro_final.quantidade_disponivel == 3
    
    def test_integracao_repositorio_servico(self, db_session):
        """Testa integração entre repositório e serviço"""
        autor = Autor(nome="Autor", nacionalidade="BR")
        db_session.add(autor)
        db_session.commit()
        
        livro_service = LivroService(db_session)
        livro = Livro(titulo="Teste", autor_id=autor.id, quantidade_total=5)
        livro = livro_service.criar_livro(livro)
        
        # Busca usando repositório diretamente
        from src.repositories.livro_repository import LivroRepository
        repo = LivroRepository(db_session)
        livro_encontrado = repo.buscar_por_id(livro.id)
        
        assert livro_encontrado is not None
        assert livro_encontrado.titulo == "Teste"
    
    def test_integracao_multiplos_emprestimos(self, db_session):
        """Testa integração com múltiplos empréstimos"""
        autor = Autor(nome="Autor", nacionalidade="BR")
        db_session.add(autor)
        db_session.commit()
        
        livro1 = Livro(titulo="Livro 1", autor_id=autor.id, quantidade_total=5)
        livro2 = Livro(titulo="Livro 2", autor_id=autor.id, quantidade_total=5)
        db_session.add_all([livro1, livro2])
        db_session.commit()
        
        usuario = Usuario(
            nome="Usuário",
            email="user@example.com",
            
            data_nascimento=date(1990, 1, 1)
        )
        db_session.add(usuario)
        db_session.commit()
        
        emprestimo_service = EmprestimoService(db_session)
        
        # Cria dois empréstimos
        emp1 = emprestimo_service.criar_emprestimo(livro1.id, usuario.id)
        emp2 = emprestimo_service.criar_emprestimo(livro2.id, usuario.id)
        
        assert emp1.id != emp2.id
        
        # Busca empréstimos do usuário
        emprestimos = emprestimo_service.buscar_por_usuario(usuario.id)
        assert len(emprestimos) == 2
    
    def test_integracao_busca_com_filtros(self, db_session):
        """Testa integração de busca com filtros"""
        autor = Autor(nome="Autor", nacionalidade="BR")
        db_session.add(autor)
        db_session.commit()
        
        livro1 = Livro(titulo="Python Avançado", autor_id=autor.id, quantidade_total=5, disponivel=True)
        livro2 = Livro(titulo="Java Básico", autor_id=autor.id, quantidade_total=5, disponivel=False)
        db_session.add_all([livro1, livro2])
        db_session.commit()
        
        livro_service = LivroService(db_session)
        
        # Busca com filtro de disponibilidade
        livros_disponiveis = livro_service.buscar_com_filtros({"disponivel": True})
        assert len(livros_disponiveis) >= 1
        assert all(l.disponivel for l in livros_disponiveis)
        
        # Busca com filtro de título
        livros_python = livro_service.buscar_com_filtros({"titulo": {"like": "%Python%"}})
        assert len(livros_python) >= 1
        assert any("Python" in l.titulo for l in livros_python)
    
    def test_integracao_atualizacao_cascata(self, db_session):
        """Testa integração de atualização em cascata"""
        autor = Autor(nome="Autor", nacionalidade="BR")
        db_session.add(autor)
        db_session.commit()
        
        livro = Livro(titulo="Livro", autor_id=autor.id, quantidade_total=5)
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
        
        # Atualiza livro
        livro_service = LivroService(db_session)
        livro_service.atualizar_livro(livro.id, {"titulo": "Livro Atualizado"})
        
        # Verifica que empréstimo ainda referencia o livro
        emprestimo_atualizado = emprestimo_service.buscar_por_id(emprestimo.id)
        assert emprestimo_atualizado.livro.titulo == "Livro Atualizado"
    
    def test_integracao_validacao_completa(self, db_session):
        """Testa integração de validações completas"""
        autor = Autor(nome="Autor", nacionalidade="BR")
        db_session.add(autor)
        db_session.commit()
        
        livro = Livro(titulo="Livro", autor_id=autor.id, quantidade_total=5)
        db_session.add(livro)
        db_session.commit()
        
        usuario_service = UsuarioService(db_session)
        
        # Tenta criar usuário com dados inválidos
        usuario_invalido = Usuario(
            nome="Usuário",
            email="email_invalido",  # Email inválido
            # CPF inválido
            data_nascimento=date(2020, 1, 1)  # Idade insuficiente
        )
        
        with pytest.raises(Exception):  # Pode ser ValidacaoException
            usuario_service.criar_usuario(usuario_invalido)
    
    def test_integracao_calculo_multa(self, db_session):
        """Testa integração de cálculo de multa"""
        autor = Autor(nome="Autor", nacionalidade="BR")
        db_session.add(autor)
        db_session.commit()
        
        livro = Livro(titulo="Livro", autor_id=autor.id, quantidade_total=5)
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
        
        # Calcula multa
        multa = emprestimo_service.calcular_multa_emprestimo(emprestimo.id)
        assert multa == 12.50  # 5 dias * 2.50
    
    def test_integracao_listagem_com_paginacao(self, db_session):
        """Testa integração de listagem com paginação"""
        autor = Autor(nome="Autor", nacionalidade="BR")
        db_session.add(autor)
        db_session.commit()
        
        # Cria múltiplos livros
        livros = []
        for i in range(15):
            livro = Livro(titulo=f"Livro {i}", autor_id=autor.id, quantidade_total=5)
            livros.append(livro)
        db_session.add_all(livros)
        db_session.commit()
        
        livro_service = LivroService(db_session)
        
        # Primeira página
        pagina1 = livro_service.listar_todos(skip=0, limit=10)
        assert len(pagina1) == 10
        
        # Segunda página
        pagina2 = livro_service.listar_todos(skip=10, limit=10)
        assert len(pagina2) == 5


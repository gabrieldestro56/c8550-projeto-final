"""
Configuração compartilhada para testes
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from src.database.base import Base
from src.models.livro import Livro
from src.models.usuario import Usuario
from src.models.emprestimo import Emprestimo
from src.models.autor import Autor
from src.models.categoria import Categoria
from src.repositories.livro_repository import LivroRepository
from src.repositories.usuario_repository import UsuarioRepository
from src.repositories.emprestimo_repository import EmprestimoRepository
from src.repositories.autor_repository import AutorRepository
from src.repositories.categoria_repository import CategoriaRepository
from src.services.livro_service import LivroService
from src.services.usuario_service import UsuarioService
from src.services.emprestimo_service import EmprestimoService
from src.services.autor_service import AutorService
from src.services.categoria_service import CategoriaService
from datetime import date, timedelta


@pytest.fixture(scope="function")
def db_session():
    """
    Cria uma sessão de banco de dados em memória para testes
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    
    yield session
    
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def autor(db_session: Session) -> Autor:
    """Cria um autor para testes"""
    autor = Autor(
        nome="Machado de Assis",
        nacionalidade="Brasileiro",
        data_nascimento=date(1839, 6, 21),
        biografia="Escritor brasileiro"
    )
    db_session.add(autor)
    db_session.commit()
    db_session.refresh(autor)
    return autor


@pytest.fixture
def categoria(db_session: Session) -> Categoria:
    """Cria uma categoria para testes"""
    categoria = Categoria(
        nome="Romance",
        descricao="Romances literários"
    )
    db_session.add(categoria)
    db_session.commit()
    db_session.refresh(categoria)
    return categoria


@pytest.fixture
def livro(db_session: Session, autor: Autor, categoria: Categoria) -> Livro:
    """Cria um livro para testes"""
    livro = Livro(
        titulo="Dom Casmurro",
        ano_publicacao=1899,
        editora="Editora Globo",
        numero_paginas=256,
        autor_id=autor.id,
        categoria_id=categoria.id,
        quantidade_total=5,
        quantidade_disponivel=5,
        disponivel=True
    )
    db_session.add(livro)
    db_session.commit()
    db_session.refresh(livro)
    return livro


@pytest.fixture
def usuario(db_session: Session) -> Usuario:
    """Cria um usuário para testes"""
    usuario = Usuario(
        nome="João Silva",
        email="joao@example.com",
        data_nascimento=date(1990, 1, 1),
        ativo=True
    )
    db_session.add(usuario)
    db_session.commit()
    db_session.refresh(usuario)
    return usuario


@pytest.fixture
def emprestimo(db_session: Session, livro: Livro, usuario: Usuario) -> Emprestimo:
    """Cria um empréstimo para testes"""
    # Atualiza quantidade disponível do livro
    livro.quantidade_disponivel -= 1
    if livro.quantidade_disponivel == 0:
        livro.disponivel = False
    db_session.commit()
    
    emprestimo = Emprestimo(
        livro_id=livro.id,
        usuario_id=usuario.id,
        data_emprestimo=date.today(),
        data_prevista_devolucao=date.today() + timedelta(days=14),
        devolvido=False,
        multa=0.0
    )
    db_session.add(emprestimo)
    db_session.commit()
    db_session.refresh(emprestimo)
    return emprestimo


@pytest.fixture
def livro_repo(db_session: Session) -> LivroRepository:
    """Cria um repositório de livros"""
    return LivroRepository(db_session)


@pytest.fixture
def usuario_repo(db_session: Session) -> UsuarioRepository:
    """Cria um repositório de usuários"""
    return UsuarioRepository(db_session)


@pytest.fixture
def emprestimo_repo(db_session: Session) -> EmprestimoRepository:
    """Cria um repositório de empréstimos"""
    return EmprestimoRepository(db_session)


@pytest.fixture
def autor_repo(db_session: Session) -> AutorRepository:
    """Cria um repositório de autores"""
    return AutorRepository(db_session)


@pytest.fixture
def categoria_repo(db_session: Session) -> CategoriaRepository:
    """Cria um repositório de categorias"""
    return CategoriaRepository(db_session)


@pytest.fixture
def livro_service(db_session: Session, livro_repo: LivroRepository) -> LivroService:
    """Cria um serviço de livros"""
    return LivroService(db_session, livro_repo=livro_repo)


@pytest.fixture
def usuario_service(db_session: Session, usuario_repo: UsuarioRepository) -> UsuarioService:
    """Cria um serviço de usuários"""
    return UsuarioService(db_session, usuario_repo=usuario_repo)


@pytest.fixture
def emprestimo_service(
    db_session: Session,
    emprestimo_repo: EmprestimoRepository,
    livro_repo: LivroRepository,
    usuario_repo: UsuarioRepository
) -> EmprestimoService:
    """Cria um serviço de empréstimos"""
    return EmprestimoService(
        db_session,
        emprestimo_repo=emprestimo_repo,
        livro_repo=livro_repo,
        usuario_repo=usuario_repo
    )


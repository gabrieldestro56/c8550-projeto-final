"""
Dependências da API (injeção de dependências)
"""
from sqlalchemy.orm import Session
from fastapi import Depends

from src.database.config import db_config
from src.services.livro_service import LivroService
from src.services.usuario_service import UsuarioService
from src.services.emprestimo_service import EmprestimoService
from src.services.autor_service import AutorService
from src.services.categoria_service import CategoriaService


def get_db() -> Session:
    """
    Dependency para obter sessão do banco de dados
    
    Yields:
        Sessão do banco de dados
    """
    db = db_config.get_session()
    try:
        yield db
    finally:
        db.close()


def get_livro_service(db: Session = Depends(get_db)) -> LivroService:
    """Dependency para obter serviço de livros"""
    return LivroService(db)


def get_usuario_service(db: Session = Depends(get_db)) -> UsuarioService:
    """Dependency para obter serviço de usuários"""
    return UsuarioService(db)


def get_emprestimo_service(db: Session = Depends(get_db)) -> EmprestimoService:
    """Dependency para obter serviço de empréstimos"""
    return EmprestimoService(db)


def get_autor_service(db: Session = Depends(get_db)) -> AutorService:
    """Dependency para obter serviço de autores"""
    return AutorService(db)


def get_categoria_service(db: Session = Depends(get_db)) -> CategoriaService:
    """Dependency para obter serviço de categorias"""
    return CategoriaService(db)


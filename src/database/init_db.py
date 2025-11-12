"""
Script para inicializar o banco de dados
"""
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.database.config import db_config
from src.database.base import Base
from src.models.livro import Livro
from src.models.usuario import Usuario
from src.models.emprestimo import Emprestimo
from src.models.autor import Autor
from src.models.categoria import Categoria


def init_database() -> None:
    """
    Inicializa o banco de dados criando todas as tabelas
    """
    print("Criando tabelas do banco de dados...")
    Base.metadata.create_all(bind=db_config.engine)
    print("Banco de dados inicializado com sucesso!")


if __name__ == "__main__":
    init_database()


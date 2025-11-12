"""
Testes unitários para módulos de database
"""
import pytest
import tempfile
import os
from pathlib import Path

from src.database.config import DatabaseConfig
from src.database.base import Base
from src.models.livro import Livro


class TestDatabaseConfig:
    """Testes para DatabaseConfig"""
    
    def test_criar_config_com_arquivo(self):
        """Testa criação de configuração com arquivo"""
        # Cria arquivo temporário de config
        config_data = {
            "database": {
                "url": "sqlite:///:memory:",
                "echo": False
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            import json
            json.dump(config_data, f)
            config_path = f.name
        
        try:
            config = DatabaseConfig(config_path)
            assert config.config is not None
            assert config.engine is not None
            assert config.SessionLocal is not None
        finally:
            if os.path.exists(config_path):
                os.remove(config_path)
    
    def test_criar_config_sem_arquivo(self):
        """Testa criação de configuração sem arquivo (usa fallback)"""
        # Usa um caminho que não existe
        config = DatabaseConfig("config/nao_existe.json")
        assert config.config is not None
        assert "database" in config.config
        assert config.engine is not None
    
    def test_get_session(self):
        """Testa obtenção de sessão"""
        config = DatabaseConfig()
        session = config.get_session()
        assert session is not None
        session.close()


class TestInitDatabase:
    """Testes para inicialização do banco"""
    
    def test_init_database_cria_tabelas(self):
        """Testa que init_database cria as tabelas"""
        from src.database.config import db_config
        
        # Limpa tabelas existentes
        Base.metadata.drop_all(bind=db_config.engine)
        
        # Cria tabelas
        Base.metadata.create_all(bind=db_config.engine)
        
        # Verifica que as tabelas foram criadas
        from sqlalchemy import inspect
        inspector = inspect(db_config.engine)
        tabelas = inspector.get_table_names()
        
        assert "livros" in tabelas
        assert "usuarios" in tabelas
        assert "emprestimos" in tabelas
        assert "autores" in tabelas
        assert "categorias" in tabelas


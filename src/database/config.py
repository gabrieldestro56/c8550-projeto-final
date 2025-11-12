"""
Configuração do banco de dados
"""
import json
import os
from pathlib import Path
from typing import Dict, Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()


class DatabaseConfig:
    """Classe para gerenciar configurações do banco de dados"""
    
    def __init__(self, config_path: str = "config/config.json") -> None:
        """
        Inicializa a configuração do banco de dados
        
        Args:
            config_path: Caminho para o arquivo de configuração JSON
        """
        self.config_path = config_path
        self.config: Dict[str, Any] = self._load_config()
        self.engine = self._create_engine()
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Carrega configurações do arquivo JSON ou variáveis de ambiente
        
        Returns:
            Dicionário com as configurações
        """
        config_file = Path(self.config_path)
        
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Fallback para variáveis de ambiente
        return {
            "database": {
                "url": os.getenv("DATABASE_URL", "sqlite:///./biblioteca.db"),
                "echo": os.getenv("DATABASE_ECHO", "false").lower() == "true"
            }
        }
    
    def _create_engine(self):
        """
        Cria a engine do SQLAlchemy
        
        Returns:
            Engine do SQLAlchemy
        """
        db_url = self.config.get("database", {}).get("url")
        if not db_url:
            db_url = os.getenv("DATABASE_URL", "sqlite:///./biblioteca.db")
        
        echo = self.config.get("database", {}).get("echo", False)
        return create_engine(db_url, echo=echo, connect_args={"check_same_thread": False} if "sqlite" in db_url else {})
    
    def get_session(self) -> Session:
        """
        Retorna uma sessão do banco de dados
        
        Returns:
            Sessão do SQLAlchemy
        """
        return self.SessionLocal()


# Instância global da configuração
db_config = DatabaseConfig()


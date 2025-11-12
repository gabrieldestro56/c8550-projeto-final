"""
Sistema de logging
"""
import logging
import json
import os
from pathlib import Path
from typing import Optional
from logging.handlers import RotatingFileHandler


class LoggerConfig:
    """Configuração do sistema de logging"""
    
    _instance: Optional['LoggerConfig'] = None
    _logger: Optional[logging.Logger] = None
    
    def __new__(cls) -> 'LoggerConfig':
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        """Inicializa o logger se ainda não foi inicializado"""
        if self._logger is None:
            self._setup_logger()
    
    def _load_config(self) -> dict:
        """
        Carrega configuração de logging
        
        Returns:
            Dicionário com configurações
        """
        config_file = Path("config/config.json")
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get("logging", {})
        
        # Fallback para variáveis de ambiente
        return {
            "level": os.getenv("LOG_LEVEL", "INFO"),
            "file": os.getenv("LOG_FILE", "logs/biblioteca.log"),
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    
    def _setup_logger(self) -> None:
        """Configura o logger"""
        config = self._load_config()
        
        # Cria diretório de logs se não existir
        log_file = Path(config.get("file", "logs/biblioteca.log"))
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Configura nível de log
        log_level = getattr(logging, config.get("level", "INFO").upper(), logging.INFO)
        
        # Cria logger
        self._logger = logging.getLogger("biblioteca")
        self._logger.setLevel(log_level)
        
        # Evita duplicação de handlers
        if self._logger.handlers:
            return
        
        # Handler para arquivo
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(log_level)
        
        # Handler para console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        
        # Formato
        formatter = logging.Formatter(config.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Adiciona handlers
        self._logger.addHandler(file_handler)
        self._logger.addHandler(console_handler)
    
    def get_logger(self, name: str = "biblioteca") -> logging.Logger:
        """
        Retorna um logger
        
        Args:
            name: Nome do logger
        
        Returns:
            Logger configurado
        """
        if name == "biblioteca":
            return self._logger
        
        # Cria logger filho
        logger = logging.getLogger(f"biblioteca.{name}")
        if not logger.handlers:
            # Herda configuração do logger pai
            logger.parent = self._logger
        return logger


def get_logger(name: str = "biblioteca") -> logging.Logger:
    """
    Função auxiliar para obter um logger
    
    Args:
        name: Nome do logger
    
    Returns:
        Logger configurado
    """
    config = LoggerConfig()
    return config.get_logger(name)


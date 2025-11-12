"""
Utilitário para manipulação de arquivos
"""
import json
import csv
from pathlib import Path
from typing import List, Dict, Any
from datetime import date, datetime

from src.utils.logger import get_logger


class FileHandler:
    """Classe para manipulação de arquivos"""
    
    def __init__(self) -> None:
        """Inicializa o handler"""
        self.logger = get_logger("FileHandler")
    
    def exportar_emprestimos_json(self, emprestimos: List[Dict[str, Any]], arquivo: str) -> None:
        """
        Exporta empréstimos para arquivo JSON
        
        Args:
            emprestimos: Lista de empréstimos (dicionários)
            arquivo: Caminho do arquivo de saída
        """
        self.logger.info(f"Exportando {len(emprestimos)} empréstimos para {arquivo}")
        
        # Converte datas para strings
        dados_export = []
        for emp in emprestimos:
            emp_copy = emp.copy()
            for key, value in emp_copy.items():
                if isinstance(value, (date, datetime)):
                    emp_copy[key] = value.isoformat()
            dados_export.append(emp_copy)
        
        arquivo_path = Path(arquivo)
        arquivo_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(arquivo_path, 'w', encoding='utf-8') as f:
            json.dump(dados_export, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Exportação concluída: {arquivo}")
    
    def importar_emprestimos_json(self, arquivo: str) -> List[Dict[str, Any]]:
        """
        Importa empréstimos de arquivo JSON
        
        Args:
            arquivo: Caminho do arquivo de entrada
        
        Returns:
            Lista de empréstimos (dicionários)
        """
        self.logger.info(f"Importando empréstimos de {arquivo}")
        
        arquivo_path = Path(arquivo)
        if not arquivo_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {arquivo}")
        
        with open(arquivo_path, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        # Converte strings de data para objetos date
        for emp in dados:
            for key, value in emp.items():
                if key in ['data_emprestimo', 'data_prevista_devolucao', 'data_devolucao'] and value:
                    emp[key] = date.fromisoformat(value) if isinstance(value, str) else value
        
        self.logger.info(f"Importação concluída: {len(dados)} empréstimos")
        return dados
    
    def exportar_livros_csv(self, livros: List[Dict[str, Any]], arquivo: str) -> None:
        """
        Exporta livros para arquivo CSV
        
        Args:
            livros: Lista de livros (dicionários)
            arquivo: Caminho do arquivo de saída
        """
        self.logger.info(f"Exportando {len(livros)} livros para {arquivo}")
        
        if not livros:
            return
        
        arquivo_path = Path(arquivo)
        arquivo_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Obtém todas as chaves possíveis
        todas_chaves = set()
        for livro in livros:
            todas_chaves.update(livro.keys())
        
        with open(arquivo_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=sorted(todas_chaves))
            writer.writeheader()
            
            for livro in livros:
                livro_copy = {}
                for key, value in livro.items():
                    if isinstance(value, (date, datetime)):
                        livro_copy[key] = value.isoformat()
                    else:
                        livro_copy[key] = value
                writer.writerow(livro_copy)
        
        self.logger.info(f"Exportação CSV concluída: {arquivo}")
    
    def ler_configuracao(self, arquivo: str) -> Dict[str, Any]:
        """
        Lê arquivo de configuração JSON
        
        Args:
            arquivo: Caminho do arquivo de configuração
        
        Returns:
            Dicionário com configurações
        """
        arquivo_path = Path(arquivo)
        if not arquivo_path.exists():
            raise FileNotFoundError(f"Arquivo de configuração não encontrado: {arquivo}")
        
        with open(arquivo_path, 'r', encoding='utf-8') as f:
            return json.load(f)


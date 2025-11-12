"""
Testes unitários para FileHandler
"""
import pytest
import json
import csv
import tempfile
import os
from pathlib import Path
from datetime import date, datetime

from src.utils.file_handler import FileHandler


class TestFileHandler:
    """Testes para FileHandler"""
    
    def test_exportar_emprestimos_json(self):
        """Testa exportação de empréstimos para JSON"""
        handler = FileHandler()
        emprestimos = [
            {
                "id": 1,
                "livro_id": 1,
                "usuario_id": 1,
                "data_emprestimo": date(2024, 1, 1),
                "data_prevista_devolucao": date(2024, 1, 15),
                "devolvido": False
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            arquivo = f.name
        
        try:
            handler.exportar_emprestimos_json(emprestimos, arquivo)
            
            assert os.path.exists(arquivo)
            with open(arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                assert len(dados) == 1
                assert dados[0]['id'] == 1
        finally:
            if os.path.exists(arquivo):
                os.remove(arquivo)
    
    def test_importar_emprestimos_json(self):
        """Testa importação de empréstimos de JSON"""
        handler = FileHandler()
        emprestimos = [
            {
                "id": 1,
                "livro_id": 1,
                "usuario_id": 1,
                "data_emprestimo": "2024-01-01",
                "data_prevista_devolucao": "2024-01-15",
                "devolvido": False
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(emprestimos, f, indent=2)
            arquivo = f.name
        
        try:
            resultado = handler.importar_emprestimos_json(arquivo)
            assert len(resultado) == 1
            assert resultado[0]['id'] == 1
        finally:
            if os.path.exists(arquivo):
                os.remove(arquivo)
    
    def test_exportar_livros_csv(self):
        """Testa exportação de livros para CSV"""
        handler = FileHandler()
        livros = [
            {
                "id": 1,
                "titulo": "Livro Teste",
                "ano_publicacao": 2020
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            arquivo = f.name
        
        try:
            handler.exportar_livros_csv(livros, arquivo)
            
            assert os.path.exists(arquivo)
            with open(arquivo, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                linhas = list(reader)
                assert len(linhas) == 1
        finally:
            if os.path.exists(arquivo):
                os.remove(arquivo)
    
    def test_ler_configuracao(self):
        """Testa leitura de configuração"""
        handler = FileHandler()
        config = {"teste": "valor"}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            arquivo = f.name
        
        try:
            resultado = handler.ler_configuracao(arquivo)
            assert resultado['teste'] == 'valor'
        finally:
            if os.path.exists(arquivo):
                os.remove(arquivo)
    
    def test_importar_emprestimos_json_arquivo_nao_existe(self):
        """Testa importação de JSON quando arquivo não existe"""
        handler = FileHandler()
        with pytest.raises(FileNotFoundError):
            handler.importar_emprestimos_json("arquivo_inexistente.json")
    
    def test_ler_configuracao_arquivo_nao_existe(self):
        """Testa leitura de configuração quando arquivo não existe"""
        handler = FileHandler()
        with pytest.raises(FileNotFoundError):
            handler.ler_configuracao("config_inexistente.json")
    


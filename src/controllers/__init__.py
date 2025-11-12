"""
Controllers - Lógica de negócio
Nota: A lógica de negócio principal está em services/.
Este diretório foi criado para seguir a estrutura esperada.
"""

# Importa os serviços para manter compatibilidade
from src.services.livro_service import LivroService
from src.services.usuario_service import UsuarioService
from src.services.emprestimo_service import EmprestimoService
from src.services.autor_service import AutorService
from src.services.categoria_service import CategoriaService

__all__ = [
    'LivroService',
    'UsuarioService',
    'EmprestimoService',
    'AutorService',
    'CategoriaService'
]


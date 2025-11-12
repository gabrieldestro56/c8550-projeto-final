"""
Exceções personalizadas do sistema de biblioteca
"""


class BibliotecaException(Exception):
    """Exceção base para todas as exceções do sistema"""
    
    def __init__(self, message: str, code: str = "GENERIC_ERROR") -> None:
        """
        Inicializa a exceção
        
        Args:
            message: Mensagem de erro
            code: Código do erro
        """
        self.message = message
        self.code = code
        super().__init__(self.message)


class EntidadeNaoEncontradaException(BibliotecaException):
    """Exceção lançada quando uma entidade não é encontrada"""
    
    def __init__(self, entidade: str, identificador: str) -> None:
        """
        Inicializa a exceção
        
        Args:
            entidade: Nome da entidade
            identificador: Identificador usado na busca
        """
        message = f"{entidade} com identificador '{identificador}' não encontrado(a)"
        super().__init__(message, "ENTIDADE_NAO_ENCONTRADA")
        self.entidade = entidade
        self.identificador = identificador


class ValidacaoException(BibliotecaException):
    """Exceção lançada quando uma validação falha"""
    
    def __init__(self, message: str, campo: str = None) -> None:
        """
        Inicializa a exceção
        
        Args:
            message: Mensagem de erro
            campo: Nome do campo que falhou na validação
        """
        super().__init__(message, "VALIDACAO_FALHOU")
        self.campo = campo


class RegraNegocioException(BibliotecaException):
    """Exceção lançada quando uma regra de negócio é violada"""
    
    def __init__(self, message: str) -> None:
        """
        Inicializa a exceção
        
        Args:
            message: Mensagem de erro
        """
        super().__init__(message, "REGRA_NEGOCIO_VIOLADA")


class LivroIndisponivelException(RegraNegocioException):
    """Exceção lançada quando um livro não está disponível para empréstimo"""
    
    def __init__(self, livro_id: int) -> None:
        """
        Inicializa a exceção
        
        Args:
            livro_id: ID do livro indisponível
        """
        message = f"Livro com ID {livro_id} não está disponível para empréstimo"
        super().__init__(message)
        self.livro_id = livro_id


class LimiteEmprestimosException(RegraNegocioException):
    """Exceção lançada quando o usuário excede o limite de empréstimos"""
    
    def __init__(self, usuario_id: int, limite: int) -> None:
        """
        Inicializa a exceção
        
        Args:
            usuario_id: ID do usuário
            limite: Limite de empréstimos permitidos
        """
        message = f"Usuário {usuario_id} excedeu o limite de {limite} empréstimos ativos"
        super().__init__(message)
        self.usuario_id = usuario_id
        self.limite = limite


class IdadeMinimaException(RegraNegocioException):
    """Exceção lançada quando o usuário não atende à idade mínima"""
    
    def __init__(self, idade: int, idade_minima: int) -> None:
        """
        Inicializa a exceção
        
        Args:
            idade: Idade do usuário
            idade_minima: Idade mínima requerida
        """
        message = f"Usuário com {idade} anos não atende à idade mínima de {idade_minima} anos"
        super().__init__(message)
        self.idade = idade
        self.idade_minima = idade_minima


class EmprestimoNaoEncontradoException(EntidadeNaoEncontradaException):
    """Exceção lançada quando um empréstimo não é encontrado"""
    
    def __init__(self, emprestimo_id: int) -> None:
        """
        Inicializa a exceção
        
        Args:
            emprestimo_id: ID do empréstimo
        """
        super().__init__("Emprestimo", str(emprestimo_id))
        self.emprestimo_id = emprestimo_id


class EmprestimoJaDevolvidoException(RegraNegocioException):
    """Exceção lançada quando tenta devolver um empréstimo já devolvido"""
    
    def __init__(self, emprestimo_id: int) -> None:
        """
        Inicializa a exceção
        
        Args:
            emprestimo_id: ID do empréstimo
        """
        message = f"Empréstimo {emprestimo_id} já foi devolvido"
        super().__init__(message)
        self.emprestimo_id = emprestimo_id


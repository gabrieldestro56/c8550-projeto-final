"""
Serviço de Emprestimo - Contém as regras de negócio complexas
"""
from typing import List, Optional
from datetime import date, timedelta
from sqlalchemy.orm import Session

from src.models.emprestimo import Emprestimo
from src.repositories.emprestimo_repository import EmprestimoRepository, IEmprestimoRepository
from src.repositories.livro_repository import LivroRepository
from src.repositories.usuario_repository import UsuarioRepository
from src.exceptions.biblioteca_exceptions import (
    EntidadeNaoEncontradaException,
    LivroIndisponivelException,
    LimiteEmprestimosException,
    IdadeMinimaException,
    EmprestimoNaoEncontradoException,
    EmprestimoJaDevolvidoException
)
from src.utils.logger import get_logger


class EmprestimoService:
    """Serviço para gerenciar empréstimos com regras de negócio complexas"""
    
    def __init__(
        self,
        session: Session,
        emprestimo_repo: Optional[IEmprestimoRepository] = None,
        livro_repo: Optional[LivroRepository] = None,
        usuario_repo: Optional[UsuarioRepository] = None,
        max_emprestimos: int = 5,
        dias_emprestimo: int = 14,
        multa_diaria: float = 2.50,
        idade_minima: int = 12
    ) -> None:
        """
        Inicializa o serviço com injeção de dependências
        
        Args:
            session: Sessão do banco de dados
            emprestimo_repo: Repositório de empréstimos (opcional)
            livro_repo: Repositório de livros (opcional)
            usuario_repo: Repositório de usuários (opcional)
            max_emprestimos: Número máximo de empréstimos por usuário
            dias_emprestimo: Número de dias para empréstimo
            multa_diaria: Valor da multa por dia de atraso
            idade_minima: Idade mínima para empréstimo
        """
        self.session = session
        self.emprestimo_repo = emprestimo_repo or EmprestimoRepository(session)
        self.livro_repo = livro_repo or LivroRepository(session)
        self.usuario_repo = usuario_repo or UsuarioRepository(session)
        self.max_emprestimos = max_emprestimos
        self.dias_emprestimo = dias_emprestimo
        self.multa_diaria = multa_diaria
        self.idade_minima = idade_minima
        self.logger = get_logger("EmprestimoService")
    
    def criar_emprestimo(self, livro_id: int, usuario_id: int) -> Emprestimo:
        """
        REGRA DE NEGÓCIO COMPLEXA 1: Validação completa de empréstimo
        
        Valida múltiplas condições:
        - Livro existe e está disponível
        - Usuário existe e está ativo
        - Usuário não excedeu limite de empréstimos
        - Usuário atende idade mínima
        - Cálculo de data de devolução
        
        Args:
            livro_id: ID do livro
            usuario_id: ID do usuário
        
        Returns:
            Empréstimo criado
        
        Raises:
            EntidadeNaoEncontradaException: Se livro ou usuário não existirem
            LivroIndisponivelException: Se livro não estiver disponível
            LimiteEmprestimosException: Se usuário exceder limite
            IdadeMinimaException: Se usuário não atender idade mínima
        """
        self.logger.info(f"Criando empréstimo: livro_id={livro_id}, usuario_id={usuario_id}")
        
        # Valida livro
        livro = self.livro_repo.buscar_por_id(livro_id)
        if not livro:
            raise EntidadeNaoEncontradaException("Livro", str(livro_id))
        
        # Valida usuário
        usuario = self.usuario_repo.buscar_por_id(usuario_id)
        if not usuario:
            raise EntidadeNaoEncontradaException("Usuario", str(usuario_id))
        
        # REGRA 1: Verifica se livro está disponível
        if not livro.esta_disponivel():
            self.logger.warning(f"Livro {livro_id} não está disponível")
            raise LivroIndisponivelException(livro_id)
        
        # REGRA 2: Verifica limite de empréstimos do usuário
        emprestimos_ativos = self.emprestimo_repo.buscar_por_usuario_ativos(usuario_id)
        if len(emprestimos_ativos) >= self.max_emprestimos:
            self.logger.warning(f"Usuário {usuario_id} excedeu limite de empréstimos")
            raise LimiteEmprestimosException(usuario_id, self.max_emprestimos)
        
        # REGRA 3: Verifica idade mínima do usuário
        idade_usuario = usuario.idade()
        if idade_usuario < self.idade_minima:
            self.logger.warning(f"Usuário {usuario_id} não atende idade mínima: {idade_usuario} < {self.idade_minima}")
            raise IdadeMinimaException(idade_usuario, self.idade_minima)
        
        # Verifica se usuário está ativo
        if not usuario.ativo:
            raise EntidadeNaoEncontradaException("Usuario", f"{usuario_id} (inativo)")
        
        # Cria empréstimo
        hoje = date.today()
        data_prevista = hoje + timedelta(days=self.dias_emprestimo)
        
        emprestimo = Emprestimo(
            livro_id=livro_id,
            usuario_id=usuario_id,
            data_emprestimo=hoje,
            data_prevista_devolucao=data_prevista,
            devolvido=False,
            multa=0.0
        )
        
        # Empresta o livro (atualiza quantidade disponível)
        livro.emprestar()
        self.livro_repo.atualizar(livro)
        
        emprestimo = self.emprestimo_repo.criar(emprestimo)
        self.logger.info(f"Empréstimo criado com sucesso: ID {emprestimo.id}")
        return emprestimo
    
    def devolver_emprestimo(self, emprestimo_id: int) -> Emprestimo:
        """
        REGRA DE NEGÓCIO COMPLEXA 2: Cálculo de multa por atraso
        
        Calcula multa baseada em:
        - Data prevista de devolução
        - Data atual
        - Valor da multa diária
        - Atualização de disponibilidade do livro
        
        Args:
            emprestimo_id: ID do empréstimo
        
        Returns:
            Empréstimo devolvido
        
        Raises:
            EmprestimoNaoEncontradoException: Se empréstimo não for encontrado
            EmprestimoJaDevolvidoException: Se empréstimo já foi devolvido
        """
        self.logger.info(f"Devolvendo empréstimo ID {emprestimo_id}")
        
        emprestimo = self.emprestimo_repo.buscar_por_id(emprestimo_id)
        if not emprestimo:
            raise EmprestimoNaoEncontradoException(emprestimo_id)
        
        if emprestimo.devolvido:
            raise EmprestimoJaDevolvidoException(emprestimo_id)
        
        # Calcula multa se houver atraso
        if emprestimo.esta_atrasado():
            dias_atraso = emprestimo.dias_atraso()
            multa = emprestimo.calcular_multa(self.multa_diaria)
            self.logger.warning(
                f"Empréstimo {emprestimo_id} atrasado por {dias_atraso} dias. "
                f"Multa calculada: R$ {multa:.2f}"
            )
        
        # Devolve o empréstimo (marca como devolvido e calcula multa)
        emprestimo.devolver_emprestimo(self.multa_diaria)
        
        # Atualiza livro
        if emprestimo.livro:
            self.livro_repo.atualizar(emprestimo.livro)
        
        emprestimo = self.emprestimo_repo.atualizar(emprestimo)
        self.logger.info(f"Empréstimo {emprestimo_id} devolvido com sucesso. Multa: R$ {emprestimo.multa:.2f}")
        return emprestimo
    
    def calcular_multa_emprestimo(self, emprestimo_id: int) -> float:
        """
        REGRA DE NEGÓCIO COMPLEXA 3: Processamento de multa
        
        Processa cálculo de multa considerando:
        - Dias de atraso
        - Valor da multa diária
        - Status do empréstimo
        - Interação entre empréstimo e livro
        
        Args:
            emprestimo_id: ID do empréstimo
        
        Returns:
            Valor da multa calculada
        
        Raises:
            EmprestimoNaoEncontradoException: Se empréstimo não for encontrado
        """
        emprestimo = self.emprestimo_repo.buscar_por_id(emprestimo_id)
        if not emprestimo:
            raise EmprestimoNaoEncontradoException(emprestimo_id)
        
        if emprestimo.devolvido:
            # Se já foi devolvido, retorna a multa já calculada
            return float(emprestimo.multa)
        
        # Calcula multa atual
        return emprestimo.calcular_multa(self.multa_diaria)
    
    def buscar_por_id(self, emprestimo_id: int) -> Emprestimo:
        """
        Busca empréstimo por ID
        
        Args:
            emprestimo_id: ID do empréstimo
        
        Returns:
            Empréstimo encontrado
        
        Raises:
            EmprestimoNaoEncontradoException: Se empréstimo não for encontrado
        """
        emprestimo = self.emprestimo_repo.buscar_por_id(emprestimo_id)
        if not emprestimo:
            raise EmprestimoNaoEncontradoException(emprestimo_id)
        return emprestimo
    
    def listar_todos(self, skip: int = 0, limit: int = 100) -> List[Emprestimo]:
        """
        Lista todos os empréstimos
        
        Args:
            skip: Número de registros a pular
            limit: Número máximo de registros
        
        Returns:
            Lista de empréstimos
        """
        return self.emprestimo_repo.listar_todos(skip, limit)
    
    def buscar_por_usuario(self, usuario_id: int) -> List[Emprestimo]:
        """
        Busca empréstimos de um usuário
        
        Args:
            usuario_id: ID do usuário
        
        Returns:
            Lista de empréstimos
        """
        return self.emprestimo_repo.buscar_por_usuario(usuario_id)
    
    def buscar_atrasados(self) -> List[Emprestimo]:
        """
        Busca empréstimos atrasados
        
        Returns:
            Lista de empréstimos atrasados
        """
        return self.emprestimo_repo.buscar_atrasados()
    
    def buscar_ativos(self) -> List[Emprestimo]:
        """
        Busca empréstimos ativos
        
        Returns:
            Lista de empréstimos ativos
        """
        return self.emprestimo_repo.buscar_ativos()


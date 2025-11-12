"""
Validadores para dados de entrada
"""
import re
from typing import Optional
from datetime import date, datetime
from src.exceptions.biblioteca_exceptions import ValidacaoException


class CPFValidator:
    """Validador de CPF"""
    
    @staticmethod
    def validar(cpf: str) -> bool:
        """
        Valida um CPF
        
        Args:
            cpf: CPF a ser validado
        
        Returns:
            True se válido, False caso contrário
        """
        # Remove caracteres não numéricos
        cpf = re.sub(r'\D', '', cpf)
        
        # Verifica se tem 11 dígitos
        if len(cpf) != 11:
            return False
        
        # Verifica se todos os dígitos são iguais
        if cpf == cpf[0] * 11:
            return False
        
        # Validação dos dígitos verificadores
        def calcular_digito(cpf_parcial: str, peso_inicial: int) -> int:
            soma = sum(int(cpf_parcial[i]) * (peso_inicial - i) for i in range(len(cpf_parcial)))
            resto = soma % 11
            return 0 if resto < 2 else 11 - resto
        
        digito1 = calcular_digito(cpf[:9], 10)
        digito2 = calcular_digito(cpf[:10], 11)
        
        return cpf[-2:] == f"{digito1}{digito2}"
    
    @staticmethod
    def formatar(cpf: str) -> str:
        """
        Formata um CPF removendo caracteres não numéricos
        
        Args:
            cpf: CPF a ser formatado
        
        Returns:
            CPF apenas com números
        """
        return re.sub(r'\D', '', cpf)


class EmailValidator:
    """Validador de email"""
    
    @staticmethod
    def validar(email: str) -> bool:
        """
        Valida um email
        
        Args:
            email: Email a ser validado
        
        Returns:
            True se válido, False caso contrário
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))


class DataValidator:
    """Validador de datas"""
    
    @staticmethod
    def validar_data_nascimento(data: date, idade_minima: int = 12) -> bool:
        """
        Valida uma data de nascimento
        
        Args:
            data: Data de nascimento
            idade_minima: Idade mínima permitida
        
        Returns:
            True se válida, False caso contrário
        """
        hoje = date.today()
        
        # Data não pode ser no futuro
        if data > hoje:
            return False
        
        # Calcula idade
        idade = hoje.year - data.year
        if (hoje.month, hoje.day) < (data.month, data.day):
            idade -= 1
        
        # Verifica idade mínima
        return idade >= idade_minima


class Validator:
    """Classe principal de validação"""
    
    @staticmethod
    def validar_cpf(cpf: str) -> None:
        """
        Valida CPF e lança exceção se inválido
        
        Args:
            cpf: CPF a ser validado
        
        Raises:
            ValidacaoException: Se o CPF for inválido
        """
        if not CPFValidator.validar(cpf):
            raise ValidacaoException("CPF inválido", "cpf")
    
    @staticmethod
    def validar_email(email: str) -> None:
        """
        Valida email e lança exceção se inválido
        
        Args:
            email: Email a ser validado
        
        Raises:
            ValidacaoException: Se o email for inválido
        """
        if not EmailValidator.validar(email):
            raise ValidacaoException("Email inválido", "email")
    
    @staticmethod
    def validar_data_nascimento(data: date, idade_minima: int = 12) -> None:
        """
        Valida data de nascimento e lança exceção se inválida
        
        Args:
            data: Data de nascimento
            idade_minima: Idade mínima permitida
        
        Raises:
            ValidacaoException: Se a data for inválida
        """
        if not DataValidator.validar_data_nascimento(data, idade_minima):
            raise ValidacaoException(
                f"Data de nascimento inválida ou idade menor que {idade_minima} anos",
                "data_nascimento"
            )


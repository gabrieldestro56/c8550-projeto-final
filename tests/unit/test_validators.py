"""
Testes unitários para validadores
"""
import pytest
from datetime import date

from src.validators.validators import (
    CPFValidator, EmailValidator,
    DataValidator, Validator
)
from src.exceptions.biblioteca_exceptions import ValidacaoException


class TestCPFValidator:
    """Testes para CPFValidator"""
    
    def test_validar_cpf_valido(self):
        """Testa validação de CPF válido"""
        cpf = "12345678909"
        assert CPFValidator.validar(cpf) is True
    
    def test_validar_cpf_invalido(self):
        """Testa validação de CPF inválido"""
        cpf = "12345678900"
        assert CPFValidator.validar(cpf) is False
    
    def test_validar_cpf_todos_iguais(self):
        """Testa CPF com todos os dígitos iguais"""
        cpf = "11111111111"
        assert CPFValidator.validar(cpf) is False
    
    def test_validar_cpf_tamanho_incorreto(self):
        """Testa CPF com tamanho incorreto"""
        cpf = "123456789"
        assert CPFValidator.validar(cpf) is False
    
    def test_formatar_cpf(self):
        """Testa formatação de CPF"""
        cpf = "123.456.789-09"
        cpf_formatado = CPFValidator.formatar(cpf)
        assert cpf_formatado == "12345678909"
    
    def test_validar_cpf_com_formatacao(self):
        """Testa validação de CPF com formatação"""
        cpf = "123.456.789-09"
        cpf_formatado = CPFValidator.formatar(cpf)
        assert CPFValidator.validar(cpf_formatado) is True


class TestEmailValidator:
    """Testes para EmailValidator"""
    
    def test_validar_email_valido(self):
        """Testa validação de email válido"""
        email = "teste@example.com"
        assert EmailValidator.validar(email) is True
    
    def test_validar_email_invalido_sem_arroba(self):
        """Testa email sem @"""
        email = "testeexample.com"
        assert EmailValidator.validar(email) is False
    
    def test_validar_email_invalido_sem_dominio(self):
        """Testa email sem domínio"""
        email = "teste@"
        assert EmailValidator.validar(email) is False
    
    def test_validar_email_invalido_sem_extensao(self):
        """Testa email sem extensão"""
        email = "teste@example"
        assert EmailValidator.validar(email) is False


class TestDataValidator:
    """Testes para DataValidator"""
    
    def test_validar_data_nascimento_valida(self):
        """Testa validação de data de nascimento válida"""
        data = date(1990, 1, 1)
        assert DataValidator.validar_data_nascimento(data, idade_minima=12) is True
    
    def test_validar_data_nascimento_idade_insuficiente(self):
        """Testa data de nascimento com idade insuficiente"""
        data = date(2020, 1, 1)  # Menos de 12 anos
        assert DataValidator.validar_data_nascimento(data, idade_minima=12) is False
    
    def test_validar_data_nascimento_futura(self):
        """Testa data de nascimento no futuro"""
        data = date(2030, 1, 1)
        assert DataValidator.validar_data_nascimento(data, idade_minima=12) is False


class TestValidator:
    """Testes para Validator"""
    
    def test_validar_cpf_levanta_excecao(self):
        """Testa que Validator.validar_cpf levanta exceção para CPF inválido"""
        with pytest.raises(ValidacaoException):
            Validator.validar_cpf("12345678900")
    
    def test_validar_email_levanta_excecao(self):
        """Testa que Validator.validar_email levanta exceção para email inválido"""
        with pytest.raises(ValidacaoException):
            Validator.validar_email("email_invalido")
    
    def test_validar_data_nascimento_levanta_excecao(self):
        """Testa que Validator.validar_data_nascimento levanta exceção"""
        with pytest.raises(ValidacaoException):
            Validator.validar_data_nascimento(date(2020, 1, 1), idade_minima=12)


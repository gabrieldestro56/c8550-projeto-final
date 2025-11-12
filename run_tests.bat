@echo off
REM Script para executar todos os testes no Windows

echo Executando testes unitarios...
pytest tests/unit/ -v

echo Executando testes de integracao...
pytest tests/integration/ -v

echo Executando testes funcionais...
pytest tests/functional/ -v

echo Executando testes de API...
pytest tests/api/ -v

echo Executando todos os testes com cobertura...
pytest --cov=src --cov-report=html --cov-report=term-missing

echo Testes concluidos!


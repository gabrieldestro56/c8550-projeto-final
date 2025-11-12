#!/bin/bash
# Script para executar todos os testes

echo "Executando testes unitários..."
pytest tests/unit/ -v

echo "Executando testes de integração..."
pytest tests/integration/ -v

echo "Executando testes funcionais..."
pytest tests/functional/ -v

echo "Executando testes de API..."
pytest tests/api/ -v

echo "Executando todos os testes com cobertura..."
pytest --cov=src --cov-report=html --cov-report=term-missing

echo "Testes concluídos!"


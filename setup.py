"""
Script de setup do projeto
"""
from setuptools import setup, find_packages

setup(
    name="sistema-biblioteca",
    version="1.0.0",
    description="Sistema de Gerenciamento de Biblioteca - CC8550",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "sqlalchemy>=2.0.23",
        "pydantic>=2.5.0",
        "python-dotenv>=1.0.0",
        "pytest>=7.4.3",
        "pytest-cov>=4.1.0",
        "pytest-mock>=3.12.0",
        "pytest-benchmark>=4.0.0",
        "httpx>=0.25.2",
        "mutmut>=2.4.0",
        "coverage>=7.3.2",
    ],
    python_requires=">=3.8",
)


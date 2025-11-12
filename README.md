# Sistema de Gerenciamento de Biblioteca

Projeto desenvolvido para a disciplina **CC8550 - Simulação e Teste de Software**.

## 📋 Descrição

Sistema completo de gerenciamento de biblioteca com operações CRUD, regras de negócio complexas e interface CLI interativa.

## 🚀 Instalação

1. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

2. **Inicialize o banco de dados:**

```bash
python -m src.database.init_db
```

## 💻 Execução

### Interface CLI (Terminal Interativo)

Execute o sistema pela interface CLI:

```bash
python run_cli.py
```

Ou:

```bash
python -m src.cli.main
```

A interface CLI oferece um menu interativo para gerenciar:

- 📖 Livros
- 👥 Usuários
- 📋 Empréstimos
- ✍️ Autores
- 📂 Categorias

## 🧪 Testes

### Executar todos os testes:

```bash
pytest
```

### Testes com cobertura:

```bash
pytest --cov=src --cov-report=html
```

O relatório de cobertura estará em `htmlcov/index.html`

### Testes específicos:

```bash
# Testes unitários
pytest tests/unit/

# Testes de integração
pytest tests/integration/

# Testes funcionais
pytest tests/functional/
```

### Testes de mutação:

```bash
mutmut run
mutmut html
```

## 📁 Estrutura do Projeto

```
.
├── src/
│   ├── models/          # Modelos de dados
│   ├── repositories/    # Camada de acesso a dados
│   ├── services/        # Lógica de negócio
│   ├── cli/             # Interface CLI interativa
│   ├── database/        # Configuração do banco
│   ├── exceptions/      # Exceções personalizadas
│   ├── validators/      # Validadores
│   └── utils/           # Utilitários
├── tests/               # Testes
│   ├── unit/            # Testes unitários
│   ├── integration/     # Testes de integração
│   └── functional/      # Testes funcionais
├── config.json          # Configurações
└── requirements.txt     # Dependências
```

## ✨ Funcionalidades

- ✅ 5 operações CRUD completas
- ✅ 3 regras de negócio complexas
- ✅ 2 funcionalidades de busca com filtros
- ✅ Tratamento de exceções personalizado
- ✅ Validação robusta de dados
- ✅ Interface CLI interativa
- ✅ Cobertura de testes >= 80%

## 📝 Requisitos

- Python 3.8+
- SQLite (incluído no Python)

## 👥 Integrantes

- **Gabriel Destro** - RA: 24.122.059-9
- **Nathan Dantas** - RA: 24.122.041-7

## 📚 Disciplina

CC8550 - Simulação e Teste de Software  
Centro Universitário FEI - 2º Semestre de 2025

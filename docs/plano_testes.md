# Plano de Testes

## Estratégia de Testes

### Testes Unitários (25%)
- Objetivo: Testar todas as funções e métodos isoladamente
- Ferramenta: pytest
- Quantidade mínima: 30 casos de teste
- Cobertura: Casos normais, extremos e de erro
- Técnicas: Fixtures e parametrização

### Testes de Integração (20%)
- Objetivo: Testar interações entre módulos
- Quantidade mínima: 10 testes
- Foco: Integração com banco de dados e fluxos completos

### Testes Funcionais - Caixa-Preta (15%)
- Objetivo: Testar funcionalidades sem conhecer implementação
- Quantidade mínima: 8 cenários
- Foco: Entradas e saídas esperadas

### Testes Estruturais - Caixa-Branca (15%)
- Objetivo: Alcançar mínimo de 80% de cobertura
- Ferramenta: pytest-cov
- Foco: Todos os caminhos críticos e branches

### Testes de Mutação (10%)
- Ferramenta: mutmut
- Módulos: Pelo menos 3 módulos principais
- Análise: Taxa de mutantes mortos

### Testes Específicos por Tipo (15%)
- Testes de Exceções
- Testes com Mocks e Stubs
- Testes de Performance
- Testes de Orientação a Objetos

## Execução

```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=src --cov-report=html

# Testes de mutação
mutmut run
mutmut html
```


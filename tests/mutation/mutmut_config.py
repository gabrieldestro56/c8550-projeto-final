"""
Configuração do mutmut para testes de mutação
"""
# Módulos a serem testados
paths_to_mutate = [
    'src/services/',
    'src/repositories/',
    'src/validators/',
]

# Testes a executar
tests_dir = 'tests/'

# Comando para executar testes
test_command = 'pytest {paths_to_mutate}'


"""
Interface CLI interativa para o Sistema de Biblioteca
"""
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.database.config import db_config
from src.services.livro_service import LivroService
from src.services.usuario_service import UsuarioService
from src.services.emprestimo_service import EmprestimoService
from src.services.autor_service import AutorService
from src.services.categoria_service import CategoriaService
from src.models.livro import Livro
from src.models.usuario import Usuario
from src.models.emprestimo import Emprestimo
from src.models.autor import Autor
from src.models.categoria import Categoria
from datetime import date
from typing import Optional


class BibliotecaCLI:
    """Interface CLI interativa para o sistema de biblioteca"""
    
    def __init__(self):
        """Inicializa a CLI"""
        self.session = db_config.get_session()
        self.livro_service = LivroService(self.session)
        self.usuario_service = UsuarioService(self.session)
        self.emprestimo_service = EmprestimoService(self.session)
        self.autor_service = AutorService(self.session)
        self.categoria_service = CategoriaService(self.session)
    
    def exibir_menu_principal(self):
        """Exibe o menu principal"""
        print("\n" + "="*60)
        print("  SISTEMA DE GERENCIAMENTO DE BIBLIOTECA")
        print("="*60)
        print("\nMENU PRINCIPAL:")
        print("1. Gerenciar Livros")
        print("2. Gerenciar Usuários")
        print("3. Gerenciar Empréstimos")
        print("4. Gerenciar Autores")
        print("5. Gerenciar Categorias")
        print("0. Sair")
        print("="*60)
    
    def exibir_menu_livros(self):
        """Exibe menu de livros"""
        print("\n" + "="*60)
        print("  GERENCIAR LIVROS")
        print("="*60)
        print("1. Listar livros")
        print("2. Buscar livro por ID")
        print("3. Criar livro")
        print("4. Atualizar livro")
        print("5. Deletar livro")
        print("6. Buscar livros disponíveis")
        print("7. Buscar com filtros")
        print("0. Voltar")
        print("="*60)
    
    def exibir_menu_usuarios(self):
        """Exibe menu de usuários"""
        print("\n" + "="*60)
        print("  GERENCIAR USUÁRIOS")
        print("="*60)
        print("1. Listar usuários")
        print("2. Buscar usuário por ID")
        print("3. Criar usuário")
        print("4. Atualizar usuário")
        print("5. Deletar usuário")
        print("6. Buscar com filtros")
        print("0. Voltar")
        print("="*60)
    
    def exibir_menu_emprestimos(self):
        """Exibe menu de empréstimos"""
        print("\n" + "="*60)
        print("  GERENCIAR EMPRÉSTIMOS")
        print("="*60)
        print("1. Listar empréstimos")
        print("2. Buscar empréstimo por ID")
        print("3. Criar empréstimo")
        print("4. Devolver empréstimo")
        print("5. Buscar empréstimos de um usuário")
        print("6. Buscar empréstimos atrasados")
        print("7. Calcular multa de empréstimo")
        print("0. Voltar")
        print("="*60)
    
    def exibir_menu_autores(self):
        """Exibe menu de autores"""
        print("\n" + "="*60)
        print("  GERENCIAR AUTORES")
        print("="*60)
        print("1. Listar autores")
        print("2. Buscar autor por ID")
        print("3. Criar autor")
        print("4. Atualizar autor")
        print("5. Deletar autor")
        print("6. Buscar por nome")
        print("0. Voltar")
        print("="*60)
    
    def exibir_menu_categorias(self):
        """Exibe menu de categorias"""
        print("\n" + "="*60)
        print("  GERENCIAR CATEGORIAS")
        print("="*60)
        print("1. Listar categorias")
        print("2. Buscar categoria por ID")
        print("3. Criar categoria")
        print("4. Atualizar categoria")
        print("5. Deletar categoria")
        print("0. Voltar")
        print("="*60)
    
    def ler_opcao(self, mensagem: str = "Escolha uma opção: ") -> str:
        """Lê uma opção do usuário"""
        return input(mensagem).strip()
    
    def ler_inteiro(self, mensagem: str) -> int:
        """Lê um inteiro do usuário"""
        while True:
            try:
                return int(input(mensagem))
            except ValueError:
                print("❌ Por favor, digite um número válido.")
    
    def ler_data(self, mensagem: str) -> date:
        """Lê uma data do usuário"""
        while True:
            try:
                data_str = input(mensagem + " (YYYY-MM-DD): ")
                return date.fromisoformat(data_str)
            except ValueError:
                print("❌ Data inválida. Use o formato YYYY-MM-DD (ex: 1990-05-15)")
    
    def processar_menu_livros(self):
        """Processa o menu de livros"""
        while True:
            self.exibir_menu_livros()
            opcao = self.ler_opcao()
            
            if opcao == "0":
                break
            elif opcao == "1":
                self.listar_livros()
            elif opcao == "2":
                self.buscar_livro()
            elif opcao == "3":
                self.criar_livro()
            elif opcao == "4":
                self.atualizar_livro()
            elif opcao == "5":
                self.deletar_livro()
            elif opcao == "6":
                self.buscar_livros_disponiveis()
            elif opcao == "7":
                self.buscar_livros_filtros()
            else:
                print("❌ Opção inválida!")
    
    def processar_menu_usuarios(self):
        """Processa o menu de usuários"""
        while True:
            self.exibir_menu_usuarios()
            opcao = self.ler_opcao()
            
            if opcao == "0":
                break
            elif opcao == "1":
                self.listar_usuarios()
            elif opcao == "2":
                self.buscar_usuario()
            elif opcao == "3":
                self.criar_usuario()
            elif opcao == "4":
                self.atualizar_usuario()
            elif opcao == "5":
                self.deletar_usuario()
            elif opcao == "6":
                self.buscar_usuarios_filtros()
            else:
                print("❌ Opção inválida!")
    
    def processar_menu_emprestimos(self):
        """Processa o menu de empréstimos"""
        while True:
            self.exibir_menu_emprestimos()
            opcao = self.ler_opcao()
            
            if opcao == "0":
                break
            elif opcao == "1":
                self.listar_emprestimos()
            elif opcao == "2":
                self.buscar_emprestimo()
            elif opcao == "3":
                self.criar_emprestimo()
            elif opcao == "4":
                self.devolver_emprestimo()
            elif opcao == "5":
                self.buscar_emprestimos_usuario()
            elif opcao == "6":
                self.buscar_emprestimos_atrasados()
            elif opcao == "7":
                self.calcular_multa()
            else:
                print("❌ Opção inválida!")
    
    def processar_menu_autores(self):
        """Processa o menu de autores"""
        while True:
            self.exibir_menu_autores()
            opcao = self.ler_opcao()
            
            if opcao == "0":
                break
            elif opcao == "1":
                self.listar_autores()
            elif opcao == "2":
                self.buscar_autor()
            elif opcao == "3":
                self.criar_autor()
            elif opcao == "4":
                self.atualizar_autor()
            elif opcao == "5":
                self.deletar_autor()
            elif opcao == "6":
                self.buscar_autor_nome()
            else:
                print("❌ Opção inválida!")
    
    def processar_menu_categorias(self):
        """Processa o menu de categorias"""
        while True:
            self.exibir_menu_categorias()
            opcao = self.ler_opcao()
            
            if opcao == "0":
                break
            elif opcao == "1":
                self.listar_categorias()
            elif opcao == "2":
                self.buscar_categoria()
            elif opcao == "3":
                self.criar_categoria()
            elif opcao == "4":
                self.atualizar_categoria()
            elif opcao == "5":
                self.deletar_categoria()
            else:
                print("❌ Opção inválida!")
    
    # Métodos para Livros
    def listar_livros(self):
        """Lista todos os livros"""
        try:
            livros = self.livro_service.listar_todos()
            if not livros:
                print("\n📚 Nenhum livro cadastrado.")
            else:
                print(f"\n📚 Total de livros: {len(livros)}")
                for livro in livros:
                    print(f"  ID: {livro.id} | {livro.titulo} | Disponível: {'Sim' if livro.esta_disponivel() else 'Não'}")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione Enter para continuar...")
    
    def buscar_livro(self):
        """Busca livro por ID"""
        try:
            livro_id = self.ler_inteiro("Digite o ID do livro: ")
            livro = self.livro_service.buscar_por_id(livro_id)
            print(f"\n📖 Livro encontrado:")
            print(f"  ID: {livro.id}")
            print(f"  Título: {livro.titulo}")
            print(f"  Disponível: {'Sim' if livro.esta_disponivel() else 'Não'}")
            print(f"  Quantidade: {livro.quantidade_disponivel}/{livro.quantidade_total}")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione Enter para continuar...")
    
    def criar_livro(self):
        """Cria um novo livro"""
        try:
            print("\n📝 Criar novo livro:")
            titulo = input("Título: ")
            autor_id = self.ler_inteiro("ID do Autor: ")
            categoria_id_input = input("ID da Categoria (opcional): ").strip()
            categoria_id = int(categoria_id_input) if categoria_id_input else None
            quantidade = self.ler_inteiro("Quantidade total: ")
            
            livro = Livro(
                titulo=titulo,
                autor_id=autor_id,
                categoria_id=categoria_id,
                quantidade_total=quantidade,
                quantidade_disponivel=quantidade
            )
            
            livro = self.livro_service.criar_livro(livro)
            print(f"✅ Livro criado com sucesso! ID: {livro.id}")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione Enter para continuar...")
    
    def atualizar_livro(self):
        """Atualiza um livro"""
        try:
            livro_id = self.ler_inteiro("Digite o ID do livro: ")
            print("\nDeixe em branco para não alterar:")
            titulo = input("Novo título: ").strip() or None
            dados = {}
            if titulo:
                dados["titulo"] = titulo
            
            if dados:
                livro = self.livro_service.atualizar_livro(livro_id, dados)
                print(f"✅ Livro atualizado com sucesso!")
            else:
                print("ℹ️ Nenhuma alteração realizada.")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione Enter para continuar...")
    
    def deletar_livro(self):
        """Deleta um livro"""
        try:
            livro_id = self.ler_inteiro("Digite o ID do livro: ")
            confirmacao = input(f"Tem certeza que deseja deletar o livro {livro_id}? (s/N): ")
            if confirmacao.lower() == 's':
                self.livro_service.deletar_livro(livro_id)
                print("✅ Livro deletado com sucesso!")
            else:
                print("ℹ️ Operação cancelada.")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione Enter para continuar...")
    
    def buscar_livros_disponiveis(self):
        """Busca livros disponíveis"""
        try:
            livros = self.livro_service.buscar_disponiveis()
            if not livros:
                print("\n📚 Nenhum livro disponível no momento.")
            else:
                print(f"\n📚 Livros disponíveis ({len(livros)}):")
                for livro in livros:
                    print(f"  ID: {livro.id} | {livro.titulo}")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione Enter para continuar...")
    
    def buscar_livros_filtros(self):
        """Busca livros com filtros"""
        try:
            print("\nFiltros (deixe em branco para ignorar):")
            titulo = input("Título (busca parcial): ").strip()
            disponivel_input = input("Disponível? (s/n): ").strip().lower()
            disponivel = None if not disponivel_input else (disponivel_input == 's')
            
            filtros = {}
            if titulo:
                filtros["titulo"] = {"like": f"%{titulo}%"}
            if disponivel is not None:
                filtros["disponivel"] = disponivel
            
            livros = self.livro_service.buscar_com_filtros(filtros)
            print(f"\n📚 Resultados encontrados: {len(livros)}")
            for livro in livros:
                print(f"  ID: {livro.id} | {livro.titulo} | Disponível: {'Sim' if livro.esta_disponivel() else 'Não'}")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione Enter para continuar...")
    
    # Métodos para Usuários
    def listar_usuarios(self):
        """Lista todos os usuários"""
        try:
            usuarios = self.usuario_service.listar_todos()
            if not usuarios:
                print("\n👥 Nenhum usuário cadastrado.")
            else:
                print(f"\n👥 Total de usuários: {len(usuarios)}")
                for usuario in usuarios:
                    status = "Ativo" if usuario.ativo else "Inativo"
                    print(f"  ID: {usuario.id} | {usuario.nome} | {usuario.email} | {status}")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione Enter para continuar...")
    
    def buscar_usuario(self):
        """Busca usuário por ID"""
        try:
            usuario_id = self.ler_inteiro("Digite o ID do usuário: ")
            usuario = self.usuario_service.buscar_por_id(usuario_id)
            print(f"\n👤 Usuário encontrado:")
            print(f"  ID: {usuario.id}")
            print(f"  Nome: {usuario.nome}")
            print(f"  Email: {usuario.email}")
            print(f"  Status: {'Ativo' if usuario.ativo else 'Inativo'}")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione Enter para continuar...")
    
    def criar_usuario(self):
        """Cria um novo usuário"""
        try:
            print("\n📝 Criar novo usuário:")
            nome = input("Nome: ")
            email = input("Email: ")
            data_nasc = self.ler_data("Data de nascimento")
            
            usuario = Usuario(
                nome=nome,
                email=email,
                data_nascimento=data_nasc
            )
            
            usuario = self.usuario_service.criar_usuario(usuario)
            print(f"✅ Usuário criado com sucesso! ID: {usuario.id}")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione Enter para continuar...")
    
    def atualizar_usuario(self):
        """Atualiza um usuário"""
        try:
            usuario_id = self.ler_inteiro("Digite o ID do usuário: ")
            print("\nDeixe em branco para não alterar:")
            nome = input("Novo nome: ").strip() or None
            dados = {}
            if nome:
                dados["nome"] = nome
            
            if dados:
                usuario = self.usuario_service.atualizar_usuario(usuario_id, dados)
                print(f"✅ Usuário atualizado com sucesso!")
            else:
                print("ℹ️ Nenhuma alteração realizada.")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione Enter para continuar...")
    
    def deletar_usuario(self):
        """Deleta um usuário"""
        try:
            usuario_id = self.ler_inteiro("Digite o ID do usuário: ")
            confirmacao = input(f"Tem certeza que deseja deletar o usuário {usuario_id}? (s/N): ")
            if confirmacao.lower() == 's':
                self.usuario_service.deletar_usuario(usuario_id)
                print("✅ Usuário deletado com sucesso!")
            else:
                print("ℹ️ Operação cancelada.")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione Enter para continuar...")
    
    def buscar_usuarios_filtros(self):
        """Busca usuários com filtros"""
        try:
            print("\nFiltros (deixe em branco para ignorar):")
            nome = input("Nome (busca parcial): ").strip()
            ativo_input = input("Ativo? (s/n): ").strip().lower()
            ativo = None if not ativo_input else (ativo_input == 's')
            
            filtros = {}
            if nome:
                filtros["nome"] = {"like": f"%{nome}%"}
            if ativo is not None:
                filtros["ativo"] = ativo
            
            usuarios = self.usuario_service.buscar_com_filtros(filtros)
            print(f"\n👥 Resultados encontrados: {len(usuarios)}")
            for usuario in usuarios:
                status = "Ativo" if usuario.ativo else "Inativo"
                print(f"  ID: {usuario.id} | {usuario.nome} | {usuario.email} | {status}")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione Enter para continuar...")
    
    # Métodos para Empréstimos
    def listar_emprestimos(self):
        """Lista todos os empréstimos"""
        try:
            emprestimos = self.emprestimo_service.listar_todos()
            if not emprestimos:
                print("\n📋 Nenhum empréstimo cadastrado.")
            else:
                print(f"\n📋 Total de empréstimos: {len(emprestimos)}")
                for emp in emprestimos:
                    status = "Devolvido" if emp.devolvido else "Ativo"
                    print(f"  ID: {emp.id} | Livro: {emp.livro_id} | Usuário: {emp.usuario_id} | {status}")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione Enter para continuar...")
    
    def buscar_emprestimo(self):
        """Busca empréstimo por ID"""
        try:
            emprestimo_id = self.ler_inteiro("Digite o ID do empréstimo: ")
            emprestimo = self.emprestimo_service.buscar_por_id(emprestimo_id)
            print(f"\n📋 Empréstimo encontrado:")
            print(f"  ID: {emprestimo.id}")
            print(f"  Livro ID: {emprestimo.livro_id}")
            print(f"  Usuário ID: {emprestimo.usuario_id}")
            print(f"  Status: {'Devolvido' if emprestimo.devolvido else 'Ativo'}")
            print(f"  Multa: R$ {emprestimo.multa:.2f}")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione Enter para continuar...")
    
    def criar_emprestimo(self):
        """Cria um novo empréstimo"""
        try:
            print("\n📝 Criar novo empréstimo:")
            livro_id = self.ler_inteiro("ID do Livro: ")
            usuario_id = self.ler_inteiro("ID do Usuário: ")
            
            emprestimo = self.emprestimo_service.criar_emprestimo(livro_id, usuario_id)
            print(f"✅ Empréstimo criado com sucesso! ID: {emprestimo.id}")
            print(f"  Data de devolução prevista: {emprestimo.data_prevista_devolucao}")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione Enter para continuar...")
    
    def devolver_emprestimo(self):
        """Devolve um empréstimo"""
        try:
            emprestimo_id = self.ler_inteiro("Digite o ID do empréstimo: ")
            emprestimo = self.emprestimo_service.devolver_emprestimo(emprestimo_id)
            print(f"✅ Empréstimo devolvido com sucesso!")
            if emprestimo.multa > 0:
                print(f"  Multa aplicada: R$ {emprestimo.multa:.2f}")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione Enter para continuar...")
    
    def buscar_emprestimos_usuario(self):
        """Busca empréstimos de um usuário"""
        try:
            usuario_id = self.ler_inteiro("Digite o ID do usuário: ")
            emprestimos = self.emprestimo_service.buscar_por_usuario(usuario_id)
            print(f"\n📋 Empréstimos do usuário {usuario_id}: {len(emprestimos)}")
            for emp in emprestimos:
                status = "Devolvido" if emp.devolvido else "Ativo"
                print(f"  ID: {emp.id} | Livro: {emp.livro_id} | {status}")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione Enter para continuar...")
    
    def buscar_emprestimos_atrasados(self):
        """Busca empréstimos atrasados"""
        try:
            emprestimos = self.emprestimo_service.buscar_atrasados()
            if not emprestimos:
                print("\n📋 Nenhum empréstimo atrasado.")
            else:
                print(f"\n📋 Empréstimos atrasados: {len(emprestimos)}")
                for emp in emprestimos:
                    dias = emp.dias_atraso()
                    print(f"  ID: {emp.id} | Livro: {emp.livro_id} | Usuário: {emp.usuario_id} | {dias} dias de atraso")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione Enter para continuar...")
    
    def calcular_multa(self):
        """Calcula multa de um empréstimo"""
        try:
            emprestimo_id = self.ler_inteiro("Digite o ID do empréstimo: ")
            multa = self.emprestimo_service.calcular_multa_emprestimo(emprestimo_id)
            print(f"\n💰 Multa calculada: R$ {multa:.2f}")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione Enter para continuar...")
    
    # Métodos para Autores
    def listar_autores(self):
        """Lista todos os autores"""
        try:
            autores = self.autor_service.listar_todos()
            if not autores:
                print("\n✍️ Nenhum autor cadastrado.")
            else:
                print(f"\n✍️ Total de autores: {len(autores)}")
                for autor in autores:
                    print(f"  ID: {autor.id} | {autor.nome}")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione Enter para continuar...")
    
    def buscar_autor(self):
        """Busca autor por ID"""
        try:
            autor_id = self.ler_inteiro("Digite o ID do autor: ")
            autor = self.autor_service.buscar_por_id(autor_id)
            print(f"\n✍️ Autor encontrado:")
            print(f"  ID: {autor.id}")
            print(f"  Nome: {autor.nome}")
            print(f"  Nacionalidade: {autor.nacionalidade or 'N/A'}")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione Enter para continuar...")
    
    def criar_autor(self):
        """Cria um novo autor"""
        try:
            print("\n📝 Criar novo autor:")
            nome = input("Nome: ")
            nacionalidade = input("Nacionalidade (opcional): ").strip() or None
            
            autor = Autor(nome=nome, nacionalidade=nacionalidade)
            autor = self.autor_service.criar_autor(autor)
            print(f"✅ Autor criado com sucesso! ID: {autor.id}")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione Enter para continuar...")
    
    def atualizar_autor(self):
        """Atualiza um autor"""
        try:
            autor_id = self.ler_inteiro("Digite o ID do autor: ")
            print("\nDeixe em branco para não alterar:")
            nome = input("Novo nome: ").strip() or None
            dados = {}
            if nome:
                dados["nome"] = nome
            
            if dados:
                autor = self.autor_service.atualizar_autor(autor_id, dados)
                print(f"✅ Autor atualizado com sucesso!")
            else:
                print("ℹ️ Nenhuma alteração realizada.")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione Enter para continuar...")
    
    def deletar_autor(self):
        """Deleta um autor"""
        try:
            autor_id = self.ler_inteiro("Digite o ID do autor: ")
            confirmacao = input(f"Tem certeza que deseja deletar o autor {autor_id}? (s/N): ")
            if confirmacao.lower() == 's':
                self.autor_service.deletar_autor(autor_id)
                print("✅ Autor deletado com sucesso!")
            else:
                print("ℹ️ Operação cancelada.")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione Enter para continuar...")
    
    def buscar_autor_nome(self):
        """Busca autor por nome"""
        try:
            nome = input("Digite o nome do autor (busca parcial): ")
            autores = self.autor_service.buscar_por_nome(nome)
            print(f"\n✍️ Resultados encontrados: {len(autores)}")
            for autor in autores:
                print(f"  ID: {autor.id} | {autor.nome}")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione Enter para continuar...")
    
    # Métodos para Categorias
    def listar_categorias(self):
        """Lista todas as categorias"""
        try:
            categorias = self.categoria_service.listar_todos()
            if not categorias:
                print("\n📂 Nenhuma categoria cadastrada.")
            else:
                print(f"\n📂 Total de categorias: {len(categorias)}")
                for categoria in categorias:
                    print(f"  ID: {categoria.id} | {categoria.nome}")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione Enter para continuar...")
    
    def buscar_categoria(self):
        """Busca categoria por ID"""
        try:
            categoria_id = self.ler_inteiro("Digite o ID da categoria: ")
            categoria = self.categoria_service.buscar_por_id(categoria_id)
            print(f"\n📂 Categoria encontrada:")
            print(f"  ID: {categoria.id}")
            print(f"  Nome: {categoria.nome}")
            print(f"  Descrição: {categoria.descricao or 'N/A'}")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione Enter para continuar...")
    
    def criar_categoria(self):
        """Cria uma nova categoria"""
        try:
            print("\n📝 Criar nova categoria:")
            nome = input("Nome: ")
            descricao = input("Descrição (opcional): ").strip() or None
            
            categoria = Categoria(nome=nome, descricao=descricao)
            categoria = self.categoria_service.criar_categoria(categoria)
            print(f"✅ Categoria criada com sucesso! ID: {categoria.id}")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione Enter para continuar...")
    
    def atualizar_categoria(self):
        """Atualiza uma categoria"""
        try:
            categoria_id = self.ler_inteiro("Digite o ID da categoria: ")
            print("\nDeixe em branco para não alterar:")
            nome = input("Novo nome: ").strip() or None
            dados = {}
            if nome:
                dados["nome"] = nome
            
            if dados:
                categoria = self.categoria_service.atualizar_categoria(categoria_id, dados)
                print(f"✅ Categoria atualizada com sucesso!")
            else:
                print("ℹ️ Nenhuma alteração realizada.")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione Enter para continuar...")
    
    def deletar_categoria(self):
        """Deleta uma categoria"""
        try:
            categoria_id = self.ler_inteiro("Digite o ID da categoria: ")
            confirmacao = input(f"Tem certeza que deseja deletar a categoria {categoria_id}? (s/N): ")
            if confirmacao.lower() == 's':
                self.categoria_service.deletar_categoria(categoria_id)
                print("✅ Categoria deletada com sucesso!")
            else:
                print("ℹ️ Operação cancelada.")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione Enter para continuar...")
    
    def executar(self):
        """Executa a CLI"""
        try:
            while True:
                self.exibir_menu_principal()
                opcao = self.ler_opcao()
                
                if opcao == "0":
                    print("\n👋 Até logo!")
                    break
                elif opcao == "1":
                    self.processar_menu_livros()
                elif opcao == "2":
                    self.processar_menu_usuarios()
                elif opcao == "3":
                    self.processar_menu_emprestimos()
                elif opcao == "4":
                    self.processar_menu_autores()
                elif opcao == "5":
                    self.processar_menu_categorias()
                else:
                    print("❌ Opção inválida!")
        except KeyboardInterrupt:
            print("\n\n👋 Até logo!")
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
        finally:
            self.session.close()


def main():
    """Função principal"""
    cli = BibliotecaCLI()
    cli.executar()


if __name__ == "__main__":
    main()


"""
API REST principal
"""
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from typing import List, Optional
from sqlalchemy.orm import Session

from src.api.schemas import (
    LivroCreate, LivroUpdate, LivroResponse,
    UsuarioCreate, UsuarioUpdate, UsuarioResponse,
    EmprestimoCreate, EmprestimoResponse,
    AutorCreate, AutorUpdate, AutorResponse,
    CategoriaCreate, CategoriaUpdate, CategoriaResponse,
    ErrorResponse
)
from src.api.dependencies import (
    get_livro_service, get_usuario_service, get_emprestimo_service,
    get_autor_service, get_categoria_service
)
from src.services.livro_service import LivroService
from src.services.usuario_service import UsuarioService
from src.services.emprestimo_service import EmprestimoService
from src.services.autor_service import AutorService
from src.services.categoria_service import CategoriaService
from src.exceptions.biblioteca_exceptions import (
    BibliotecaException,
    EntidadeNaoEncontradaException,
    ValidacaoException,
    RegraNegocioException
)
from src.models.livro import Livro
from src.models.usuario import Usuario
from src.models.emprestimo import Emprestimo
from src.models.autor import Autor
from src.models.categoria import Categoria
from src.utils.logger import get_logger

# Cria aplicação FastAPI
app = FastAPI(
    title="Sistema de Gerenciamento de Biblioteca",
    version="1.0.0",
    description="API REST para gerenciamento de biblioteca"
)

logger = get_logger("API")


# Handler global de exceções
@app.exception_handler(BibliotecaException)
async def biblioteca_exception_handler(request, exc: BibliotecaException):
    """Handler para exceções do sistema"""
    logger.error(f"Erro: {exc.message} (Código: {exc.code})")
    return JSONResponse(
        status_code=400 if isinstance(exc, (ValidacaoException, RegraNegocioException)) else 404,
        content={"error": exc.message, "code": exc.code}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """Handler para exceções genéricas"""
    logger.error(f"Erro inesperado: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Erro interno do servidor", "code": "INTERNAL_ERROR"}
    )


# ==================== ROTAS DE LIVRO ====================

@app.post("/livros", response_model=LivroResponse, status_code=201, tags=["Livros"])
def criar_livro(
    livro_data: LivroCreate,
    service: LivroService = Depends(get_livro_service)
) -> LivroResponse:
    """Cria um novo livro"""
    livro = Livro(**livro_data.model_dump())
    if livro_data.quantidade_disponivel is None:
        livro.quantidade_disponivel = livro.quantidade_total
    livro = service.criar_livro(livro)
    return LivroResponse.model_validate(livro)


@app.get("/livros", response_model=List[LivroResponse], tags=["Livros"])
def listar_livros(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: LivroService = Depends(get_livro_service)
) -> List[LivroResponse]:
    """Lista todos os livros"""
    livros = service.listar_todos(skip, limit)
    return [LivroResponse.model_validate(livro) for livro in livros]


@app.get("/livros/{livro_id}", response_model=LivroResponse, tags=["Livros"])
def buscar_livro(
    livro_id: int,
    service: LivroService = Depends(get_livro_service)
) -> LivroResponse:
    """Busca um livro por ID"""
    livro = service.buscar_por_id(livro_id)
    return LivroResponse.model_validate(livro)


@app.put("/livros/{livro_id}", response_model=LivroResponse, tags=["Livros"])
def atualizar_livro(
    livro_id: int,
    livro_data: LivroUpdate,
    service: LivroService = Depends(get_livro_service)
) -> LivroResponse:
    """Atualiza um livro"""
    dados = livro_data.model_dump(exclude_unset=True)
    livro = service.atualizar_livro(livro_id, dados)
    return LivroResponse.model_validate(livro)


@app.delete("/livros/{livro_id}", status_code=204, tags=["Livros"])
def deletar_livro(
    livro_id: int,
    service: LivroService = Depends(get_livro_service)
):
    """Deleta um livro"""
    service.deletar_livro(livro_id)
    return None


@app.get("/livros/buscar/filtros", response_model=List[LivroResponse], tags=["Livros"])
def buscar_livros_com_filtros(
    titulo: Optional[str] = Query(None),
    autor_id: Optional[int] = Query(None),
    categoria_id: Optional[int] = Query(None),
    disponivel: Optional[bool] = Query(None),
    ordenar_por: Optional[str] = Query(None),
    ordem_desc: bool = Query(False),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: LivroService = Depends(get_livro_service)
) -> List[LivroResponse]:
    """Busca livros com filtros e ordenação"""
    filtros = {}
    if titulo:
        filtros["titulo"] = {"like": f"%{titulo}%"}
    if autor_id:
        filtros["autor_id"] = autor_id
    if categoria_id:
        filtros["categoria_id"] = categoria_id
    if disponivel is not None:
        filtros["disponivel"] = disponivel
    
    livros = service.buscar_com_filtros(filtros, skip, limit, ordenar_por, ordem_desc)
    return [LivroResponse.model_validate(livro) for livro in livros]


@app.get("/livros/disponiveis", response_model=List[LivroResponse], tags=["Livros"])
def buscar_livros_disponiveis(
    service: LivroService = Depends(get_livro_service)
) -> List[LivroResponse]:
    """Busca livros disponíveis"""
    livros = service.buscar_disponiveis()
    return [LivroResponse.model_validate(livro) for livro in livros]


# ==================== ROTAS DE USUARIO ====================

@app.post("/usuarios", response_model=UsuarioResponse, status_code=201, tags=["Usuários"])
def criar_usuario(
    usuario_data: UsuarioCreate,
    service: UsuarioService = Depends(get_usuario_service)
) -> UsuarioResponse:
    """Cria um novo usuário"""
    usuario = Usuario(**usuario_data.model_dump())
    usuario = service.criar_usuario(usuario)
    return UsuarioResponse.model_validate(usuario)


@app.get("/usuarios", response_model=List[UsuarioResponse], tags=["Usuários"])
def listar_usuarios(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: UsuarioService = Depends(get_usuario_service)
) -> List[UsuarioResponse]:
    """Lista todos os usuários"""
    usuarios = service.listar_todos(skip, limit)
    return [UsuarioResponse.model_validate(usuario) for usuario in usuarios]


@app.get("/usuarios/{usuario_id}", response_model=UsuarioResponse, tags=["Usuários"])
def buscar_usuario(
    usuario_id: int,
    service: UsuarioService = Depends(get_usuario_service)
) -> UsuarioResponse:
    """Busca um usuário por ID"""
    usuario = service.buscar_por_id(usuario_id)
    return UsuarioResponse.model_validate(usuario)


@app.put("/usuarios/{usuario_id}", response_model=UsuarioResponse, tags=["Usuários"])
def atualizar_usuario(
    usuario_id: int,
    usuario_data: UsuarioUpdate,
    service: UsuarioService = Depends(get_usuario_service)
) -> UsuarioResponse:
    """Atualiza um usuário"""
    dados = usuario_data.model_dump(exclude_unset=True)
    usuario = service.atualizar_usuario(usuario_id, dados)
    return UsuarioResponse.model_validate(usuario)


@app.delete("/usuarios/{usuario_id}", status_code=204, tags=["Usuários"])
def deletar_usuario(
    usuario_id: int,
    service: UsuarioService = Depends(get_usuario_service)
):
    """Deleta um usuário"""
    service.deletar_usuario(usuario_id)
    return None


@app.get("/usuarios/buscar/filtros", response_model=List[UsuarioResponse], tags=["Usuários"])
def buscar_usuarios_com_filtros(
    nome: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    ativo: Optional[bool] = Query(None),
    ordenar_por: Optional[str] = Query(None),
    ordem_desc: bool = Query(False),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: UsuarioService = Depends(get_usuario_service)
) -> List[UsuarioResponse]:
    """Busca usuários com filtros e ordenação"""
    filtros = {}
    if nome:
        filtros["nome"] = {"like": f"%{nome}%"}
    if email:
        filtros["email"] = email
    if ativo is not None:
        filtros["ativo"] = ativo
    
    usuarios = service.buscar_com_filtros(filtros, skip, limit, ordenar_por, ordem_desc)
    return [UsuarioResponse.model_validate(usuario) for usuario in usuarios]


# ==================== ROTAS DE EMPRESTIMO ====================

@app.post("/emprestimos", response_model=EmprestimoResponse, status_code=201, tags=["Empréstimos"])
def criar_emprestimo(
    emprestimo_data: EmprestimoCreate,
    service: EmprestimoService = Depends(get_emprestimo_service)
) -> EmprestimoResponse:
    """Cria um novo empréstimo"""
    emprestimo = service.criar_emprestimo(
        emprestimo_data.livro_id,
        emprestimo_data.usuario_id
    )
    return EmprestimoResponse.model_validate(emprestimo)


@app.get("/emprestimos", response_model=List[EmprestimoResponse], tags=["Empréstimos"])
def listar_emprestimos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: EmprestimoService = Depends(get_emprestimo_service)
) -> List[EmprestimoResponse]:
    """Lista todos os empréstimos"""
    emprestimos = service.listar_todos(skip, limit)
    return [EmprestimoResponse.model_validate(emp) for emp in emprestimos]


# Rotas específicas devem vir ANTES das rotas com parâmetros
@app.get("/emprestimos/atrasados", response_model=List[EmprestimoResponse], tags=["Empréstimos"])
def buscar_emprestimos_atrasados(
    service: EmprestimoService = Depends(get_emprestimo_service)
) -> List[EmprestimoResponse]:
    """Busca empréstimos atrasados"""
    emprestimos = service.buscar_atrasados()
    return [EmprestimoResponse.model_validate(emp) for emp in emprestimos]


@app.get("/emprestimos/usuario/{usuario_id}", response_model=List[EmprestimoResponse], tags=["Empréstimos"])
def buscar_emprestimos_usuario(
    usuario_id: int,
    service: EmprestimoService = Depends(get_emprestimo_service)
) -> List[EmprestimoResponse]:
    """Busca empréstimos de um usuário"""
    emprestimos = service.buscar_por_usuario(usuario_id)
    return [EmprestimoResponse.model_validate(emp) for emp in emprestimos]


@app.get("/emprestimos/{emprestimo_id}", response_model=EmprestimoResponse, tags=["Empréstimos"])
def buscar_emprestimo(
    emprestimo_id: int,
    service: EmprestimoService = Depends(get_emprestimo_service)
) -> EmprestimoResponse:
    """Busca um empréstimo por ID"""
    emprestimo = service.buscar_por_id(emprestimo_id)
    return EmprestimoResponse.model_validate(emprestimo)


@app.post("/emprestimos/{emprestimo_id}/devolver", response_model=EmprestimoResponse, tags=["Empréstimos"])
def devolver_emprestimo(
    emprestimo_id: int,
    service: EmprestimoService = Depends(get_emprestimo_service)
) -> EmprestimoResponse:
    """Devolve um empréstimo"""
    emprestimo = service.devolver_emprestimo(emprestimo_id)
    return EmprestimoResponse.model_validate(emprestimo)


@app.get("/emprestimos/{emprestimo_id}/multa", tags=["Empréstimos"])
def calcular_multa_emprestimo(
    emprestimo_id: int,
    service: EmprestimoService = Depends(get_emprestimo_service)
):
    """Calcula a multa de um empréstimo"""
    multa = service.calcular_multa_emprestimo(emprestimo_id)
    return {"emprestimo_id": emprestimo_id, "multa": multa}


# ==================== ROTAS DE AUTOR ====================

@app.post("/autores", response_model=AutorResponse, status_code=201, tags=["Autores"])
def criar_autor(
    autor_data: AutorCreate,
    service: AutorService = Depends(get_autor_service)
) -> AutorResponse:
    """Cria um novo autor"""
    autor = Autor(**autor_data.model_dump())
    autor = service.criar_autor(autor)
    return AutorResponse.model_validate(autor)


@app.get("/autores", response_model=List[AutorResponse], tags=["Autores"])
def listar_autores(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: AutorService = Depends(get_autor_service)
) -> List[AutorResponse]:
    """Lista todos os autores"""
    autores = service.listar_todos(skip, limit)
    return [AutorResponse.model_validate(autor) for autor in autores]


@app.get("/autores/{autor_id}", response_model=AutorResponse, tags=["Autores"])
def buscar_autor(
    autor_id: int,
    service: AutorService = Depends(get_autor_service)
) -> AutorResponse:
    """Busca um autor por ID"""
    autor = service.buscar_por_id(autor_id)
    return AutorResponse.model_validate(autor)


@app.put("/autores/{autor_id}", response_model=AutorResponse, tags=["Autores"])
def atualizar_autor(
    autor_id: int,
    autor_data: AutorUpdate,
    service: AutorService = Depends(get_autor_service)
) -> AutorResponse:
    """Atualiza um autor"""
    dados = autor_data.model_dump(exclude_unset=True)
    autor = service.atualizar_autor(autor_id, dados)
    return AutorResponse.model_validate(autor)


@app.delete("/autores/{autor_id}", status_code=204, tags=["Autores"])
def deletar_autor(
    autor_id: int,
    service: AutorService = Depends(get_autor_service)
):
    """Deleta um autor"""
    service.deletar_autor(autor_id)
    return None


# ==================== ROTAS DE CATEGORIA ====================

@app.post("/categorias", response_model=CategoriaResponse, status_code=201, tags=["Categorias"])
def criar_categoria(
    categoria_data: CategoriaCreate,
    service: CategoriaService = Depends(get_categoria_service)
) -> CategoriaResponse:
    """Cria uma nova categoria"""
    categoria = Categoria(**categoria_data.model_dump())
    categoria = service.criar_categoria(categoria)
    return CategoriaResponse.model_validate(categoria)


@app.get("/categorias", response_model=List[CategoriaResponse], tags=["Categorias"])
def listar_categorias(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: CategoriaService = Depends(get_categoria_service)
) -> List[CategoriaResponse]:
    """Lista todas as categorias"""
    categorias = service.listar_todos(skip, limit)
    return [CategoriaResponse.model_validate(cat) for cat in categorias]


@app.get("/categorias/{categoria_id}", response_model=CategoriaResponse, tags=["Categorias"])
def buscar_categoria(
    categoria_id: int,
    service: CategoriaService = Depends(get_categoria_service)
) -> CategoriaResponse:
    """Busca uma categoria por ID"""
    categoria = service.buscar_por_id(categoria_id)
    return CategoriaResponse.model_validate(categoria)


@app.put("/categorias/{categoria_id}", response_model=CategoriaResponse, tags=["Categorias"])
def atualizar_categoria(
    categoria_id: int,
    categoria_data: CategoriaUpdate,
    service: CategoriaService = Depends(get_categoria_service)
) -> CategoriaResponse:
    """Atualiza uma categoria"""
    dados = categoria_data.model_dump(exclude_unset=True)
    categoria = service.atualizar_categoria(categoria_id, dados)
    return CategoriaResponse.model_validate(categoria)


@app.delete("/categorias/{categoria_id}", status_code=204, tags=["Categorias"])
def deletar_categoria(
    categoria_id: int,
    service: CategoriaService = Depends(get_categoria_service)
):
    """Deleta uma categoria"""
    service.deletar_categoria(categoria_id)
    return None


# ==================== ROTA RAIZ ====================

@app.get("/", tags=["Sistema"])
def root():
    """Endpoint raiz com informações da API"""
    return {
        "message": "Sistema de Gerenciamento de Biblioteca API",
        "version": "1.0.0",
        "documentation": "/docs",
        "health": "/health",
        "endpoints": {
            "livros": "/livros",
            "usuarios": "/usuarios",
            "emprestimos": "/emprestimos",
            "autores": "/autores",
            "categorias": "/categorias"
        }
    }


# ==================== ROTA DE HEALTH CHECK ====================

@app.get("/health", tags=["Sistema"])
def health_check():
    """Endpoint de health check"""
    return {"status": "ok", "message": "Sistema de Biblioteca está funcionando"}


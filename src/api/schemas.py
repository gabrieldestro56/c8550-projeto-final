"""
Schemas Pydantic para validação de entrada/saída da API
"""
from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field


# Schemas de Livro
class LivroBase(BaseModel):
    """Schema base para Livro"""
    titulo: str = Field(..., min_length=1, max_length=300)
    ano_publicacao: Optional[int] = Field(None, ge=1000, le=2100)
    editora: Optional[str] = Field(None, max_length=200)
    numero_paginas: Optional[int] = Field(None, gt=0)
    sinopse: Optional[str] = None
    preco: Optional[float] = Field(None, ge=0)
    quantidade_total: int = Field(1, gt=0)
    quantidade_disponivel: Optional[int] = Field(None, ge=0)
    autor_id: int = Field(..., gt=0)
    categoria_id: Optional[int] = Field(None, gt=0)


class LivroCreate(LivroBase):
    """Schema para criação de Livro"""
    pass


class LivroUpdate(BaseModel):
    """Schema para atualização de Livro"""
    titulo: Optional[str] = Field(None, min_length=1, max_length=300)
    ano_publicacao: Optional[int] = Field(None, ge=1000, le=2100)
    editora: Optional[str] = Field(None, max_length=200)
    numero_paginas: Optional[int] = Field(None, gt=0)
    sinopse: Optional[str] = None
    preco: Optional[float] = Field(None, ge=0)
    quantidade_total: Optional[int] = Field(None, gt=0)
    quantidade_disponivel: Optional[int] = Field(None, ge=0)
    autor_id: Optional[int] = Field(None, gt=0)
    categoria_id: Optional[int] = Field(None, gt=0)
    disponivel: Optional[bool] = None


class LivroResponse(LivroBase):
    """Schema de resposta para Livro"""
    id: int
    disponivel: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Schemas de Usuario
class UsuarioBase(BaseModel):
    """Schema base para Usuario"""
    nome: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    data_nascimento: date


class UsuarioCreate(UsuarioBase):
    """Schema para criação de Usuario"""
    pass


class UsuarioUpdate(BaseModel):
    """Schema para atualização de Usuario"""
    nome: Optional[str] = Field(None, min_length=1, max_length=200)
    email: Optional[EmailStr] = None
    data_nascimento: Optional[date] = None
    ativo: Optional[bool] = None


class UsuarioResponse(UsuarioBase):
    """Schema de resposta para Usuario"""
    id: int
    ativo: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Schemas de Emprestimo
class EmprestimoBase(BaseModel):
    """Schema base para Emprestimo"""
    livro_id: int = Field(..., gt=0)
    usuario_id: int = Field(..., gt=0)


class EmprestimoCreate(EmprestimoBase):
    """Schema para criação de Emprestimo"""
    pass


class EmprestimoResponse(EmprestimoBase):
    """Schema de resposta para Emprestimo"""
    id: int
    data_emprestimo: date
    data_prevista_devolucao: date
    data_devolucao: Optional[date]
    devolvido: bool
    multa: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Schemas de Autor
class AutorBase(BaseModel):
    """Schema base para Autor"""
    nome: str = Field(..., min_length=1, max_length=200)
    nacionalidade: Optional[str] = Field(None, max_length=100)
    data_nascimento: Optional[date] = None
    biografia: Optional[str] = Field(None, max_length=1000)


class AutorCreate(AutorBase):
    """Schema para criação de Autor"""
    pass


class AutorUpdate(BaseModel):
    """Schema para atualização de Autor"""
    nome: Optional[str] = Field(None, min_length=1, max_length=200)
    nacionalidade: Optional[str] = Field(None, max_length=100)
    data_nascimento: Optional[date] = None
    biografia: Optional[str] = Field(None, max_length=1000)


class AutorResponse(AutorBase):
    """Schema de resposta para Autor"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Schemas de Categoria
class CategoriaBase(BaseModel):
    """Schema base para Categoria"""
    nome: str = Field(..., min_length=1, max_length=100)
    descricao: Optional[str] = None


class CategoriaCreate(CategoriaBase):
    """Schema para criação de Categoria"""
    pass


class CategoriaUpdate(BaseModel):
    """Schema para atualização de Categoria"""
    nome: Optional[str] = Field(None, min_length=1, max_length=100)
    descricao: Optional[str] = None


class CategoriaResponse(CategoriaBase):
    """Schema de resposta para Categoria"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Schema de resposta de erro
class ErrorResponse(BaseModel):
    """Schema para respostas de erro"""
    error: str
    code: str
    detail: Optional[str] = None


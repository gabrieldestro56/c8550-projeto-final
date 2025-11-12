"""
Repositório base com interface abstrata
"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc

from src.database.base import BaseModel

T = TypeVar('T', bound=BaseModel)


class IRepository(ABC, Generic[T]):
    """Interface abstrata para repositórios"""
    
    @abstractmethod
    def criar(self, entidade: T) -> T:
        """
        Cria uma nova entidade
        
        Args:
            entidade: Entidade a ser criada
        
        Returns:
            Entidade criada
        """
        pass
    
    @abstractmethod
    def buscar_por_id(self, id: int) -> Optional[T]:
        """
        Busca uma entidade por ID
        
        Args:
            id: ID da entidade
        
        Returns:
            Entidade encontrada ou None
        """
        pass
    
    @abstractmethod
    def listar_todos(self, skip: int = 0, limit: int = 100) -> List[T]:
        """
        Lista todas as entidades
        
        Args:
            skip: Número de registros a pular
            limit: Número máximo de registros a retornar
        
        Returns:
            Lista de entidades
        """
        pass
    
    @abstractmethod
    def atualizar(self, entidade: T) -> T:
        """
        Atualiza uma entidade
        
        Args:
            entidade: Entidade a ser atualizada
        
        Returns:
            Entidade atualizada
        """
        pass
    
    @abstractmethod
    def deletar(self, id: int) -> bool:
        """
        Deleta uma entidade
        
        Args:
            id: ID da entidade a ser deletada
        
        Returns:
            True se deletado com sucesso, False caso contrário
        """
        pass


class BaseRepository(IRepository[T]):
    """Implementação base do repositório"""
    
    def __init__(self, session: Session, model_class: type[T]) -> None:
        """
        Inicializa o repositório
        
        Args:
            session: Sessão do banco de dados
            model_class: Classe do modelo
        """
        self.session = session
        self.model_class = model_class
    
    def criar(self, entidade: T) -> T:
        """Cria uma nova entidade"""
        self.session.add(entidade)
        self.session.commit()
        self.session.refresh(entidade)
        return entidade
    
    def buscar_por_id(self, id: int) -> Optional[T]:
        """Busca uma entidade por ID"""
        return self.session.query(self.model_class).filter(self.model_class.id == id).first()
    
    def listar_todos(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Lista todas as entidades"""
        return self.session.query(self.model_class).offset(skip).limit(limit).all()
    
    def atualizar(self, entidade: T) -> T:
        """Atualiza uma entidade"""
        self.session.commit()
        self.session.refresh(entidade)
        return entidade
    
    def deletar(self, id: int) -> bool:
        """Deleta uma entidade"""
        entidade = self.buscar_por_id(id)
        if entidade:
            self.session.delete(entidade)
            self.session.commit()
            return True
        return False
    
    def buscar_com_filtros(
        self,
        filtros: Dict[str, Any],
        skip: int = 0,
        limit: int = 100,
        ordenar_por: Optional[str] = None,
        ordem_desc: bool = False
    ) -> List[T]:
        """
        Busca entidades com filtros e ordenação
        
        Args:
            filtros: Dicionário com filtros a aplicar
            skip: Número de registros a pular
            limit: Número máximo de registros
            ordenar_por: Campo para ordenação
            ordem_desc: Se True, ordena em ordem decrescente
        
        Returns:
            Lista de entidades filtradas
        """
        query = self.session.query(self.model_class)
        
        # Aplica filtros
        for campo, valor in filtros.items():
            if hasattr(self.model_class, campo):
                if isinstance(valor, dict):
                    # Suporta operadores como {'like': '%texto%'}
                    for op, val in valor.items():
                        if op == 'like':
                            query = query.filter(getattr(self.model_class, campo).like(val))
                        elif op == 'gt':
                            query = query.filter(getattr(self.model_class, campo) > val)
                        elif op == 'lt':
                            query = query.filter(getattr(self.model_class, campo) < val)
                        elif op == 'gte':
                            query = query.filter(getattr(self.model_class, campo) >= val)
                        elif op == 'lte':
                            query = query.filter(getattr(self.model_class, campo) <= val)
                else:
                    query = query.filter(getattr(self.model_class, campo) == valor)
        
        # Aplica ordenação
        if ordenar_por and hasattr(self.model_class, ordenar_por):
            if ordem_desc:
                query = query.order_by(desc(getattr(self.model_class, ordenar_por)))
            else:
                query = query.order_by(asc(getattr(self.model_class, ordenar_por)))
        
        return query.offset(skip).limit(limit).all()


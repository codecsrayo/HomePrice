from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID
from fastapi_pagination.ext.async_sqlmodel import paginate
from fastapi_pagination import Params, Page
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import text
from sqlmodel import SQLModel, select, func
from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import Select, SelectOfScalar

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
SchemaType = TypeVar("SchemaType", bound=BaseModel)
T = TypeVar("T", bound=SQLModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(
        self,
        db_session: AsyncSession,
        *,
        id: Union[UUID, str, int],
        query: Optional[Union[T, Select[T], SelectOfScalar[T]]] = None
    ) -> Optional[ModelType]:

        if isinstance(query, (Select, SelectOfScalar, str)):
            response = await db_session.exec(query)
            return response.one_or_none()
        response = await db_session.exec(
            select(self.model).where(self.model.id == id).options(selectinload("*"))
        )
        return response.one_or_none()

    async def get_by_ids(
        self,
        db_session: AsyncSession,
        list_ids: List[Union[UUID, str]],
    ) -> Optional[List[ModelType]]:
        response = await db_session.exec(
            select(self.model).where(self.model.id.in_(list_ids))
        )
        return response.all()

    async def get_count(
        self,
        db_session: AsyncSession,
        query: Optional[Union[T, Select[T], SelectOfScalar[T]]] = None,
    ) -> Optional[ModelType]:
        response = await db_session.exec(
            select(func.count()).select_from(select(self.model).subquery())
        )
        return response.one()

    async def get_multi(
        self, db_session: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        response = await db_session.exec(
            select(self.model).offset(skip).limit(limit).order_by(self.model.id)
        )
        return response.all()

    async def get_multi_paginated(
        self,
        db_session: AsyncSession,
        *,
        params: Optional[Params] = Params(),
        query: Optional[Union[T, Select[T], SelectOfScalar[T]]] = None
    ) -> Page[ModelType]:
        # if not query:
        #     query = self.model
        return await paginate(db_session, query, params)

    async def create(
        self,
        db_session: AsyncSession,
        *,
        obj_in: Union[CreateSchemaType, ModelType],
    ) -> ModelType:
        db_obj = self.model.model_validate(obj_in)
        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db_session: AsyncSession,
        *,
        obj_current: ModelType,
        obj_new: Union[UpdateSchemaType, Dict[str, Any], ModelType]
    ) -> ModelType:
        obj_data = jsonable_encoder(obj_current)

        if isinstance(obj_new, dict):
            update_data = obj_new
        else:
            # This tells Pydantic to not include the values that were not sent
            update_data = obj_new.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(obj_current, field, update_data[field])
            if field == "updated_at":
                setattr(obj_current, field, datetime.utcnow())

            if field == "DateUpdate":
                setattr(obj_current, field, datetime.utcnow())

            if field == "FechaSistema":
                setattr(obj_current, field, datetime.utcnow())

        db_session.add(obj_current)
        await db_session.commit()
        await db_session.refresh(obj_current)
        return obj_current

    async def remove(
        self,
        db_session: AsyncSession,
        *,
        id: Union[UUID, str],
        query: Optional[Union[T, Select[T], SelectOfScalar[T]]] = None
    ) -> ModelType:
        if not query:
            response = await db_session.exec(
                select(self.model).where(self.model.id == id)
            )
        else:
            response = await db_session.exec(query)
        obj = response.one()
        await db_session.delete(obj)
        await db_session.commit()
        return obj

__all__ = ["CRUDBase"]

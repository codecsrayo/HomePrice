from typing import Generic, Optional, TypeVar
from pydantic.generics import GenericModel



DataType = TypeVar("DataType")


# Path: app/app/schemas/common.py
class IResponseBase(GenericModel, Generic[DataType]):
    message: str = ""
    meta: dict = {}
    data: Optional[DataType] = None


class IGetResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str = "Data got correctly"


class IPostResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str = "Data created correctly"


class IPutResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str = "Data updated correctly"


class IDeleteResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str = "Data deleted correctly"

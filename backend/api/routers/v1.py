from datetime import datetime
from decimal import Decimal
import uuid as uuid_pkg
from typing import TypeVar, Union

from fastapi import APIRouter, Depends
from sqlmodel import select, func, and_, col
from sqlmodel.ext.asyncio.session import AsyncSession

from api.models import CRUDBase, Prediction, Property
from api.routers import deps

from .common import (
    IPostResponseBase,
    IGetResponseBase,
    # IDeleteResponseBase,
    # IPutResponseBase,
    # IResponseBase
)

router = APIRouter()


ResponseT = TypeVar("ResponseT", bound=Union[Property, Prediction])


@router.post("/predict", response_model=IPostResponseBase[ResponseT])
async def predict(data: Property, db_session: AsyncSession = Depends(deps.get_db)):

    id = uuid_pkg.uuid4()
    save = await CRUDBase(Property).create(
        db_session=db_session, obj_in=data.model_dump(exclude={"id"}), created_by_id=id
    )

    prediction = Prediction(
            property_id=id,
            predicted_price=0.1,
            # prediction_date=datetime.now(),
            # property="test",
            # model_predictions="550e8400-e29b-41d4-a716-446655440009"
        )
    print(prediction)
    await CRUDBase(Prediction).create(
        db_session=db_session, obj_in=prediction, created_by_id=id)
    return IPostResponseBase[ResponseT](data=save)


@router.get("/predict/{id}", response_model=IGetResponseBase[ResponseT])
async def get_predict(
    id: uuid_pkg.UUID, db_session: AsyncSession = Depends(deps.get_db)
):

    # Consulta de la propiedad
    query_property = await CRUDBase(Property).get(db_session=db_session, id=id)

    # Consulta de la predicción relacionada con la propiedad
    query_prediction = await CRUDBase(Prediction).get(
        db_session=db_session,
        id=id,
        query=select(Prediction).where(Prediction.property_id == id),
    )

    # Verificar que ambos resultados existan
    query_result = query_property is not None and query_prediction is not None
    print(query_result)

    # Si ambos existen, combinar los resultados
    if query_result:
        # Combinar los resultados en ResponseT
        query_result = ResponseT(**property_data, **prediction_data)

    # Devolver la respuesta usando IGetResponseBase
    return IGetResponseBase[ResponseT](data=query_result)



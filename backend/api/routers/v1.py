from datetime import datetime
from decimal import Decimal
import uuid as uuid_pkg
from typing import TypeVar, Union

from fastapi import APIRouter, Depends
from sqlmodel import select
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


@router.post("/predict")
async def predict(data: Property, db_session: AsyncSession = Depends(deps.get_db)):
    data.id =  uuid_pkg.uuid4()
    save_property = await CRUDBase(Property).create(db_session=db_session, obj_in=data)

    data_predict =Prediction(
      id=uuid_pkg.uuid4(),
      property_id=save_property.id, 
      predicted_price=20.0,

    )

    db_session.add(data_predict)
    await db_session.commit()
    await db_session.refresh(data_predict)


    return {'id': data.id}



@router.get("/predict/history")
async def get_all_predict(
    db_session: AsyncSession = Depends(deps.get_db)
):
    # Consulta para obtener todas las propiedades con sus predicciones
    query = (
        select(Property, Prediction)
        .outerjoin(Prediction, Property.id == Prediction.property_id)
        .order_by(Prediction.prediction_date.desc())
    )
    
    result = await db_session.execute(query)
    rows = result.fetchall()

    # Procesar los resultados
    properties_with_predictions = []
    for property, prediction in rows:
        property_dict = property.dict()
        if prediction:
            property_dict["prediction"] = prediction.dict()
        else:
            property_dict["prediction"] = None
        properties_with_predictions.append(property_dict)

    return {
        "total": len(properties_with_predictions),
        "items": properties_with_predictions
    }



@router.get("/predict/history/{id}")
async def get_id(
    id: uuid_pkg.UUID,
    db_session: AsyncSession = Depends(deps.get_db),
):

    property = await CRUDBase(Property).get(db_session=db_session, id=id)
    predict = await CRUDBase(Prediction).get(db_session=db_session, id=id, query=select(Prediction).where(Prediction.property_id==id))  
    if not predict:
       return None
    return { 'id': id, **property.__dict__,  **predict.dict(exclude={'id'})}
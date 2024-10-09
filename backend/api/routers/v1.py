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


@router.post("/predict")
async def predict(data: Property, db_session: AsyncSession = Depends(deps.get_db)):


    return {
  "id": uuid_pkg.uuid4(),
  "address": "123 Main St",
  "city": "Springfield",
  "state": "IL",
  "zip_code": "62704",
  "bedrooms": 3,
  "bathrooms": 2,
  "square_feet": 1500,
  "lot_size": 5000,
  "year_built": 1990,
  "property_type": "Single Family Home",
  "price": 250000,
  "predicted_price": 275000,
  "prediction_date": "2024-09-22T10:00:00Z",
  "features": [
    {
      "id": "76a1f97e-9bde-4f8e-a49b-5b97f1d207a6",
      "feature_name": "Garage",
      "feature_value": "2 Car"
    },
    {
      "id": "c6bf0fb9-ec6d-4f34-86db-20c1baf7e27a",
      "feature_name": "Pool",
      "feature_value": "In-ground"
    }
  ],
  "ml_model_predictions": [
    {
      "ml_model": {
        "ml_model_tag": "RandomForest",
        "ml_model_version": "1.0.0",
        "created_at": "2024-09-20T08:30:00Z"
      }
    }
  ]
}



@router.get("/predict/history")
async def get_all_predict(
    db_session: AsyncSession = Depends(deps.get_db)
):
    return {
  "total": 2,
  "items": [
    {
      "id": "64b2f871-dfb5-4023-9c6f-9e765f5fa8a9",
      "address": "123 Main St",
      "city": "Springfield",
      "state": "IL",
      "zip_code": "62704",
      "bedrooms": 3,
      "bathrooms": 2,
      "square_feet": 1500,
      "lot_size": 5000,
      "year_built": 1990,
      "property_type": "Single Family Home",
      "price": 250000,
      "predicted_price": 275000,
      "prediction_date": "2024-09-22T10:00:00Z",
      "features": [
        {
          "id": "76a1f97e-9bde-4f8e-a49b-5b97f1d207a6",
          "feature_name": "Garage",
          "feature_value": "2 Car"
        },
        {
          "id": "c6bf0fb9-ec6d-4f34-86db-20c1baf7e27a",
          "feature_name": "Pool",
          "feature_value": "In-ground"
        }
      ],
      "ml_model_predictions": [
        {
          "ml_model": {
            "ml_model_tag": "RandomForest",
            "ml_model_version": "1.0.0",
            "created_at": "2024-09-20T08:30:00Z"
          }
        }
      ]
    },
    {
      "id": "21b2e771-bdf5-4419-b2cf-2e46415d93a0",
      "address": "456 Elm St",
      "city": "Springfield",
      "state": "IL",
      "zip_code": "62705",
      "bedrooms": 4,
      "bathrooms": 3,
      "square_feet": 2000,
      "lot_size": 8000,
      "year_built": 1985,
      "property_type": "Single Family Home",
      "price": 350000,
      "predicted_price": 365000,
      "prediction_date": "2024-09-15T14:30:00Z",
      "features": [
        {
          "id": "f5f25b4d-a6e7-421a-83d1-295e39f7d84b",
          "feature_name": "Fireplace",
          "feature_value": "Wood Burning"
        },
        {
          "id": "2f13491d-5fa1-4a1f-85f5-56bb0a5f8d92",
          "feature_name": "Deck",
          "feature_value": "Large"
        }
      ],
      "ml_model_predictions": [
        {
          "ml_model": {
            "ml_model_tag": "LinearRegression",
            "ml_model_version": "2.0.0",
            "created_at": "2024-09-10T11:00:00Z"
          }
        }
      ]
    }
  ]
}


   



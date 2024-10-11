from typing import Optional
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, DateTime, Numeric
from sqlmodel import Field,  Relationship
import uuid as uuid_pkg
from .id import BaseUUIDModel


class Property(BaseUUIDModel, table=True):
    __tablename__ = "properties"
    address: str
    city: str
    state: str
    zip_code: str
    bedrooms: int
    bathrooms: int
    square_feet: int
    lot_size: Optional[int] = None
    year_built: Optional[int] = None
    property_type: Optional[str] = None
    price: Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(12, 2)))
    
    features: list["Feature"] = Relationship(back_populates="property")
    predictions: list["Prediction"] = Relationship(back_populates="property")



class Prediction(BaseUUIDModel, table=True):
    __tablename__ = "predictions"
    
    property_id: uuid_pkg.UUID = Field(foreign_key="properties.id")
    predicted_price: Decimal = Field(sa_column=Column(Numeric(12, 2)))
    prediction_date: datetime = Field(
        default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True))
    )
    
    property: Property = Relationship(back_populates="predictions")
    ml_model_predictions: list["MLModelPrediction"] = Relationship(
        back_populates="prediction"
    )

class Feature(BaseUUIDModel, table=True):
    __tablename__ = "features"
    
    property_id: uuid_pkg.UUID = Field(foreign_key="properties.id")
    feature_name: str
    feature_value: Optional[str] = None
    
    property: Property = Relationship(back_populates="features")
class MLModel(BaseUUIDModel, table=True):
    __tablename__ = "ml_models"
    
    ml_model_tag: str
    ml_model_version: str
    created_at: datetime = Field(
        default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True))
    )
    
    ml_model_predictions: list["MLModelPrediction"] = Relationship(back_populates="ml_model")

class MLModelPrediction(BaseUUIDModel, table=True):
    __tablename__ = "ml_model_predictions"
    
    ml_model_id: uuid_pkg.UUID = Field(foreign_key="ml_models.id")
    prediction_id: uuid_pkg.UUID = Field(foreign_key="predictions.id")
    
    ml_model: MLModel = Relationship(back_populates="ml_model_predictions")
    prediction: Prediction = Relationship(back_populates="ml_model_predictions")

__all__ = [
"Property",
"Feature",
"Prediction",
"MLModel",
"MLModelPrediction",
]



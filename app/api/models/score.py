from typing import Optional
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, DateTime, Numeric
from sqlmodel import Field, SQLModel, Relationship


class Property(SQLModel, table=True):
    __tablename__ = "properties"

    id: Optional[int] = Field(default=None, primary_key=True)
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


class Feature(SQLModel, table=True):
    __tablename__ = "features"

    id: Optional[int] = Field(default=None, primary_key=True)
    property_id: int = Field(foreign_key="properties.id")
    feature_name: str
    feature_value: Optional[str] = None

    property: Property = Relationship(back_populates="features")


class Prediction(SQLModel, table=True):
    __tablename__ = "predictions"

    id: Optional[int] = Field(default=None, primary_key=True)
    property_id: int = Field(foreign_key="properties.id")
    predicted_price: Decimal = Field(sa_column=Column(Numeric(12, 2)))
    prediction_date: datetime = Field(
        default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True))
    )

    property: Property = Relationship(back_populates="predictions")
    model_predictions: list["ModelPrediction"] = Relationship(
        back_populates="prediction"
    )


class Model(SQLModel, table=True):
    __tablename__ = "models"

    id: Optional[int] = Field(default=None, primary_key=True)
    model_name: str
    model_version: str
    created_at: datetime = Field(
        default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True))
    )

    model_predictions: list["ModelPrediction"] = Relationship(back_populates="model")


class ModelPrediction(SQLModel, table=True):
    __tablename__ = "model_predictions"

    id: Optional[int] = Field(default=None, primary_key=True)
    model_id: int = Field(foreign_key="models.id")
    prediction_id: int = Field(foreign_key="predictions.id")

    model: Model = Relationship(back_populates="model_predictions")
    prediction: Prediction = Relationship(back_populates="model_predictions")

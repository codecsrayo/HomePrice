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




class Feature(BaseUUIDModel, table=True):
    __tablename__ = "features"

    property_id: uuid_pkg.UUID = Field(foreign_key="properties.id")
    feature_name: str
    feature_value: Optional[str] = None

    property: Property = Relationship(back_populates="features")


class Prediction(BaseUUIDModel, table=True):
    __tablename__ = "predictions"

    property_id: uuid_pkg.UUID = Field(foreign_key="properties.id")
    predicted_price: Decimal = Field(sa_column=Column(Numeric(12, 2)))
    prediction_date: datetime = Field(
        default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True))
    )

    property: Property = Relationship(back_populates="predictions")
    model_predictions: list["ModelPrediction"] = Relationship(
        back_populates="prediction"
    )


class Model(BaseUUIDModel, table=True):
    __tablename__ = "models"

    model_tag: str
    model_version: str
    created_at: datetime = Field(
        default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True))
    )

    model_predictions: list["ModelPrediction"] = Relationship(back_populates="model")


class ModelPrediction(BaseUUIDModel, table=True):
    __tablename__ = "model_predictions"

    model_id: uuid_pkg.UUID = Field(foreign_key="models.id")
    prediction_id: uuid_pkg.UUID = Field(foreign_key="predictions.id")

    model: Model = Relationship(back_populates="model_predictions")
    prediction: Prediction = Relationship(back_populates="model_predictions")

__all__ = [
"Property",
"Feature",
"Prediction",
"Model",
"ModelPrediction",
]


# Database setup (example with SQLite)
# DATABASE_URL = "sqlite:///./test.db"
# engine = create_engine(DATABASE_URL)

# Create tables
# SQLModel.metadata.create_all(engine)

# Example data insertion
def insert_property(property_data: Property):...
    # with Session(engine) as session:
    #     session.add(property_data)
    #     session.commit()
    #     session.refresh(property_data)
    # return property_data.id

def insert_prediction(prediction_data: Prediction):...
    # with Session(engine) as session:
    #     session.add(prediction_data)
    #     session.commit()
    #     session.refresh(prediction_data)
    # return prediction_data.id

def insert_model(model_data: Model):...
    # with Session(engine) as session:
    #     session.add(model_data)
    #     session.commit()
    #     session.refresh(model_data)
    # return model_data.id

def insert_model_prediction(model_prediction_data: ModelPrediction):...
    # with Session(engine) as session:
    #     session.add(model_prediction_data)
    #     session.commit()
    #     session.refresh(model_prediction_data)
    # return model_prediction_data.id

# Example usage
property_data = Property(
    address="123 Main St",
    city="Springfield",
    state="IL",
    zip_code="62701",
    bedrooms=3,
    bathrooms=2,
    square_feet=1500,
    lot_size=5000,
    year_built=1990,
    property_type="Single Family",
    price=Decimal("250000.00"),
    features=[
        Feature(feature_name="Garage", feature_value="2 car"),
        Feature(feature_name="Pool", feature_value="Yes")
    ]
)

property_id = insert_property(property_data)

prediction_data = Prediction(
    property_id=property_id,
    predicted_price=Decimal("255000.00")
)

prediction_id = insert_prediction(prediction_data)

model_data = Model(
    model_tag="RandomForestRegressor",
    model_version="1.0.0"
)

model_id = insert_model(model_data)

model_prediction_data = ModelPrediction(
    model_id=model_id,
    prediction_id=prediction_id
)

model_prediction_id = insert_model_prediction(model_prediction_data)

print(f"Inserted property with ID: {property_id}")
print(f"Inserted prediction with ID: {prediction_id}")
print(f"Inserted model with ID: {model_id}")
print(f"Inserted model prediction with ID: {model_prediction_id}")
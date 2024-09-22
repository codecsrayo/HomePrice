from typing import Type
from .models import Property, Feature, Prediction, MLModel, MLModelPrediction
from .crud_base import CRUDBase  # Tu clase CRUDBase definida anteriormente
from pydantic import BaseModel


# Esquemas Pydantic para validaciones
class PropertyCreate(BaseModel):
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
    price: Optional[Decimal] = None


class PropertyUpdate(BaseModel):
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    square_feet: Optional[int] = None
    lot_size: Optional[int] = None
    year_built: Optional[int] = None
    property_type: Optional[str] = None
    price: Optional[Decimal] = None


# CRUD para la clase Property
class CRUDProperty(CRUDBase[Property, PropertyCreate, PropertyUpdate]):
    def __init__(self, model: Type[Property]):
        super().__init__(model)


crud_property = CRUDProperty(Property)


# CRUD para Feature
class FeatureCreate(BaseModel):
    property_id: uuid_pkg.UUID
    feature_name: str
    feature_value: Optional[str] = None


class FeatureUpdate(BaseModel):
    feature_name: Optional[str] = None
    feature_value: Optional[str] = None


class CRUDFeature(CRUDBase[Feature, FeatureCreate, FeatureUpdate]):
    def __init__(self, model: Type[Feature]):
        super().__init__(model)


crud_feature = CRUDFeature(Feature)


# CRUD para Prediction
class PredictionCreate(BaseModel):
    property_id: uuid_pkg.UUID
    predicted_price: Decimal
    prediction_date: Optional[datetime] = None


class PredictionUpdate(BaseModel):
    predicted_price: Optional[Decimal] = None
    prediction_date: Optional[datetime] = None


class CRUDPrediction(CRUDBase[Prediction, PredictionCreate, PredictionUpdate]):
    def __init__(self, model: Type[Prediction]):
        super().__init__(model)


crud_prediction = CRUDPrediction(Prediction)


# CRUD para MLModel
class MLModelCreate(BaseModel):
    ml_model_tag: str
    ml_model_version: str


class MLModelUpdate(BaseModel):
    ml_model_tag: Optional[str] = None
    ml_model_version: Optional[str] = None


class CRUDMLModel(CRUDBase[MLModel, MLModelCreate, MLModelUpdate]):
    def __init__(self, model: Type[MLModel]):
        super().__init__(model)


crud_ml_model = CRUDMLModel(MLModel)


# CRUD para MLModelPrediction
class MLModelPredictionCreate(BaseModel):
    ml_model_id: uuid_pkg.UUID
    prediction_id: uuid_pkg.UUID


class MLModelPredictionUpdate(BaseModel):
    ml_model_id: Optional[uuid_pkg.UUID] = None
    prediction_id: Optional[uuid_pkg.UUID] = None


class CRUDMLModelPrediction(CRUDBase[MLModelPrediction, MLModelPredictionCreate, MLModelPredictionUpdate]):
    def __init__(self, model: Type[MLModelPrediction]):
        super().__init__(model)


crud_ml_model_prediction = CRUDMLModelPrediction(MLModelPrediction)

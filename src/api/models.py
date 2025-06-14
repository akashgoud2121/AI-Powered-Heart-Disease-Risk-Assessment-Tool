from pydantic import BaseModel

class PredictionRequest(BaseModel):
    age: int
    sex: int
    ChestPainType: int
    RestingBp: float
    Cholesterol: float
    FastingBS: int
    RestingECG: int
    MaxHR: int
    ExerciseAngina: int
    Oldpeak: float
    ST_Slope: int

class PredictionResponse(BaseModel):
    heart_disease_risk: int
    confidence: float = None
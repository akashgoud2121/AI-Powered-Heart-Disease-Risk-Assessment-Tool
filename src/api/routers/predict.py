from fastapi import APIRouter, HTTPException
import numpy as np
import pickle
import os
import logging
from src.api.models import PredictionRequest, PredictionResponse

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Define expected feature names
EXPECTED_FEATURES = [
    'Age', 'RestingBP', 'Cholesterol', 'FastingBS', 'MaxHR', 'Oldpeak', 'Sex_M',
    'ChestPainType_ATA', 'ChestPainType_NAP', 'ChestPainType_TA',
    'RestingECG_Normal', 'RestingECG_ST', 'ExerciseAngina_Y', 'ST_Slope_Flat',
    'ST_Slope_Up'
]

# Model loading with better error handling
def load_model():
    model_path = os.path.join(os.path.dirname(__file__), "../../models/random_forest_model.pkl")
    try:
        with open(model_path, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        logger.error(f"Model file not found at {model_path}")
        raise HTTPException(status_code=500, detail="Model file not found")
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise HTTPException(status_code=500, detail="Error loading model")

# Load model on startup
try:
    model = load_model()
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load model on startup: {str(e)}")
    model = None

@router.post("/predict", response_model=PredictionResponse)
async def predict(data: PredictionRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not available")
    
    try:
        # Initialize features array
        features = np.zeros(len(EXPECTED_FEATURES))
        
        # Map input data to feature array
        features[EXPECTED_FEATURES.index('Age')] = data.age
        features[EXPECTED_FEATURES.index('RestingBP')] = data.RestingBp
        features[EXPECTED_FEATURES.index('Cholesterol')] = data.Cholesterol
        features[EXPECTED_FEATURES.index('FastingBS')] = data.FastingBS
        features[EXPECTED_FEATURES.index('MaxHR')] = data.MaxHR
        features[EXPECTED_FEATURES.index('Oldpeak')] = data.Oldpeak
        features[EXPECTED_FEATURES.index('Sex_M')] = 1 if data.sex == 1 else 0
        features[EXPECTED_FEATURES.index('ExerciseAngina_Y')] = 1 if data.ExerciseAngina == 1 else 0
        
        # Map chest pain type
        if data.ChestPainType == 0:
            features[EXPECTED_FEATURES.index('ChestPainType_TA')] = 1
        elif data.ChestPainType == 1:
            features[EXPECTED_FEATURES.index('ChestPainType_ATA')] = 1
        elif data.ChestPainType == 2:
            features[EXPECTED_FEATURES.index('ChestPainType_NAP')] = 1
            
        # Map ECG results
        if data.RestingECG == 0:
            features[EXPECTED_FEATURES.index('RestingECG_Normal')] = 1
        elif data.RestingECG == 1:
            features[EXPECTED_FEATURES.index('RestingECG_ST')] = 1
            
        # Map ST slope
        if data.ST_Slope == 0:
            features[EXPECTED_FEATURES.index('ST_Slope_Up')] = 1
        elif data.ST_Slope == 1:
            features[EXPECTED_FEATURES.index('ST_Slope_Flat')] = 1
        
        # Make prediction
        prediction = model.predict(features.reshape(1, -1))
        result = int(prediction[0])
        
        return PredictionResponse(heart_disease_risk=result)
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )
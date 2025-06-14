from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routers import predict

app = FastAPI(
    title="Heart Disease Prediction API",
    description="API for predicting heart disease risk",
    version="1.0.0"
)

# Add CORS middleware for Render deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your Streamlit app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict.router)

@app.get("/")
async def root():
    return {"status": "healthy", "message": "Heart Disease Prediction API is running"}
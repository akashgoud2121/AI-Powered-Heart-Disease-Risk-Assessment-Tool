from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routers import predict  # Change back to use full path

app = FastAPI()

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the prediction router
app.include_router(predict.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Heart Disease Prediction API"}
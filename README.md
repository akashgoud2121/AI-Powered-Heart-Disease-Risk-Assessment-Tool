# AI-Powered-Heart-Disease-Risk-Assessment-Tool 🫀

## Overview
An AI-powered web application that predicts heart disease risk using machine learning. Built with Python, this tool provides real-time risk assessment and personalized health recommendations.

## Features
- 🔍 Real-time heart disease risk prediction
- 📊 Analysis of 11 vital health parameters
- 📑 Automated PDF report generation
- 💡 Personalized health recommendations
- 🏥 Medical terminology translations
- 🚨 Emergency resource integration

## Tech Stack
- **Frontend:** Streamlit
- **Backend:** FastAPI
- **ML Model:** Scikit-learn (Random Forest)
- **Documentation:** OpenAPI/Swagger

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/heart-disease-prediction.git
cd heart-disease-prediction
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the FastAPI backend:
```bash
cd src
uvicorn api.main:app --reload
```

2. Launch the Streamlit frontend (in a new terminal):
```bash
cd src/frontend
streamlit run app.py
```

## Project Structure
```
heart-disease-prediction/
│
├── src/
│   ├── api/
│   │   ├── main.py
│   │   └── routers/
│   │       └── predict.py
│   │
│   ├── frontend/
│   │   └── app.py
│   │
│   ├── models/
│   │   └── random_forest_model.pkl
│   │
│   └── utils/
│       └── model_utils.py
│
├── requirements.txt
└── README.md
```

## Usage
1. Enter patient health parameters in the web interface
2. Click "Generate Risk Assessment"
3. View risk assessment results and recommendations
4. Download PDF report if needed

## Input Parameters
- Age
- Sex
- Chest Pain Type
- Resting Blood Pressure
- Cholesterol Level
- Fasting Blood Sugar
- Resting ECG
- Maximum Heart Rate
- Exercise-Induced Angina
- ST Depression
- ST Slope

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Acknowledgments
- Dataset source: https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction
- Medical guidelines and recommendations based on standard healthcare practices

## Contact
E Akash Goud - letsmail.akashgoud@gmail.com
Project Link: https://github.com/akashgoud2121/AI-Powered-Heart-Disease-Risk-Assessment-Tool.git

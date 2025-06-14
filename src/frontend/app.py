import streamlit as st
import requests
from datetime import datetime
from fpdf import FPDF
import base64
import os

API_URL = os.getenv('API_URL', 'http://localhost:8000')

def get_health_recommendations(data, risk_level):
    recommendations = []
    try:
        # Blood Pressure Management
        bp = float(data.get('RestingBp', 0))
        if bp > 140:
            recommendations.append({
                "category": "Blood Pressure Management",
                "tips": [
                    "🧂 Reduce sodium intake (<2,300mg/day)",
                    "🚶‍♂️ Regular moderate exercise",
                    "🧘‍♀️ Practice stress management",
                    "📊 Monitor BP daily"
                ]
            })
        
        # Cholesterol Management
        chol = float(data.get('Cholesterol', 0))
        if chol > 200:
            recommendations.append({
                "category": "Cholesterol Management",
                "tips": [
                    "🥑 Choose heart-healthy fats",
                    "🍎 Increase fiber intake",
                    "🍖 Limit saturated fats",
                    "🏃‍♂️ Exercise 30 minutes daily"
                ]
            })
        
        # Heart Rate Management
        hr = int(data.get('MaxHR', 0))
        if hr > 150:
            recommendations.append({
                "category": "Heart Rate Management",
                "tips": [
                    "❤️ Monitor heart rate during exercise",
                    "🎯 Stay within target heart rate zone",
                    "⚖️ Balance exercise intensity"
                ]
            })
        
        # Risk-based Recommendations
        if risk_level == 1:
            recommendations.append({
                "category": "High Risk Management",
                "tips": [
                    "👨‍⚕️ Consult with a cardiologist",
                    "📊 Regular health monitoring",
                    "💊 Review medications with doctor",
                    "🚨 Know warning signs of heart problems"
                ]
            })
        else:
            recommendations.append({
                "category": "Preventive Care",
                "tips": [
                    "✅ Maintain healthy lifestyle",
                    "📋 Schedule regular check-ups",
                    "💚 Continue heart-healthy habits"
                ]
            })
            
    except Exception as e:
        st.error(f"Error generating recommendations: {str(e)}")
        recommendations.append({
            "category": "General Health",
            "tips": [
                "👨‍⚕️ Please consult a healthcare provider",
                "💪 Maintain a healthy lifestyle",
                "📅 Regular check-ups recommended"
            ]
        })
    
    return recommendations

def create_report_pdf(data, risk_level):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    
    # Title
    pdf.cell(0, 10, 'Heart Disease Risk Assessment Report', ln=True, align='C')
    pdf.line(10, 30, 200, 30)
    
    # Date and Risk Level
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Date: {datetime.now().strftime("%Y-%m-%d %H:%M")}', ln=True)
    pdf.cell(0, 10, f'Risk Level: {"High" if risk_level else "Low"}', ln=True)
    
    # Patient Data
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Patient Information:', ln=True)
    pdf.set_font('Arial', '', 12)
    
    metrics = [
        ('Age', data['age']),
        ('Sex', 'Male' if data['sex'] == 1 else 'Female'),
        ('Blood Pressure', f"{data['RestingBp']} mmHg"),
        ('Cholesterol', f"{data['Cholesterol']} mg/dl"),
        ('Max Heart Rate', data['MaxHR']),
        ('ST Depression', data['Oldpeak'])
    ]
    
    for label, value in metrics:
        pdf.cell(0, 10, f'{label}: {value}', ln=True)
    
    return pdf.output(dest='S').encode('latin-1')

def init_session_state():
    if 'assessment_history' not in st.session_state:
        st.session_state.assessment_history = []

init_session_state()

# Set page config
st.set_page_config(page_title="Heart Disease Prediction", page_icon="❤️", layout="wide", initial_sidebar_state="expanded")

# Add custom CSS with centered content and reduced spacing
st.markdown("""
    <style>
    /* Center align the main content */
    .main {
        padding: 0 !important;
        margin: 0 auto !important;
    }
    
    /* Center the title and remove extra spacing */
    h1 {
        text-align: center !important;
        margin: 0 !important;
        padding: 0.5rem !important;
    }
    
    /* Style the button */
    .stButton>button { 
        width: 100%; 
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
    }
    
    /* Custom info box */
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    
    /* Remove default padding from containers */
    .element-container {
        margin: 0 !important;
        padding: 0.25rem 0 !important;
    }
    
    /* Center align description text */
    .css-1p05t8e {
        text-align: center;
    }
    
    /* Adjust stMarkdown elements */
    .stMarkdown {
        margin-top: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# App Header with centered alignment and reduced spacing
st.markdown("<h1>❤️ Heart Disease Risk Assessment Tool</h1>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; padding: 0.5rem;'>
    This tool helps assess the risk of heart disease based on various health parameters.<br>
    Please fill in all the fields below with your medical information.
    </div>
    """, unsafe_allow_html=True)

# Information for first-time users
st.info("""
### ℹ️ New to Heart Health Terms?
Check the sidebar for simple explanations of medical terms. Each input field also has a help tooltip - 
hover over the ❔ icon next to each field to learn more.

**Quick Tips:**
- Fill in the values you know from your latest medical checkup
- Ask your healthcare provider if you're unsure about any values
- Use the example profiles in the sidebar as reference
""")

# Sidebar - Risk Factors Information
st.sidebar.markdown("""

### 📚 Understanding Medical Terms

#### Basic Terms Explained:
1. **Blood Pressure (BP)**
   - What: Force of blood against artery walls
   - Normal: Below 120/80 mmHg
   - High: Above 140/90 mmHg

2. **Cholesterol**
   - What: Fat-like substance in blood
   - Normal: Below 200 mg/dl
   - High: Above 240 mg/dl

3. **Fasting Blood Sugar**
   - What: Blood sugar level after not eating for 8 hours
   - Normal: Below 120 mg/dl
   - High: Above 120 mg/dl

4. **Types of Chest Pain**
   - Typical Angina: Pain triggered by exercise, relieved by rest
   - Atypical Angina: Similar but less predictable
   - Non-anginal Pain: Not heart-related
   - Asymptomatic: No pain

5. **ECG (Electrocardiogram)**
   - What: Measures heart's electrical activity
   - Normal: Regular pattern
   - ST-T Wave Abnormality: Shows possible reduced blood flow
   - Left Ventricular Hypertrophy: Enlarged heart muscle

6. **Exercise Test Terms**
   - ST Depression: Shows how heart responds to exercise
   - ST Slope: Pattern of heart activity during exercise
     * Upsloping: Usually normal
     * Flat or Downsloping: May indicate problems

---

### 📊 Risk Profile Examples

#### Examples of Risk Profiles:

##### 🔴 High Risk Profile Example:
**Personal Information:**
- Age: 49 years
- Sex: Female
- Resting BP: 160 mmHg (High)

**Clinical Measurements:**
- Cholesterol: 180 mg/dl
- Fasting Blood Sugar: Normal
- Max Heart Rate: 156 bpm

**Cardiac Assessment:**
- Chest Pain Type: Non-anginal Pain
- Resting ECG: Normal
- Exercise-Induced Angina: No

**Exercise Test Results:**
- ST Depression (Oldpeak): 1.0
- ST Slope: Flat
---
##### 🟢 Low Risk Profile Example:
**Personal Information:**
- Age: 40 years
- Sex: Male
- Resting BP: 80 mmHg (Normal)

**Clinical Measurements:**
- Cholesterol: 100 mg/dl
- Fasting Blood Sugar: Normal
- Max Heart Rate: 60 bpm

**Cardiac Assessment:**
- Chest Pain Type: Typical Angina
- Resting ECG: Normal
- Exercise-Induced Angina: No

**Exercise Test Results:**
- ST Depression (Oldpeak): 0.0
- ST Slope: Upsloping

#### Key Risk Indicators:
- Higher resting blood pressure (>140 mmHg)
- Higher age (>45 years)
- Presence of exercise-induced angina
- Abnormal ST depression and slope
- Non-typical chest pain patterns
""")

# Create three columns for better organization
col1, col2, col3 = st.columns(3)

# Personal Information Section
with col1:
    st.markdown("### 📋 Personal Information")
    st.info("Basic demographic and physical measurements")
    age = st.number_input("Age (years)", 
                         min_value=20, 
                         max_value=120, 
                         value=40,
                         help="Patient's age in years")
    sex = st.selectbox("Biological Sex",
                      options=["Male", "Female"],
                      help="Patient's biological sex at birth")
    resting_bp = st.number_input("Resting Blood Pressure (mm Hg)", 
                                min_value=80, 
                                max_value=200,
                                help="Blood pressure measured while patient is at rest")

# Clinical Measurements Section
with col2:
    st.markdown("### 🔬 Clinical Measurements")
    st.info("Laboratory and diagnostic test results")
    cholesterol = st.number_input("Cholesterol Level (mg/dl)", 
                                 min_value=100, 
                                 max_value=600,
                                 help="Total cholesterol level in blood")
    fasting_bs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", 
                             options=["No (≤120 mg/dl)", "Yes (>120 mg/dl)"],
                             help="Blood sugar measurement after overnight fasting")
    max_hr = st.number_input("Maximum Heart Rate", 
                            min_value=60, 
                            max_value=220,
                            help="Maximum heart rate achieved during exercise")

# Cardiac Specific Section
with col3:
    st.markdown("### 💗 Cardiac Assessment")
    st.info("Heart-specific diagnostic information")
    chest_pain_type = st.selectbox("Type of Chest Pain", 
        options=["Typical Angina", "Atypical Angina", "Non-anginal Pain", "Asymptomatic"],
        help="Classification of chest pain experienced by patient")
    
    resting_ecg = st.selectbox("Resting ECG Results", 
        options=["Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"],
        help="ECG results when patient is at rest")
    
    exercise_angina = st.selectbox("Exercise-Induced Angina", 
        options=["No", "Yes"],
        help="Presence of chest pain during exercise")

# Exercise Test Results
st.markdown("### 📊 Exercise Test Results")
col4, col5 = st.columns(2)

with col4:
    oldpeak = st.number_input("ST Depression (Oldpeak)", 
                             min_value=0.0, 
                             max_value=6.0, 
                             step=0.1,
                             help="ST depression induced by exercise relative to rest")

with col5:
    st_slope = st.selectbox("ST Slope", 
        options=["Upsloping", "Flat", "Downsloping"],
        help="Slope of peak exercise ST segment")

# Add a divider
st.divider()

# Prediction Button
if st.button("📋 Generate Risk Assessment"):
    try:
        # Data validation
        if not all([age, resting_bp, cholesterol, max_hr]):
            st.error("❌ Please fill in all required fields.")
            st.stop()

        # Prepare input data matching predict.py PredictionRequest structure
        input_data = {
            "age": age,
            "sex": 1 if sex == "Male" else 0,
            "ChestPainType": {
                "Typical Angina": 0,
                "Atypical Angina": 1,
                "Non-anginal Pain": 2,
                "Asymptomatic": 3
            }[chest_pain_type],
            "RestingBp": float(resting_bp),
            "Cholesterol": float(cholesterol),
            "FastingBS": 1 if fasting_bs == "Yes (>120 mg/dl)" else 0,
            "RestingECG": {
                "Normal": 0,
                "ST-T Wave Abnormality": 1,
                "Left Ventricular Hypertrophy": 2
            }[resting_ecg],
            "MaxHR": max_hr,
            "ExerciseAngina": 1 if exercise_angina == "Yes" else 0,
            "Oldpeak": float(oldpeak),
            "ST_Slope": {
                "Upsloping": 0,
                "Flat": 1,
                "Downsloping": 2
            }[st_slope]
        }

        with st.spinner('🔄 Analyzing patient data...'):
            response = requests.post(f"{API_URL}/predict", json=input_data)
            
        if response.status_code == 200:
            prediction = response.json()
            risk_level = prediction['heart_disease_risk']
            
            # Clear visual separation
            st.markdown("---")
            
            # Display Risk Assessment Result
            st.markdown("### 📊 Risk Assessment Result")
            if risk_level == 1:
                st.error("""
                    ### ⚠️ High Risk of Heart Disease Detected
                    
                    The analysis indicates potential risk factors for heart disease. 
                    Key points to consider:
                    - Immediate consultation with a healthcare provider is recommended
                    - Regular monitoring of vital signs
                    - Follow the recommendations below
                """)
            else:
                st.success("""
                    ### ✅ Low Risk of Heart Disease
                    
                    The analysis suggests lower risk factors for heart disease. 
                    Key points to consider:
                    - Continue maintaining a healthy lifestyle
                    - Regular check-ups are still important
                    - Follow the preventive recommendations below
                """)
            
            # Get and display recommendations
            recommendations = get_health_recommendations(input_data, risk_level)
            st.markdown("### 🎯 Personalized Health Recommendations")
            for rec in recommendations:
                with st.expander(f"📌 {rec['category']}", expanded=True):
                    for tip in rec['tips']:
                        st.markdown(f"- {tip}")

            # Generate PDF report
            pdf = create_report_pdf(input_data, risk_level)
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf,
                file_name=f"heart_assessment_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf"
            )
            
        else:
            st.error(f"Error: Unable to process the assessment (Status code: {response.status_code})")
            
    except requests.exceptions.ConnectionError:
        st.error("Unable to connect to the prediction service. Please check if the server is running.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

# Disclaimer
st.markdown("---")
st.warning("""
    **Medical Disclaimer**: This tool provides a preliminary risk assessment only. 
    It should not be used as a substitute for professional medical advice, diagnosis, or treatment. 
    Always seek the advice of your physician or other qualified health provider with any questions 
    you may have regarding a medical condition.
""")
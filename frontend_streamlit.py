import streamlit as st
import requests
import json

st.set_page_config(
    page_title="Heart Disease Prediction",
    page_icon="❤️",
    layout="wide"
)

st.title("❤️ Heart Disease Prediction System")
st.markdown("---")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=Montserrat:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Montserrat', sans-serif;
    }
    
    .stButton > button {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

API_URL = "http://127.0.0.1:8000/predict"

col1, col2 = st.columns([2, 1])

with col1:
    st.header("Patient Information")
    
    with st.form(key="patient_form"):
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            age = st.number_input(
                "Age",
                min_value=0,
                max_value=120,
                value=50,
                help="Patient age in years"
            )
        with col_b:
            sex = st.selectbox(
                "Sex",
                options=[0, 1],
                format_func=lambda x: "Female" if x == 0 else "Male",
                help="Patient sex"
            )
        with col_c:
            chest_pain = st.selectbox(
                "Chest Pain Type",
                options=[0, 1, 2, 3, 4],
                index=2,
                help="Type of chest pain (0-4)"
            )
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            cholesterol = st.number_input(
                "Cholesterol (mg/dl)",
                min_value=0,
                max_value=400,
                value=200,
                help="Serum cholesterol level"
            )
        with col_b:
            ekg = st.selectbox(
                "EKG Results",
                options=[0, 1, 2],
                index=0,
                help="EKG test results"
            )
        with col_c:
            max_hr = st.number_input(
                "Max Heart Rate",
                min_value=0,
                max_value=250,
                value=150,
                help="Maximum heart rate achieved"
            )
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            exercise_angina = st.selectbox(
                "Exercise Induced Angina",
                options=[0, 1],
                format_func=lambda x: "No" if x == 0 else "Yes",
                index=0,
                help="Does patient experience angina with exercise?"
            )
        with col_b:
            st_depression = st.number_input(
                "ST Depression",
                min_value=0.0,
                max_value=10.0,
                value=0.0,
                step=0.1,
                help="ST depression induced by exercise"
            )
        with col_c:
            slope_st = st.selectbox(
                "Slope of ST Segment",
                options=[0, 1, 2, 3],
                index=1,
                help="Slope of ST segment"
            )
        
        col_a, col_b = st.columns(2)
        with col_a:
            num_vessels = st.selectbox(
                "Number of Major Vessels",
                options=[0, 1, 2, 3],
                index=0,
                help="Number of major vessels with fluoroscopy"
            )
        with col_b:
            thallium = st.selectbox(
                "Thallium Test Result",
                options=[0, 1, 2, 3, 4, 5, 6, 7],
                index=3,
                help="Thallium stress test result"
            )
        
        submit_button = st.form_submit_button(
            label="🔍 Predict",
            use_container_width=True,
            type="primary"
        )

with col2:
    st.header("Information")
    st.info("""
    ### Feature Ranges:
    - **Age**: 0-120 years
    - **Sex**: 0 (F), 1 (M)
    - **Chest Pain**: 0-4
    - **Cholesterol**: 0-400 mg/dl
    - **EKG**: 0-2
    - **Max HR**: 0-250 bpm
    - **Angina**: 0 (No), 1 (Yes)
    - **ST Dep**: 0-10
    - **Slope**: 0-3
    - **Vessels**: 0-3
    - **Thallium**: 0-7
    """)

if submit_button:
    st.markdown("---")
    
    with st.spinner("🔄 Making prediction..."):
        try:
            payload = {
                "age": age,
                "sex": sex,
                "chest_pain_type": chest_pain,
                "cholesterol": cholesterol,
                "ekg_results": ekg,
                "max_hr": max_hr,
                "exercise_angina": exercise_angina,
                "st_depression": st_depression,
                "slope_of_st": slope_st,
                "number_of_vessels_fluro": num_vessels,
                "thallium": thallium
            }
            
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                
                st.header("Prediction Results")
                
                col_res1, col_res2 = st.columns(2)
                
                with col_res1:
                    if result["prediction"] == 1:
                        st.markdown(f"<h2 style='color: #ff6b6b; text-align: center;'>⚠️ {result['result_text']}</h2>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<h2 style='color: #51cf66; text-align: center;'>✓ {result['result_text']}</h2>", unsafe_allow_html=True)
                
                with col_res2:
                    st.metric(
                        label="Confidence Score",
                        value=f"{result['confidence_score']:.4f}"
                    )
                
                st.markdown("---")
                st.subheader("Patient Summary")
                summary_data = {
                    "Age": f"{age} years",
                    "Sex": "Male" if sex == 1 else "Female",
                    "Cholesterol": f"{cholesterol} mg/dl",
                    "Max Heart Rate": f"{max_hr} bpm",
                    "Exercise Angina": "Yes" if exercise_angina == 1 else "No",
                    "Prediction": "Heart Disease Present" if result["prediction"] == 1 else "No Heart Disease",
                    "Confidence": f"{result['confidence_score']:.4f}"
                }
                
                for key, value in summary_data.items():
                    st.write(f"**{key}**: {value}")
                
                st.warning("⚠️ **Disclaimer**: This is a machine learning prediction and should NOT be used as a substitute for professional medical diagnosis. Please consult a qualified healthcare provider.")
            
            else:
                st.error(f"API Error: {response.status_code}")
                st.write(response.text)
        
        except requests.exceptions.ConnectionError:
            st.error("❌ Connection Error: Cannot reach the API backend. Make sure it's running on http://127.0.0.1:8000")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

st.markdown("---")
st.markdown("""
### How to use:
1. Fill in the patient information in the form
2. Click the **Predict** button
3. The system will send the data to the backend API
4. Results will be displayed with a confidence score

**Made with ❤️ for educational purposes only. - By Asifur Rahaman**
""")

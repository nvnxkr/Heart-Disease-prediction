import streamlit as st
import pandas as pd
import joblib

# ----------------------------
# Load your trained model
# ----------------------------
model = joblib.load("logistic_regression.pkl")
scaler = joblib.load("scalar.pkl")
expected_columns = joblib.load("columns.pkl")

# ----------------------------
# Page Config & Styling
# ----------------------------
st.set_page_config(page_title="❤️ Heart Disease Prediction", layout="centered", page_icon="❤️")

# Add custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #f5f7fa;
    }
    .main {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-size: 18px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #ff1c1c;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# Sidebar Info
# ----------------------------
st.sidebar.title("ℹ️ About ")
st.sidebar.info(
    """
    This app predicts the **likelihood of Heart Disease**  
    based on your health parameters.  

    👉 Fill in the details carefully.  
    👉 Click **Predict** to get results.  
    🟢 **Model:** ***Logistic Regression with 'accuracy': 0.8641, 'f1 score': 0.8792***
     
    """
)

# ----------------------------
# Title
# ----------------------------
st.title("❤️ Heart Disease Prediction ")
st.markdown("Check your **heart health risk** by filling the details below.")
st.write("---")

# ----------------------------
# UI Inputs
# ----------------------------
col1, col2 = st.columns(2)

with col1:
    age = st.slider("📅 Age", 18, 100, 40)
    sex = st.selectbox("⚧ Sex", ["Male", "Female"])
    chest_pain = st.selectbox(
        "💔 Chest Pain Type",
        ["Typical Angina", "Atypical Angina", "Non-anginal Pain", "Asymptomatic"]
    )
    resting_bp = st.number_input("🩸 Resting Blood Pressure (mm Hg)", 80, 200, 120)
    cholesterol = st.number_input("🥓 Cholesterol (mg/dl)", 100, 600, 200)
    fasting_bs = st.selectbox("🍬 Fasting Blood Sugar > 120 mg/dl", ["Yes", "No"])

with col2:
    resting_ecg = st.selectbox(
        "🫀 Resting ECG",
        ["Normal", "ST-T Abnormality", "Left Ventricular Hypertrophy"]
    )
    max_hr = st.slider("🏃 Max Heart Rate Achieved", 60, 220, 150)
    exercise_angina = st.selectbox("⚡ Exercise Induced Angina", ["Yes", "No"])
    oldpeak = st.number_input("📉 Oldpeak (ST depression by exercise)", -2.0, 7.0, 1.0, step=0.1)
    st_slope = st.selectbox("📈 ST Slope", ["Upsloping", "Flat", "Downsloping"])

st.write("---")

# ----------------------------
# Encoding same as training
# ----------------------------
sex_map = {"Male": 1, "Female": 0}
cp_map = {
    "Typical Angina": 0,
    "Atypical Angina": 1,
    "Non-anginal Pain": 2,
    "Asymptomatic": 3
}
fbs_map = {"Yes": 1, "No": 0}
restecg_map = {
    "Normal": 0,
    "ST-T Abnormality": 1,
    "Left Ventricular Hypertrophy": 2
}
exang_map = {"Yes": 1, "No": 0}
slope_map = {"Upsloping": 0, "Flat": 1, "Downsloping": 2}

# ----------------------------
# Prediction
# ----------------------------
if st.button("🔍 Predict"):

    input_df = pd.DataFrame([{
        "Age": age,
        "Sex": sex,
        "ChestPainType": chest_pain,
        "RestingBP": resting_bp,
        "Cholesterol": cholesterol,
        "FastingBS": fasting_bs,
        "RestingECG": resting_ecg,
        "MaxHR": max_hr,
        "ExerciseAngina": exercise_angina,
        "Oldpeak": oldpeak,
        "ST_Slope": st_slope
    }])

    # ✅ Apply categorical mappings
    input_df["Sex"] = input_df["Sex"].map(sex_map)
    input_df["ChestPainType"] = input_df["ChestPainType"].map(cp_map)
    input_df["FastingBS"] = input_df["FastingBS"].map(fbs_map)
    input_df["RestingECG"] = input_df["RestingECG"].map(restecg_map)
    input_df["ExerciseAngina"] = input_df["ExerciseAngina"].map(exang_map)
    input_df["ST_Slope"] = input_df["ST_Slope"].map(slope_map)

    # Ensure all expected columns
    for col in expected_columns:
        if col not in input_df.columns:
            input_df[col] = 0

    # Reorder
    input_df = input_df[expected_columns]

    # Scale
    scaled_input = scaler.transform(input_df)

    # Predict
    prediction = model.predict(scaled_input)[0]
    probability = model.predict_proba(scaled_input)[0][1]

    st.write("---")
    st.subheader("📊 Prediction Result")
    if prediction == 1:
        st.error(f"⚠️ **High risk of Heart Disease**\n\n🔴 Probability: **{probability:.2f}**" )
    else:
        st.success(f"✅ **Low risk of Heart Disease**\n\n🟢 Probability: **{probability:.2f}**")

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import joblib
import os
import time

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Radioactive Water Element Detector", layout="wide")

# ================= CUSTOM CSS =================
css_block = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');

* { font-family: 'Bebas Neue', sans-serif !important; }
html, body, [class*="css"] { background-color: #0a0a0a; color: #e8f5e9; min-height:100vh; }
h1.app-title { text-align:center; color:#FFD300; font-size:52px; margin-bottom:4px; text-shadow:0 0 10px #FFD300,0 0 28px #FF7518;}
p.app-sub { text-align:center; color:#39FF14; margin-top:0; font-size:20px; text-shadow:0 0 10px #39FF14; }
</style>
"""
st.markdown(css_block, unsafe_allow_html=True)

# ================= LOAD AI MODEL =================
MODEL_PATH = "models/element_detector.pkl"
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None

# ================= UI =================
st.markdown("<h1 class='app-title'>💧☢️ Radioactive Water Element Detector</h1>", unsafe_allow_html=True)
st.markdown("<p class='app-sub'>AI-Powered Detection | Developed by Karthikeyan</p>", unsafe_allow_html=True)

st.subheader("🔍 Enter Water Parameters")

ph = st.number_input("pH Level", 0.0, 14.0, 7.0)
tds = st.number_input("TDS (mg/L)", 0.0, 2000.0, 300.0)
hardness = st.number_input("Hardness (mg/L)", 0.0, 1000.0, 150.0)
nitrate = st.number_input("Nitrate (mg/L)", 0.0, 500.0, 20.0)
location = st.text_input("📍 Location")

if st.button("Run Analysis"):
    if model is None:
        st.error("❌ AI model not found! Please run train_model.py first.")
    else:
        # Predict element
        X_input = pd.DataFrame([[ph, tds, hardness, nitrate]], columns=["pH", "TDS", "Hardness", "Nitrate"])
        element = model.predict(X_input)[0]

        # Display Result
        st.markdown(f"<h2 style='color:#FFD300;'>⚠️ Detected Element: {element}</h2>", unsafe_allow_html=True)

        # ----------------- Animated Risk Gauge -----------------
        # Simple risk estimation (based on deviation from safe ranges)
        score = 0
        if ph < 6.5 or ph > 8.5: score += 25
        if tds > 500: score += 25
        if hardness > 200: score += 25
        if nitrate > 45: score += 25

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            title={'text': "Risk Level %"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "red" if score >= 60 else "orange" if score >= 30 else "#39FF14"},
                'steps': [
                    {'range': [0, 30], 'color': "#39FF14"},
                    {'range': [30, 60], 'color': "yellow"},
                    {'range': [60, 100], 'color': "red"}
                ],
            }
        ))
        st.plotly_chart(fig, use_container_width=True)

        # ----------------- Save Dataset -----------------
        new_data = pd.DataFrame([[location, ph, tds, hardness, nitrate, element]],
                                columns=["Location", "pH", "TDS", "Hardness", "Nitrate", "Element"])
        if os.path.exists("water_data.csv"):
            old_data = pd.read_csv("water_data.csv")
            df = pd.concat([old_data, new_data], ignore_index=True)
        else:
            df = new_data
        df.to_csv("water_data.csv", index=False)
        st.success("Data saved successfully ✅")
        st.download_button("📥 Download Dataset", data=df.to_csv(index=False),
                           file_name="water_data.csv", mime="text/csv")

# ================= Info Section =================
st.subheader("⚠️ Why this matters")
st.markdown("""
- Radioactive elements like **Uranium, Cesium, Radium** in water can cause serious health risks.
- AI helps quickly detect which element is present based on water chemistry.
- Stay informed and ensure safe drinking water.
""")


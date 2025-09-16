import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import joblib
import os
import time

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Radioactive Water Detector", layout="wide")

# ================= CUSTOM CSS =================
css_block = """
<style>
* { font-family: 'Arial', sans-serif !important; }
h1.app-title { text-align:center; color:#FFD300; font-size:48px; }
p.app-sub { text-align:center; color:#39FF14; font-size:18px; }
</style>
"""
st.markdown(css_block, unsafe_allow_html=True)

# ================= LOAD AI MODEL =================
MODEL_PATH = "models/element_detector.pkl"
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None
    st.error("❌ AI model not found! Please run train_model.py first.")

# ================= FUNCTIONS =================
def predict_element(ph, tds, hardness, nitrate):
    if model:
        features = pd.DataFrame([[ph, tds, hardness, nitrate]],
                                columns=["pH", "TDS", "Hardness", "Nitrate"])
        prediction = model.predict(features)[0]
        return prediction
    else:
        return "Model not available"

def calculate_risk(ph, tds, hardness, nitrate):
    score = 0
    if ph < 6.5 or ph > 8.5: score += 30
    if tds > 500: score += 25
    if hardness > 300: score += 20
    if nitrate > 45: score += 25
    return score

# ================= UI =================
st.markdown("<h1 class='app-title'>💧☢️ Radioactive Water Contamination Detector</h1>", unsafe_allow_html=True)
st.markdown("<p class='app-sub'>AI/ML Powered Water Safety | Developed by Karthikeyan</p>", unsafe_allow_html=True)

tabs = st.tabs(["🔬 Contamination Check", "📊 Safety Meter", "⚠️ Radioactive Awareness"])

# ---- TAB 1: Contamination Check ----
with tabs[0]:
    st.subheader("🔍 Enter Water Parameters")
    ph = st.number_input("pH Level", 0.0, 14.0, 7.0)
    tds = st.number_input("TDS (mg/L)", 0.0, 2000.0, 300.0)
    hardness = st.number_input("Hardness (mg/L)", 0.0, 1000.0, 150.0)
    nitrate = st.number_input("Nitrate (mg/L)", 0.0, 500.0, 20.0)
    location = st.text_input("📍 Location")

    if st.button("Run Analysis"):
        element = predict_element(ph, tds, hardness, nitrate)
        score = calculate_risk(ph, tds, hardness, nitrate)

        # Result message
        result_msg = f"Detected Element: {element}\nRisk Score: {score}%"
        st.markdown(f"<p style='font-size:20px; color:#FFD300;'>{result_msg}</p>", unsafe_allow_html=True)

        # Animated gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            title={'text': "Radioactive Risk %"},
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

# ---- TAB 2: Safety Meter ----
with tabs[1]:
    st.subheader("📊 Safe vs Unsafe Water Levels (Mini Dashboard)")
    safe_ranges = {
        "pH": (6.5, 8.5, ph),
        "TDS (mg/L)": (0, 500, tds),
        "Hardness (mg/L)": (0, 300, hardness),
        "Nitrate (mg/L)": (0, 45, nitrate)
    }

    params = list(safe_ranges.items())
    for i in range(0, len(params), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j >= len(params): break
            param, (low, high, value) = params[i + j]
            with col:
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=[param],
                    y=[value],
                    marker_color="red" if value < low or value > high else "#39FF14"
                ))
                fig.add_shape(type="rect", x0=-0.5, x1=0.5, y0=low, y1=high, fillcolor="rgba(57,255,20,0.2)", line_width=0)
                fig.update_layout(height=180, width=180, margin=dict(l=10,r=10,t=30,b=10))
                st.plotly_chart(fig, use_container_width=False)
                status = "✅ Safe" if low <= value <= high else "⚠️ Unsafe"
                color = "#39FF14" if low <= value <= high else "red"
                st.markdown(f"<div style='font-size:16px; color:{color};'><b>{status}</b></div>", unsafe_allow_html=True)

# ---- TAB 3: Radioactive Awareness ----
with tabs[2]:
    st.subheader("⚠️ Dangers of Radioactive Water")
    st.image("radioactive_process.png", caption="Radioactive Contamination Process", use_container_width=True)
    st.info("ℹ️ Stay informed and take action to ensure safe drinking water.")

# Connect Section
st.markdown("""
<div style="text-align:center; margin-top:10px;">
    <p style="color:#FFD300; font-size:16px;">
        Connect with me: 
        <a href="https://www.linkedin.com/in/karthikeyan-t-82a86931a" target="_blank" style="color:#00FF7F;">LinkedIn</a> | 
        <a href="mailto:karthikeyant1885@gmail.com" style="color:#00FF7F;">Email</a>
    </p>
</div>
""", unsafe_allow_html=True)

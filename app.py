import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import joblib
import time
import os

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Radioactive Water Contamination Detector", layout="wide")

# ================= CUSTOM CSS =================
css_block = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');
* { font-family: 'Bebas Neue', sans-serif !important; }
html, body, [class*="css"] { background-color: #0a0a0a; color: #e8f5e9; min-height: 100vh; }
h1.app-title { text-align: center; color: #FFD300; font-size: 52px; text-shadow: 0 0 10px #FFD300, 0 0 28px #FF7518; }
p.app-sub { text-align: center; color: #39FF14; font-size: 20px; text-shadow: 0 0 10px #39FF14; }
.stTabs [role="tablist"] button { background: #101010 !important; color: #39FF14 !important; border-radius: 12px !important; border: 1px solid rgba(57,255,20,0.3) !important; margin-right: 6px !important; padding: 8px 14px !important; font-size: 16px !important; transition: all .18s ease; }
.stTabs [role="tablist"] button:hover { background: #39FF14 !important; color: black !important; transform: translateY(-2px) scale(1.03); box-shadow: 0 0 18px rgba(57,255,20,0.15); }
.stTabs [role="tablist"] button[aria-selected="true"] { background: linear-gradient(90deg, #FFD300, #FF7518) !important; color: black !important; border: 1px solid #FFD300 !important; box-shadow: 0 0 26px rgba(255,211,0,0.35); }
</style>
"""
st.markdown(css_block, unsafe_allow_html=True)

# ================= Load AI Model =================
model_path = "models/element_model.pkl"
if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    st.error("❌ AI model not found! Please run train_model.py first.")
    st.stop()

# ================= UI =================
st.markdown("<h1 class='app-title'>💧☢️ Radioactive Water Contamination Detector</h1>", unsafe_allow_html=True)
st.markdown("<p class='app-sub'>AI/ML Powered Water Safety | Developed by Karthikeyan</p>", unsafe_allow_html=True)

tabs = st.tabs(["🔬 Contamination Check", "📊 Safety Meter", "⚠️ Radioactive Awareness"])

# ---- TAB 1 ----
with tabs[0]:
    st.subheader("🔍 Enter Water Parameters")

    ph = st.number_input("pH Level", 0.0, 14.0, 7.0)
    tds = st.number_input("TDS (mg/L)", 0.0, 2000.0, 300.0)
    hardness = st.number_input("Hardness (mg/L)", 0.0, 1000.0, 150.0)
    nitrate = st.number_input("Nitrate (mg/L)", 0.0, 500.0, 20.0)
    conductivity = st.number_input("Conductivity (µS/cm)", 0.0, 2000.0, 500.0)
    location = st.text_input("📍 Location")

    if st.button("Run Analysis"):
        # AI Prediction
        input_df = pd.DataFrame([[ph, tds, hardness, nitrate, conductivity]], 
                                columns=["pH","TDS","Hardness","Nitrate","Conductivity"])
        element_pred = model.predict(input_df)[0]

        # Contamination Score
        score = 0
        if ph < 6.5 or ph > 8.5: score += 30
        if tds > 500: score += 25
        if hardness > 200: score += 20
        if nitrate > 45: score += 25

        if score < 30:
            risk_text = '✅ Safe: No significant radioactive contamination detected.'
        elif score < 60:
            risk_text = '⚠️ Moderate Risk: Some radioactive traces possible.'
        else:
            risk_text = '☢️ High Risk: Potential radioactive contamination detected!'

        st.markdown(f"<p style='font-size:20px; color:#FFD300;'>{risk_text}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:20px; color:#39FF14;'>Detected Element: <b>{element_pred}</b></p>", unsafe_allow_html=True)

        # Gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            title={'text': "Radioactive Risk %"},
            gauge={'axis': {'range': [0, 100]},
                   'bar': {'color': "red" if score >= 60 else "orange" if score >= 30 else "#39FF14"},
                   'steps': [
                       {'range': [0,30],'color':'#39FF14'},
                       {'range':[30,60],'color':'yellow'},
                       {'range':[60,100],'color':'red'}]
                  }
        ))
        st.plotly_chart(fig, use_container_width=True)

# ---- TAB 2 ----
with tabs[1]:
    st.subheader("📊 Safe vs Unsafe Water Levels")
    safe_ranges = {"pH": (6.5,8.5,ph),"TDS":(0,500,tds),"Hardness":(0,200,hardness),"Nitrate":(0,45,nitrate),"Conductivity":(0,1000,conductivity)}
    for param,(low,high,value) in safe_ranges.items():
        color = "#39FF14" if low<=value<=high else "red"
        st.markdown(f"<b>{param}</b>: {value} (Safe: {low}-{high}) ✅" if low<=value<=high else f"<b>{param}</b>: {value} (Safe: {low}-{high}) ⚠️", unsafe_allow_html=True)

# ---- TAB 3 ----
with tabs[2]:
    st.subheader("⚠️ Dangers of Radioactive Water")
    st.image("radioactive_process.png", caption="Radioactive Contamination Process", use_container_width=True)
    st.info("ℹ️ Stay informed and take action to ensure safe drinking water.")

# Footer
st.markdown("""
<div style="text-align:center; margin-top:10px;">
<p style="color:#FFD300; font-size:16px;">
Connect with me: 
<a href="https://www.linkedin.com/in/karthikeyan-t-82a86931a" target="_blank" style="color:#00FF7F;">LinkedIn</a> | 
<a href="mailto:karthikeyant1885@gmail.com" style="color:#00FF7F;">Email</a>
</p></div>
""", unsafe_allow_html=True)

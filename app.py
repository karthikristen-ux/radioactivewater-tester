import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
import joblib
import time

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Radioactive Water Element Predictor", layout="wide")

# ================= CUSTOM CSS =================
css_block = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');
* { font-family: 'Bebas Neue', sans-serif !important; }
html, body, [class*="css"] { background-color: #0a0a0a; color: #e8f5e9; min-height: 100vh; }
h1.app-title { text-align: center; color: #FFD300; font-size: 52px; margin-bottom: 4px; text-shadow: 0 0 10px #FFD300, 0 0 28px #FF7518; }
p.app-sub { text-align: center; color: #39FF14; margin-top: 0; font-size: 20px; text-shadow: 0 0 10px #39FF14; }
.stTabs [role="tablist"] button { background: #101010 !important; color: #39FF14 !important; border-radius: 12px !important; border: 1px solid rgba(57,255,20,0.3) !important; margin-right: 6px !important; padding: 8px 14px !important; font-size: 16px !important; transition: all .18s ease; }
.stTabs [role="tablist"] button:hover { background: #39FF14 !important; color: black !important; transform: translateY(-2px) scale(1.03); box-shadow: 0 0 18px rgba(57,255,20,0.15); }
.stTabs [role="tablist"] button[aria-selected="true"] { background: linear-gradient(90deg, #FFD300, #FF7518) !important; color: black !important; border: 1px solid #FFD300 !important; box-shadow: 0 0 26px rgba(255,211,0,0.35); }
</style>
"""
st.markdown(css_block, unsafe_allow_html=True)

# ================= LOAD REGRESSION MODEL =================
MODEL_PATH = "models/element_predictor.pkl"
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    st.error("❌ AI model not found! Please run train_model.py first.")
    st.stop()

# ================= UI =================
st.markdown("<h1 class='app-title'>💧☢️ Radioactive Water Element Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p class='app-sub'>Predict exact element concentrations using AI | Developed by Karthikeyan</p>", unsafe_allow_html=True)

tabs = st.tabs(["🔬 Check Water", "📊 Safety Meter", "⚠️ Radioactive Awareness"])

# ---- TAB 1: Water Check ----
with tabs[0]:
    st.subheader("🔍 Enter Water Parameters")

    ph = st.number_input("pH Level", 0.0, 14.0, 7.0)
    tds = st.number_input("TDS (mg/L)", 0.0, 2000.0, 300.0)
    hardness = st.number_input("Hardness (mg/L)", 0.0, 1000.0, 150.0)
    location = st.text_input("📍 Location (Optional)")

    if st.button("Run Analysis"):
        input_data = pd.DataFrame({
            "pH": [ph],
            "TDS": [tds],
            "Hardness": [hardness]
        })

        # ---------------- AI Prediction ----------------
        predicted = model.predict(input_data)[0]
        nitrate_pred, uranium_pred = predicted

        # ---------------- Identify problematic elements ----------------
        elements_found = []
        if nitrate_pred > 45:
            elements_found.append(f"Nitrate: {nitrate_pred:.1f} mg/L")
        if uranium_pred > 30:
            elements_found.append(f"Uranium: {uranium_pred:.2f} µg/L")
        if ph < 6.5 or ph > 8.5:
            elements_found.append(f"pH Imbalance: {ph:.2f}")
        if tds > 500:
            elements_found.append(f"TDS High: {tds:.1f} mg/L")
        if hardness > 300:
            elements_found.append(f"Hardness High: {hardness:.1f} mg/L")

        if len(elements_found) == 0:
            st.success("✅ Water appears safe! All parameters within safe limits.")
        else:
            st.warning("⚠️ Potential contamination detected!")
            for elem in elements_found:
                st.info(elem)

        # ---------------- Bar Chart for Elements ----------------
        fig = go.Figure()
        fig.add_trace(go.Bar(x=["Nitrate","Uranium"], y=[nitrate_pred, uranium_pred],
                             marker_color=["red" if nitrate_pred>45 else "#39FF14",
                                           "red" if uranium_pred>30 else "#39FF14"]))
        fig.update_layout(title="Predicted Element Levels", yaxis_title="Concentration", height=400)
        st.plotly_chart(fig, use_container_width=True)

        # ---------------- Save Data ----------------
        new_data = pd.DataFrame([[location, ph, tds, hardness, nitrate_pred, uranium_pred]],
                                columns=["Location","pH","TDS","Hardness","Predicted_Nitrate","Predicted_Uranium"])
        if os.path.exists("water_data.csv"):
            df = pd.read_csv("water_data.csv")
            df = pd.concat([df, new_data], ignore_index=True)
        else:
            df = new_data
        df.to_csv("water_data.csv", index=False)
        st.success("Data saved successfully ✅")
        st.download_button("📥 Download Dataset", data=df.to_csv(index=False),
                           file_name="water_data.csv", mime="text/csv")

# ---- TAB 2: Safety Meter ----
with tabs[1]:
    st.subheader("📊 Parameter Levels vs Safe Limits")
    safe_ranges = {
        "pH": (6.5, 8.5, ph),
        "TDS (mg/L)": (0, 500, tds),
        "Hardness (mg/L)": (0, 200, hardness),
        "Predicted Nitrate": (0, 45, nitrate_pred),
        "Predicted Uranium": (0, 30, uranium_pred)
    }

    for param, (low, high, value) in safe_ranges.items():
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=[param],
            y=[value],
            marker_color="red" if value < low or value > high else "#39FF14"
        ))
        fig.add_shape(type="rect", x0=-0.5, x1=0.5, y0=low, y1=high, fillcolor="rgba(57,255,20,0.2)", line_width=0)
        fig.update_layout(height=200, width=300, margin=dict(l=10,r=10,t=30,b=10))
        st.plotly_chart(fig, use_container_width=False)
        status = "✅ Safe" if low <= value <= high else "⚠️ Unsafe"
        color = "#39FF14" if low <= value <= high else "red"
        st.markdown(f"<div style='font-size:16px; color:{color};'><b>{param}: {status}</b></div>", unsafe_allow_html=True)

# ---- TAB 3: Radioactive Awareness ----
with tabs[2]:
    st.subheader("⚠️ Dangers of Radioactive Water")
    st.image("radioactive_process.png", caption="Radioactive Contamination Process", use_container_width=True)
    st.markdown("""
    - ☢️ Long-term exposure can increase cancer risk.
    - 🧬 May cause organ damage and genetic mutations.
    - 🌍 Bioaccumulation affects plants and animals.
    - 🛡️ Follow WHO guidelines for safe drinking water.
    """)

# ---- Connect Section ----
st.markdown("""
<div style="text-align:center; margin-top:10px;">
    <p style="color:#FFD300; font-size:16px;">
        Connect with me: 
        <a href="https://www.linkedin.com/in/karthikeyan-t-82a86931a" target="_blank" style="color:#00FF7F;">LinkedIn</a> | 
        <a href="mailto:karthikeyant1885@gmail.com" style="color:#00FF7F;">Email</a>
    </p>
</div>
""", unsafe_allow_html=True)

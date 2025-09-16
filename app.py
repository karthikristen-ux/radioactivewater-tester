import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import joblib
import os
import time
import numpy as np

# ================= GOOGLE SITE VERIFICATION =================
st.markdown("""
<head>
    <meta name="google-site-verification" content="google428314d1749adc2d" />
</head>
""", unsafe_allow_html=True)

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Radioactive Water Contamination Detector", layout="wide")

# ================= CUSTOM CSS =================
css_block = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');

* { font-family: 'Bebas Neue', sans-serif !important; }

html, body, [class*="css"] { background-color: #0a0a0a; color: #e8f5e9; min-height: 100vh; }

h1.app-title { text-align: center; color: #FFD300; font-size: 52px; margin-bottom: 4px; text-shadow: 0 0 10px #FFD300, 0 0 28px #FF7518; }
p.app-sub { text-align: center; color: #39FF14; margin-top: 0; font-size: 20px; text-shadow: 0 0 10px #39FF14; }

.stTabs [role="tablist"] button {
    background: #101010 !important;
    color: #39FF14 !important;
    border-radius: 12px !important;
    border: 1px solid rgba(57,255,20,0.3) !important;
    margin-right: 6px !important;
    padding: 8px 14px !important;
    transition: all .18s ease;
    font-size: 16px !important;
}
.stTabs [role="tablist"] button:hover {
    background: #39FF14 !important;
    color: black !important;
    transform: translateY(-2px) scale(1.03);
    box-shadow: 0 0 18px rgba(57,255,20,0.15);
}
.stTabs [role="tablist"] button[aria-selected="true"] {
    background: linear-gradient(90deg, #FFD300, #FF7518) !important;
    color: black !important;
    border: 1px solid #FFD300 !important;
    box-shadow: 0 0 26px rgba(255,211,0,0.35);
}
</style>
"""
st.markdown(css_block, unsafe_allow_html=True)

# ================= LOAD AI MODEL =================
model_path = "models/contaminant_model.pkl"
if not os.path.exists(model_path):
    st.error("❌ AI model not found! Please run train_model.py first.")
    st.stop()

model = joblib.load(model_path)

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
    uranium = st.number_input("Uranium (ppb)", 0.0, 200.0, 10.0)
    location = st.text_input("📍 Location")

    if st.button("Run Analysis"):
        input_data = np.array([[ph, nitrate, tds, hardness, uranium]])
        prediction = model.predict(input_data)[0]  # 0 = Safe, 1 = Unsafe

        if prediction == 0:
            result = '✅ Safe: No significant radioactive contamination detected.'
            score = 20
        else:
            result = '☢️ High Risk: Potential radioactive contamination detected!'
            score = 80

        st.markdown(f"<p style='font-size:20px; color:#FFD300;'>{result}</p>", unsafe_allow_html=True)

        # ----------------- Animated Gauge -----------------
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=0,
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
        gauge_placeholder = st.empty()
        for i in range(0, int(score)+1, 2):
            fig.update_traces(value=i)
            gauge_placeholder.plotly_chart(fig, use_container_width=True)
            time.sleep(0.02)

        # ----------------- Save Dataset -----------------
        new_data = pd.DataFrame([[location, ph, tds, hardness, nitrate, uranium, score]],
                                columns=["Location", "pH", "TDS", "Hardness", "Nitrate", "Uranium", "RiskScore"])
        if os.path.exists("water_data.csv"):
            old_data = pd.read_csv("water_data.csv")
            df = pd.concat([old_data, new_data], ignore_index=True)
        else:
            df = new_data
        df.to_csv("water_data.csv", index=False)

        st.success("Data saved successfully ✅")
        st.download_button("📥 Download Dataset", data=df.to_csv(index=False),
                           file_name="water_data.csv", mime="text/csv")

# ---- TAB 2 ----
with tabs[1]:
    st.subheader("📊 Safe vs Unsafe Water Levels (Mini Dashboard)")

    safe_ranges = {
        "pH": (6.5, 8.5, ph),
        "TDS (mg/L)": (0, 500, tds),
        "Hardness": (0, 200, hardness),
        "Nitrate": (0, 45, nitrate),
        "Uranium": (0, 30, uranium)
    }

    params = list(safe_ranges.items())

    for i in range(0, len(params), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j >= len(params):
                break
            param, (low, high, value) = params[i + j]
            with col:
                subcols = st.columns([1.1, 1.0, 0.7])
                with subcols[0]:
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=[param],
                        y=[value],
                        name=f"{param} Value",
                        marker_color="red" if value < low or value > high else "#39FF14"
                    ))
                    fig.add_shape(
                        type="rect",
                        x0=-0.5, x1=0.5,
                        y0=low, y1=high,
                        fillcolor="rgba(57,255,20,0.2)",
                        line_width=0
                    )
                    fig.update_layout(
                        title=f"{param} Level",
                        barmode="overlay",
                        height=180, width=180,
                        margin=dict(l=10, r=10, t=30, b=10)
                    )
                    st.plotly_chart(fig, use_container_width=False)
                with subcols[1]:
                    st.markdown(
                        f"<div style='font-size:16px; color:#FFD300;'><b>{param}</b><br>Safe Range: {low} – {high}<br>Your Value: <span style='color:{'red' if value < low or value > high else '#39FF14'};'>{value}</span></div>",
                        unsafe_allow_html=True
                    )
                with subcols[2]:
                    status = "✅ Safe" if low <= value <= high else "⚠️ Unsafe"
                    color = "#39FF14" if low <= value <= high else "red"
                    st.markdown(f"<div style='font-size:18px; color:{color};'><b>{status}</b></div>", unsafe_allow_html=True)

    st.info("ℹ️ Compare your water parameters above with the WHO safe ranges.")

# ---- TAB 3 ----
with tabs[2]:
    st.subheader("⚠️ Dangers of Radioactive Water")
    st.image("radioactive_process.png", caption="Radioactive Contamination Process", use_container_width=True)

    sections = [
        {"title": "☢️ Health Risks", "title_color": "#FFD700", "content": [
            ('Cancer: Long-term exposure to radioactive elements can increase cancer risk.', "https://ensia.com/features/radioactive-contamination-drinking-water-radium-radon-uranium/?utm_source=chatgpt.com"),
            ('Organ Damage: Kidney and liver dysfunction may occur.', "https://pmc.ncbi.nlm.nih.gov/articles/PMC3261972/?utm_source=chatgpt.com"),
            ('Genetic Mutations: Can affect future generations.', "https://link.springer.com/chapter/10.1007/978-3-031-89591-3_10?utm_source=chatgpt.com")
        ]},
        {"title": "🌍 Environmental Impact", "title_color": "#FFD700", "content": [
            ('Bioaccumulation: Radioactive isotopes accumulate in plants & animals.', "https://ensia.com/features/radioactive-contamination-drinking-water-radium-radon-uranium/?utm_source=chatgpt.com"),
            ('Ecosystem Disruption: Contaminated water affects biodiversity.', None)
        ]},

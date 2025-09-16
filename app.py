import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import time
import joblib

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Radioactive Water Contamination Detector", layout="wide")

# ================= LOAD AI MODEL =================
model = joblib.load("models/contaminant_model.pkl")

# ================= CUSTOM CSS =================
css_block = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');

* {
  font-family: 'Bebas Neue', sans-serif !important;
}

html, body, [class*="css"] {
  background-color: #0a0a0a;
  color: #e8f5e9;
  min-height: 100vh;
}

/* Title & Subtitle */
h1.app-title {
  text-align: center;
  color: #FFD300;
  font-size: 52px;
  margin-bottom: 4px;
  text-shadow: 0 0 10px #FFD300, 0 0 28px #FF7518;
}
p.app-sub {
  text-align: center;
  color: #39FF14;
  margin-top: 0;
  font-size: 20px;
  text-shadow: 0 0 10px #39FF14;
}

/* Tabs */
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

# ================= AI PREDICTION FUNCTION =================
def predict_contamination_ai(ph, tds, hardness, nitrate, uranium):
    input_data = [[ph, nitrate, tds, hardness, uranium]]
    prediction = model.predict(input_data)[0]

    if prediction == 0:
        return "✅ Safe: No significant radioactive contamination detected.", 20
    else:
        return "☢️ High Risk: Potential radioactive contamination detected!", 80

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
    uranium = st.number_input("Uranium (µg/L)", 0.0, 100.0, 10.0)
    location = st.text_input("📍 Location")

    if st.button("Run Analysis"):
        result, score = predict_contamination_ai(ph, tds, hardness, nitrate, uranium)

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
        "Hardness (mg/L)": (0, 300, hardness),
        "Nitrate (mg/L)": (0, 45, nitrate),
        "Uranium (µg/L)": (0, 30, uranium)
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

                # Small Bar Graph
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

                # Display Value
                with subcols[1]:
                    st.markdown(
                        f"""
                        <div style="font-size:16px; color:#FFD300;">
                        <b>{param}</b><br>
                        Safe Range: {low} – {high}<br>
                        Your Value: <span style="color:{'red' if value < low or value > high else '#39FF14'};">{value}</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                # Parameter Status
                with subcols[2]:
                    status = "✅ Safe" if low <= value <= high else "⚠️ Unsafe"
                    color = "#39FF14" if low <= value <= high else "red"
                    st.markdown(
                        f"<div style='font-size:18px; color:{color};'><b>{status}</b></div>",
                        unsafe_allow_html=True
                    )

    st.info("ℹ️ Compare your water parameters above with the WHO safe ranges.")

# ---- TAB 3 ----
with tabs[2]:
    st.subheader("⚠️ Dangers of Radioactive Water")
    st.image("radioactive_process.png", caption="Radioactive Contamination Process", use_container_width=True)

    st.markdown("""
    - ☢️ **Health Risks**: Cancer, organ damage, genetic mutations.  
    - 🌍 **Environmental Impact**: Bioaccumulation, ecosystem disruption.  
    - 🛡️ **WHO Guidelines**: Follow safe limits for pH, TDS, Hardness, Nitrate, and Uranium.  
    """)
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

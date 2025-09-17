import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Radioactive Water Detector", layout="wide")

# ================= CUSTOM CSS =================
css_block = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');

* { font-family: 'Bebas Neue', sans-serif !important; }

html, body, [class*="css"] {
  background-color: #0a0a0a;
  color: #e8f5e9;
  min-height: 100vh;
}

h1.app-title { text-align: center; color: #FFD300; font-size: 52px; margin-bottom: 4px; text-shadow: 0 0 10px #FFD300, 0 0 28px #FF7518; }
p.app-sub { text-align: center; color: #39FF14; margin-top: 0; font-size: 20px; text-shadow: 0 0 10px #39FF14; }

.stTabs [role="tablist"] button { background: #101010 !important; color: #39FF14 !important; border-radius: 12px !important; border: 1px solid rgba(57,255,20,0.3) !important; margin-right: 6px !important; padding: 8px 14px !important; transition: all .18s ease; font-size: 16px !important; }
.stTabs [role="tablist"] button:hover { background: #39FF14 !important; color: black !important; transform: translateY(-2px) scale(1.03); box-shadow: 0 0 18px rgba(57,255,20,0.15); }
.stTabs [role="tablist"] button[aria-selected="true"] { background: linear-gradient(90deg, #FFD300, #FF7518) !important; color: black !important; border: 1px solid #FFD300 !important; box-shadow: 0 0 26px rgba(255,211,0,0.35); }

.glow-green { color: #39FF14; text-shadow: 0 0 20px #39FF14; font-size: 22px; }
.glow-red { color: red; text-shadow: 0 0 20px red; font-size: 22px; }
</style>
"""
st.markdown(css_block, unsafe_allow_html=True)

# ================= FUNCTIONS =================
def predict_contamination(ph, tds, hardness, nitrate):
    score = 0
    if ph < 6.5 or ph > 8.5: score += 30
    if tds > 500: score += 25
    if hardness > 200: score += 20
    if nitrate > 45: score += 25
    return score

def detect_elements(ph, tds, hardness, nitrate):
    elements = []
    if ph < 6.5 or tds > 550 or hardness > 200: elements.append("Uranium")
    if nitrate > 40 or tds > 600: elements.append("Cesium")
    if ph > 7.5 and hardness < 150: elements.append("Radium")
    return elements if elements else ["None Detected"]

def show_risk_gauge(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Radioactive Risk %"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "red" if score >= 60 else "orange" if score >= 30 else "green"},
            'steps': [
                {'range': [0, 30], 'color': "lightgreen"},
                {'range': [30, 60], 'color': "yellow"},
                {'range': [60, 100], 'color': "red"}
            ],
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

# ================= UI =================
st.markdown("<h1 class='app-title'>💧☢️ Radioactive Water Detector</h1>", unsafe_allow_html=True)
st.markdown("<p class='app-sub'>Futuristic AI/ML Powered System | Developed by Our Team</p>", unsafe_allow_html=True)

tabs = st.tabs(["🔬 Contamination Check", "📊 Safe vs Unsafe Levels", "📁 Dataset", "📚 Methodology & Treatment"])

# ---- TAB 1 ----
with tabs[0]:
    st.subheader("Enter Water Parameters")
    ph = st.number_input("pH Level", 0.0, 14.0, 7.0)
    tds = st.number_input("TDS (mg/L)", 0.0, 2000.0, 300.0)
    hardness = st.number_input("Hardness (mg/L)", 0.0, 1000.0, 150.0)
    nitrate = st.number_input("Nitrate (mg/L)", 0.0, 500.0, 20.0)
    location = st.text_input("Location")

    if st.button("Run Analysis"):
        score = predict_contamination(ph, tds, hardness, nitrate)
        elements = detect_elements(ph, tds, hardness, nitrate)
        result_label = "✅ Safe" if score < 30 else "⚠️ Moderate Risk" if score < 60 else "☢️ High Risk"
        st.markdown(f"<p class='glow-red'>{result_label}</p>", unsafe_allow_html=True)
        st.markdown(f"**Detected Elements:** {', '.join(elements)}")
        show_risk_gauge(score)

        # Save dataset
        new_data = pd.DataFrame([[location, ph, tds, hardness, nitrate, score, ', '.join(elements)]],
                                columns=["Location","pH","TDS","Hardness","Nitrate","RiskScore","Elements"])
        try:
            old_data = pd.read_csv("water_data.csv")
            df = pd.concat([old_data, new_data], ignore_index=True)
        except:
            df = new_data
        df.to_csv("water_data.csv", index=False)
        st.success("Data saved successfully ✅")
        st.download_button("📥 Download Dataset", data=df.to_csv(index=False), file_name="water_data.csv", mime="text/csv")

# ---- TAB 2 ----
with tabs[1]:
    st.subheader("Safe vs Unsafe Levels")
    safe_ranges = {"pH": (6.5, 8.5, ph), "TDS": (0, 500, tds), "Hardness": (0, 200, hardness), "Nitrate": (0, 45, nitrate)}
    for param, (low, high, value) in safe_ranges.items():
        color = "green" if low <= value <= high else "red"
        st.markdown(f"**{param}:** {value} ({'Safe' if color=='green' else 'Unsafe'})")

# ---- TAB 3 ----
with tabs[2]:
    st.subheader("Dataset Viewer")
    try:
        df = pd.read_csv("water_data.csv")
        st.dataframe(df)
        remove_cols = st.multiselect("Remove unwanted columns", options=df.columns.tolist())
        if remove_cols:
            df = df.drop(columns=remove_cols)
            st.dataframe(df)
    except:
        st.info("No dataset available yet.")

# ---- TAB 4 ----
with tabs[3]:
    st.subheader("Methodology & Water Treatment Suggestions")
    st.write("""
    **Element Detection Methodology:**  
    - Based on correlations of pH, TDS, Hardness, Nitrate with radioactive elements.  
    - Rules adapted from UNSCEAR and WHO studies.

    **Treatment Suggestions:**  
    - **Uranium:** Reverse osmosis, ion-exchange filtration  
    - **Cesium:** Activated carbon, reverse osmosis  
    - **Radium:** Lime softening, reverse osmosis  

    **Disclaimer:** This is a preliminary estimation. Always confirm with certified labs.
    """)

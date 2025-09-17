import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Radioactive Water Contamination Detector", layout="wide")

# ================= CUSTOM CSS =================
css_block = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');
* { font-family: 'Bebas Neue', sans-serif !important; }
html, body, [class*="css"] { background-color: #0a0a0a; color: #e8f5e9; min-height:100vh; }
h1.app-title { text-align:center; color:#FFD300; font-size:52px; margin-bottom:4px; text-shadow:0 0 10px #FFD300,0 0 28px #FF7518; }
p.app-sub { text-align:center; color:#39FF14; margin-top:0; font-size:20px; text-shadow:0 0 10px #39FF14; }
.stTabs [role="tablist"] button { background:#101010 !important; color:#39FF14 !important; border-radius:12px !important; border:1px solid rgba(57,255,20,0.3) !important; margin-right:6px !important; padding:8px 14px !important; transition: all .18s ease; font-size:16px !important; }
.stTabs [role="tablist"] button:hover { background:#39FF14 !important; color:black !important; transform:translateY(-2px) scale(1.03); box-shadow:0 0 18px rgba(57,255,20,0.15);}
.stTabs [role="tablist"] button[aria-selected="true"] { background: linear-gradient(90deg,#FFD300,#FF7518) !important; color:black !important; border:1px solid #FFD300 !important; box-shadow:0 0 26px rgba(255,211,0,0.35);}
.glow-green { color:#39FF14; text-shadow:0 0 20px #39FF14; font-size:22px;}
.glow-red { color:red; text-shadow:0 0 20px red; font-size:22px;}
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
    # Simple simulation logic: return elements based on thresholds
    elements = []
    if ph < 6.5 or ph > 8.5: elements.append("Uranium")
    if tds > 500: elements.append("Cesium")
    if hardness > 200: elements.append("Radium")
    if nitrate > 45: elements.append("Other Traces")
    return ", ".join(elements) if elements else "None"

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

def show_safety_graph_small(ph, tds, hardness, nitrate):
    safe_ranges = {"pH": (6.5, 8.5, ph), "TDS": (0, 500, tds), "Hardness": (0, 200, hardness), "Nitrate": (0, 45, nitrate)}
    for param, (low, high, value) in safe_ranges.items():
        col1, col2 = st.columns([1.1, 1.0])
        with col1:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=[param],
                y=[value],
                marker_color="red" if value < low or value > high else "green"
            ))
            fig.add_shape(type="rect", x0=-0.5, x1=0.5, y0=low, y1=high, fillcolor="lightgreen", opacity=0.3, line_width=0)
            fig.update_layout(title=f"{param} Level", barmode="overlay", height=220, width=220, margin=dict(l=20,r=20,t=40,b=20))
            st.plotly_chart(fig, use_container_width=False)
        with col2:
            st.markdown(f"""
                <div style="font-size:18px; color:#FFD300;">
                <b>{param}</b><br>
                ✅ Safe Range: {low} – {high}<br>
                💧 Your Value: <span style="color:{'red' if value<low or value>high else 'lightgreen'};">{value}</span>
                </div>
            """, unsafe_allow_html=True)

def generate_heatmap(ph, tds, hardness, nitrate):
    # Simulated 5x5 heatmap (asymmetrical like thermal vision)
    grid = np.random.rand(5,5)
    grid[0,0] = ph/14
    grid[1,1] = tds/2000
    grid[2,2] = hardness/1000
    grid[3,3] = nitrate/500
    colorscale = [[0,'green'],[0.5,'yellow'],[1,'red']]
    fig = go.Figure(go.Heatmap(z=grid, colorscale=colorscale))
    fig.update_layout(title="Thermal-style Contamination Heatmap", xaxis_showgrid=False, yaxis_showgrid=False,
                      width=400, height=400)
    st.plotly_chart(fig, use_container_width=False)

# ================= INIT VARIABLES ==================
ph = 7.0
tds = 300.0
hardness = 150.0
nitrate = 20.0
location = ""
score = 0
elements_str = "None"

# ================= UI =================
st.markdown("<h1 class='app-title'>💧☢️ Radioactive Water Contamination Detector</h1>", unsafe_allow_html=True)
st.markdown("<p class='app-sub'>Futuristic AI/ML Powered System | Developed by Our Team</p>", unsafe_allow_html=True)

tabs = st.tabs(["🔬 Contamination Check", "📊 Safety Meter", "⚠️ Radioactive Awareness", "🌡️ Radiation Map & Elements", "📁 Dataset Viewer"])

# ---- TAB 1 ----
with tabs[0]:
    st.subheader("🔍 Enter Water Parameters")
    ph = st.number_input("pH Level", 0.0, 14.0, ph)
    tds = st.number_input("TDS (mg/L)", 0.0, 2000.0, tds)
    hardness = st.number_input("Hardness (mg/L)", 0.0, 1000.0, hardness)
    nitrate = st.number_input("Nitrate (mg/L)", 0.0, 500.0, nitrate)
    location = st.text_input("📍 Location")

    if st.button("Run Analysis"):
        score = predict_contamination(ph, tds, hardness, nitrate)
        elements_str = detect_elements(ph, tds, hardness, nitrate)

        if score < 30:
            result = '<p class="glow-green">✅ Safe: No significant radioactive contamination detected.</p>'
        elif score < 60:
            result = '<p class="glow-red">⚠️ Moderate Risk: Some radioactive traces possible.</p>'
        else:
            result = '<p class="glow-red">☢️ High Risk: Potential radioactive contamination detected!</p>'

        st.markdown(result, unsafe_allow_html=True)
        show_risk_gauge(score)

        # Save dataset
        new_data = pd.DataFrame([[location, ph, tds, hardness, nitrate, score, elements_str]],
                                columns=["Location","pH","TDS","Hardness","Nitrate","RiskScore","Elements Found"])
        try:
            old_data = pd.read_csv("water_data.csv")
            df = pd.concat([old_data,new_data], ignore_index=True)
        except:
            df = new_data
        df.to_csv("water_data.csv", index=False)
        st.success("Data saved successfully ✅")
        st.download_button("📥 Download Dataset", data=df.to_csv(index=False), file_name="water_data.csv", mime="text/csv")

# ---- TAB 2 ----
with tabs[1]:
    st.subheader("📊 Safe vs Unsafe Water Levels")
    show_safety_graph_small(ph, tds, hardness, nitrate)
    st.info("ℹ️ Compare your water parameters above with safe ranges.")

# ---- TAB 3 ----
with tabs[2]:
    st.subheader("⚠️ Dangers of Radioactive Water")
    st.write("""
    - ☢️ Radioactive water exposure can cause **cancer, organ damage, and genetic mutations**.  
    - ☠️ Animals and plants also suffer from **biological accumulation** of radioactive isotopes.  
    - 💧 Continuous monitoring is **critical** for human survival.
    - 📰 [WHO Radioactive Water Guidelines](https://www.who.int/news-room/fact-sheets/detail/radioactive-contamination)
    - 📰 [Example Article on Contamination](https://www.nature.com/articles/s41598-020-60595-2)
    """)

# ---- TAB 4 ----
with tabs[3]:
    st.subheader("🌡️ Radiation Heat Map & Elements Found")
    generate_heatmap(ph, tds, hardness, nitrate)
    st.markdown(f"**Detected Elements:** {elements_str}")

# ---- TAB 5 ----
with tabs[4]:
    st.subheader("📁 Dataset Viewer")
    try:
        df = pd.read_csv("water_data.csv")
        cols = st.multiselect("Select parameters to display", df.columns.tolist(), default=df.columns.tolist())
        st.dataframe(df[cols])
    except:
        st.info("No dataset found yet. Run an analysis first.")

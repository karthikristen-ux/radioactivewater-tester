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

* {
  font-family: 'Bebas Neue', sans-serif !important;
}

html, body, [class*="css"] {
  background-color: #0a0a0a;
  color: #e8f5e9;
  min-height: 100vh;
}

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

.glow-green {
    color: #39FF14;
    text-shadow: 0 0 20px #39FF14;
    font-size: 22px;
}
.glow-red {
    color: red;
    text-shadow: 0 0 20px red;
    font-size: 22px;
}
</style>
"""
st.markdown(css_block, unsafe_allow_html=True)

# ================= FUNCTIONS =================
def contamination_score(ph, tds, hardness, nitrate):
    """Calculates contamination risk score (0-100)"""
    score = 0
    if ph < 6.5 or ph > 8.5: score += 30
    if tds > 500: score += 25
    if hardness > 200: score += 20
    if nitrate > 45: score += 25
    return score

def detect_elements(ph, tds, hardness):
    """Determine possible radioactive element based on thresholds"""
    elements = []
    if ph < 6.5 or tds > 550 or hardness > 200:
        elements.append("Uranium")
    if nitrate > 40 or tds > 600:
        elements.append("Cesium")
    if ph > 7.5 and hardness < 150:
        elements.append("Radium")
    if not elements:
        elements.append("None Detected")
    return elements

def show_risk_gauge(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Contamination Risk %"},
        gauge={
            'axis': {'range':[0,100]},
            'bar': {'color': "red" if score >= 60 else "orange" if score >= 30 else "green"},
            'steps': [
                {'range':[0,30], 'color':'lightgreen'},
                {'range':[30,60], 'color':'yellow'},
                {'range':[60,100], 'color':'red'}
            ]
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

def thermal_heatmap(ph, tds, hardness, nitrate):
    """Square thermal-style heatmap with colored circles"""
    grid = np.random.rand(5,5)
    fig = go.Figure()
    colors = []
    for r in range(5):
        for c in range(5):
            val = np.random.rand()
            if val < 0.33: color='green'
            elif val <0.66: color='yellow'
            else: color='red'
            fig.add_trace(go.Scatter(
                x=[c], y=[r],
                mode='markers',
                marker=dict(size=40, color=color),
                showlegend=False,
                hoverinfo='skip'
            ))
    fig.update_layout(
        title="Radioactive Contamination Heatmap",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=400, width=400,
        plot_bgcolor="#0a0a0a"
    )
    st.plotly_chart(fig, use_container_width=False)

# ================= UI =================
st.markdown("<h1 class='app-title'>💧☢️ Radioactive Water Detector</h1>", unsafe_allow_html=True)
st.markdown("<p class='app-sub'>Team Aquatic Guardians | AI-Free Detection</p>", unsafe_allow_html=True)

tabs = st.tabs(["🔬 Contamination Check", "📊 Safety Meter", "⚠️ Radioactive Awareness", "🌡️ Heatmap & Elements"])

# ---- TAB 1 ----
with tabs[0]:
    st.subheader("🔍 Enter Water Parameters")
    ph = st.number_input("pH Level", 0.0, 14.0, 7.0)
    tds = st.number_input("TDS (mg/L)", 0.0, 2000.0, 300.0)
    hardness = st.number_input("Hardness (mg/L)", 0.0, 1000.0, 150.0)
    nitrate = st.number_input("Nitrate (mg/L)", 0.0, 500.0, 20.0)
    location = st.text_input("📍 Location")

    if st.button("Run Analysis"):
        score = contamination_score(ph, tds, hardness, nitrate)
        elements = detect_elements(ph, tds, hardness)

        if score < 30:
            st.markdown('<p class="glow-green">✅ Safe: No significant contamination.</p>', unsafe_allow_html=True)
        elif score < 60:
            st.markdown('<p class="glow-red">⚠️ Moderate Risk: Possible contamination.</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="glow-red">☢️ High Risk: Contamination detected!</p>', unsafe_allow_html=True)

        show_risk_gauge(score)
        st.write("⚛️ Possible Elements Detected:", ", ".join(elements))

        # Save dataset
        new_data = pd.DataFrame([[location, ph, tds, hardness, nitrate, score, ", ".join(elements)]],
                                columns=["Location","pH","TDS","Hardness","Nitrate","RiskScore","Elements"])
        try:
            old_data = pd.read_csv("water_data.csv")
            df = pd.concat([old_data, new_data], ignore_index=True)
        except:
            df = new_data
        df.to_csv("water_data.csv", index=False)
        st.success("Data saved ✅")
        st.download_button("📥 Download Dataset", data=df.to_csv(index=False), file_name="water_data.csv", mime="text/csv")

# ---- TAB 2 ----
with tabs[1]:
    st.subheader("📊 Safe vs Unsafe Water Levels")
    safe_ranges = {
        "pH": (6.5,8.5, ph),
        "TDS": (0,500, tds),
        "Hardness": (0,200, hardness),
        "Nitrate": (0,45,nitrate)
    }
    for param,(low,high,value) in safe_ranges.items():
        col1,col2 = st.columns([1.1,1.0])
        with col1:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=[param],
                y=[value],
                marker_color="red" if value<low or value>high else "green"
            ))
            fig.add_shape(type="rect", x0=-0.5, x1=0.5, y0=low, y1=high, fillcolor="lightgreen", opacity=0.3, line_width=0)
            fig.update_layout(title=f"{param} Level", barmode="overlay", height=220, width=220,
                              margin=dict(l=20,r=20,t=40,b=20))
            st.plotly_chart(fig, use_container_width=False)
        with col2:
            st.markdown(f"<div style='font-size:18px; color:#FFD300;'><b>{param}</b><br>Safe: {low}-{high}<br>Your Value: <span style='color:{'red' if value<low or value>high else 'lightgreen'}'>{value}</span></div>", unsafe_allow_html=True)

# ---- TAB 3 ----
with tabs[2]:
    st.subheader("⚠️ Real-Life Radioactive Water Awareness")
    st.write("""
    - ☢️ [WHO Guidelines on Safe Drinking Water](https://www.who.int/news-room/fact-sheets/detail/drinking-water)
    - 💧 [UN Water Resources & Safety](https://www.unwater.org)
    - ⚠️ [News: Radioactive Contamination Cases](https://www.bbc.com/news/topics/cx1m7zg0wz4t/radioactive-contamination)
    """)

# ---- TAB 4 ----
with tabs[3]:
    st.subheader("🌡️ Thermal-Style Contamination Heatmap")
    thermal_heatmap(ph, tds, hardness, nitrate)
    st.write("⚛️ Elements detected:", ", ".join(detect_elements(ph, tds, hardness)))

st.markdown("---")
st.markdown('<p style="text-align:center; color:#FFD300;">👨‍💻 Developed by Team Aquatic Guardians</p>', unsafe_allow_html=True)

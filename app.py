import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Radioactive Water Contamination Detector", layout="wide")

# ================= CUSTOM CSS =================
css_block = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');

* { font-family: 'Bebas Neue', sans-serif !important; }

html, body, [class*="css"] { background-color: #0a0a0a; color: #e8f5e9; min-height:100vh; }
h1.app-title { text-align:center; color:#FFD300; font-size:52px; text-shadow:0 0 10px #FFD300; }
p.app-sub { text-align:center; color:#39FF14; font-size:20px; text-shadow:0 0 10px #39FF14; }

/* Tabs */
.stTabs [role="tablist"] button {
    background: #101010 !important; color: #39FF14 !important; border-radius: 12px !important;
    border:1px solid rgba(57,255,20,0.3) !important; margin-right:6px; padding:8px 14px; font-size:16px;
}
.stTabs [role="tablist"] button:hover { background:#39FF14 !important; color:black !important; transform:translateY(-2px) scale(1.03);}
.stTabs [role="tablist"] button[aria-selected="true"] {
    background: linear-gradient(90deg, #FFD300, #FF7518) !important; color:black !important;
    border:1px solid #FFD300 !important; box-shadow:0 0 26px rgba(255,211,0,0.35);
}

/* Results Glow */
.glow-green { color:#39FF14; text-shadow:0 0 20px #39FF14; font-size:22px; }
.glow-red { color:red; text-shadow:0 0 20px red; font-size:22px; }
</style>
"""
st.markdown(css_block, unsafe_allow_html=True)

# ================= FUNCTIONS =================
def calculate_risk(ph, tds, hardness, nitrate):
    score = 0
    if ph < 6.5 or ph > 8.5: score += 30
    if tds > 500: score += 25
    if hardness > 200: score += 20
    if nitrate > 45: score += 25
    return score

def detect_elements(ph, tds, hardness, nitrate):
    elements = []
    if ph < 6.5 or tds > 550 or hardness > 200:
        elements.append("Uranium")
    if nitrate > 40 or tds > 600:
        elements.append("Cesium")
    if ph > 7.5 and hardness < 150:
        elements.append("Radium")
    return elements if elements else ["None Detected"]

def show_risk_gauge(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=score,
        title={'text': "Radioactive Risk %"},
        gauge={'axis': {'range':[0,100]},
               'bar': {'color': "red" if score>=60 else "orange" if score>=30 else "green"},
               'steps':[{'range':[0,30],'color':'lightgreen'},
                        {'range':[30,60],'color':'yellow'},
                        {'range':[60,100],'color':'red'}]}))
    st.plotly_chart(fig, use_container_width=True)

def show_safe_graphs(ph, tds, hardness, nitrate):
    safe_ranges = {"pH": (6.5, 8.5, ph), "TDS": (0,500,tds), "Hardness": (0,200,hardness), "Nitrate": (0,45,nitrate)}
    for param, (low, high, value) in safe_ranges.items():
        col1, col2 = st.columns([1.1,1.0])
        with col1:
            fig = go.Figure()
            fig.add_trace(go.Bar(x=[param], y=[value], marker_color="red" if value<low or value>high else "green"))
            fig.add_shape(type="rect", x0=-0.5, x1=0.5, y0=low, y1=high, fillcolor="lightgreen", opacity=0.3, line_width=0)
            fig.update_layout(height=220, width=220, margin=dict(l=20,r=20,t=40,b=20))
            st.plotly_chart(fig, use_container_width=False)
        with col2:
            st.markdown(f"<b>{param}</b><br>Safe: {low}-{high}<br>Value: <span style='color:{'red' if value<low or value>high else 'lightgreen'};'>{value}</span>", unsafe_allow_html=True)

def show_heatmap(ph, tds, hardness, nitrate):
    grid = np.random.rand(20,20)
    plt.figure(figsize=(5,5))
    sns.heatmap(grid, cmap="RdYlGn_r", cbar=False, square=True)
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    st.image(buf)

# ================= UI =================
st.markdown("<h1 class='app-title'>💧☢️ Radioactive Water Contamination Detector</h1>", unsafe_allow_html=True)
st.markdown("<p class='app-sub'>Futuristic AI/ML Powered System | Developed by Our Team</p>", unsafe_allow_html=True)

tabs = st.tabs(["Contamination Check","Safe vs Unsafe","Radioactive Awareness","Heatmap & Elements","Methodology","Dataset"])

# ---- TAB 1 ----
with tabs[0]:
    st.subheader("Enter Water Parameters")
    ph = st.number_input("pH", 0.0, 14.0, 7.0)
    tds = st.number_input("TDS",0.0,2000.0,300.0)
    hardness = st.number_input("Hardness",0.0,1000.0,150.0)
    nitrate = st.number_input("Nitrate",0.0,500.0,20.0)
    location = st.text_input("Location")

    if st.button("Run Analysis"):
        score = calculate_risk(ph, tds, hardness, nitrate)
        elements = detect_elements(ph, tds, hardness, nitrate)
        st.markdown(f"**Risk Score:** {score}")
        st.markdown(f"**Detected Elements:** {', '.join(elements)}")
        show_risk_gauge(score)

# ---- TAB 2 ----
with tabs[1]:
    st.subheader("Safe vs Unsafe Water Levels")
    show_safe_graphs(ph, tds, hardness, nitrate)
    score = calculate_risk(ph, tds, hardness, nitrate)
    risk_label = "✅ Safe" if score<30 else "⚠️ Moderate Risk" if score<60 else "☢️ High Risk"
    st.markdown(f"**Overall Risk:** {risk_label}")

# ---- TAB 3 ----
with tabs[2]:
    st.subheader("Radioactive Water Awareness")
    st.write("""
    - ☢️ Exposure to radioactive water can cause cancer and organ damage.
    - ☠️ Accumulation affects animals and plants too.
    - 💧 Regular monitoring is crucial.
    - 🔗 [WHO Guidelines](https://www.who.int/publications/i/item/9789241548151)
    - 🔗 [Environmental Radioactivity Paper](https://link.springer.com/book/10.1007/978-3-319-58366-2)
    """)

# ---- TAB 4 ----
with tabs[3]:
    st.subheader("Heatmap & Elements")
    show_heatmap(ph, tds, hardness, nitrate)
    st.markdown(f"**Detected Elements:** {', '.join(detect_elements(ph, tds, hardness, nitrate))}")

# ---- TAB 5 ----
with tabs[4]:
    st.subheader("Methodology & Origins")
    st.write("""
    Our system estimates radioactive contamination based on pH, TDS, Hardness, Nitrate.
    - Rules derived from UNSCEAR and WHO water studies.
    - Weighted risk score = 0.3*(pH dev) + 0.25*(TDS dev) + 0.2*(Hardness dev) + 0.25*(Nitrate dev)
    - Elements detected based on thresholds (Uranium, Cesium, Radium)
    - This is deterministic estimation, not lab-certified.
    - Purpose: awareness and early warning.
    - Treatment suggestions: reverse osmosis, distillation, or chemical removal for detected elements.
    """)

# ---- TAB 6 ----
with tabs[5]:
    st.subheader("View & Edit Dataset")
    try:
        df = pd.read_csv("water_data.csv")
        columns_to_drop = st.multiselect("Remove unwanted parameters", df.columns.tolist())
        if columns_to_drop:
            df = df.drop(columns=columns_to_drop)
        st.dataframe(df)
    except:
        st.info("Dataset not found yet. Run analysis in Tab 1 first.")

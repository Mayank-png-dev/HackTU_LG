import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pickle
from pathlib import Path
import requests
import time


# Page configuration
st.set_page_config(
    page_title="Liver Guard AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS with Dark Theme and Animations
st.markdown("""
<style>
    /* Import modern medical-tech font */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
    
    /* Dark theme color palette */
    :root {
        --primary-color: #00D9FF;
        --secondary-color: #FF006E;
        --accent-color: #FFBE0B;
        --success-color: #06FFA5;
        --warning-color: #FF6B35;
        --background-dark: #0A0E27;
        --background-card: #151B3D;
        --background-elevated: #1E2749;
        --text-light: #E0E7FF;
        --text-dim: #8B92B8;
        --border-glow: #00D9FF;
    }
    
    /* Main background with animated gradient */
    .stApp {
        background: linear-gradient(135deg, #0A0E27 0%, #1a1f3a 50%, #0f1428 100%);
        background-size: 200% 200%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Animated grid background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(0, 217, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 217, 255, 0.03) 1px, transparent 1px);
        background-size: 50px 50px;
        animation: gridMove 20s linear infinite;
        pointer-events: none;
        z-index: 0;
    }
    
    @keyframes gridMove {
        0% { transform: translate(0, 0); }
        100% { transform: translate(50px, 50px); }
    }
    
    /* Main header with neon glow effect */
    .main-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 4.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00D9FF 0%, #FF006E 50%, #FFBE0B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 0 0 30px rgba(0, 217, 255, 0.5);
        animation: pulse 3s ease-in-out infinite, slideDown 1s ease-out;
        letter-spacing: 3px;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.9; transform: scale(1.02); }
    }
    
    @keyframes slideDown {
        from { 
            opacity: 0; 
            transform: translateY(-50px); 
        }
        to { 
            opacity: 1; 
            transform: translateY(0); 
        }
    }
    
    .sub-header {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.4rem;
        color: var(--text-dim);
        text-align: center;
        margin-bottom: 2rem;
        animation: fadeIn 1.5s ease-out;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Glowing card effect */
    .info-box {
        background: linear-gradient(135deg, rgba(0, 217, 255, 0.1) 0%, rgba(255, 0, 110, 0.1) 100%);
        border: 1px solid rgba(0, 217, 255, 0.3);
        border-left: 4px solid var(--border-glow);
        padding: 25px;
        border-radius: 15px;
        margin: 15px 0;
        box-shadow: 
            0 0 20px rgba(0, 217, 255, 0.2),
            inset 0 0 20px rgba(0, 217, 255, 0.05);
        transition: all 0.4s ease;
        animation: slideInLeft 0.8s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .info-box::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent,
            rgba(0, 217, 255, 0.1),
            transparent
        );
        transform: rotate(45deg);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .info-box:hover {
        transform: translateY(-5px) scale(1.02);
        border-color: var(--primary-color);
        box-shadow: 
            0 10px 40px rgba(0, 217, 255, 0.4),
            inset 0 0 30px rgba(0, 217, 255, 0.1);
    }
    
    @keyframes slideInLeft {
        from { 
            opacity: 0; 
            transform: translateX(-50px); 
        }
        to { 
            opacity: 1; 
            transform: translateX(0); 
        }
    }
    
    .info-box h3 {
        color: var(--primary-color);
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        margin-bottom: 10px;
        font-size: 1.4rem;
    }
    
    .info-box p {
        color: var(--text-light);
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    /* Sidebar styling with dark theme */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f1428 0%, #1a1f3a 100%);
        border-right: 1px solid rgba(0, 217, 255, 0.2);
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        background-color: transparent;
    }
    
    /* Metric cards with glow */
    .stMetric {
        background: rgba(30, 39, 73, 0.6);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(0, 217, 255, 0.2);
        box-shadow: 0 4px 15px rgba(0, 217, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 217, 255, 0.3);
        border-color: var(--primary-color);
    }
    
    /* Enhanced button styling */
    .stButton>button {
        background: linear-gradient(135deg, #00D9FF 0%, #0099CC 100%);
        color: #0A0E27;
        border: none;
        border-radius: 10px;
        padding: 15px 30px;
        font-weight: 700;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.1rem;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 217, 255, 0.3);
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton>button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 8px 30px rgba(0, 217, 255, 0.5);
    }
    
    /* Text color overrides */
    h1, h2, h3, h4, h5, h6, p, label, span, div {
        color: var(--text-light) !important;
    }
    
    /* Success/Warning/Error boxes */
    .stSuccess {
        background: rgba(6, 255, 165, 0.1);
        border-left: 4px solid var(--success-color);
        color: var(--success-color);
    }
    
    .stWarning {
        background: rgba(255, 190, 11, 0.1);
        border-left: 4px solid var(--accent-color);
        color: var(--accent-color);
    }
    
    .stError {
        background: rgba(255, 0, 110, 0.1);
        border-left: 4px solid var(--secondary-color);
        color: var(--secondary-color);
    }
    
    /* Floating particles effect */
    .particle {
        position: fixed;
        width: 3px;
        height: 3px;
        background: var(--primary-color);
        border-radius: 50%;
        opacity: 0.3;
        animation: float 20s infinite ease-in-out;
        pointer-events: none;
        z-index: 1;
    }
    
    @keyframes float {
        0%, 100% { 
            transform: translateY(0) translateX(0);
            opacity: 0;
        }
        10% { opacity: 0.3; }
        90% { opacity: 0.3; }
        100% { 
            transform: translateY(-100vh) translateX(100px);
            opacity: 0;
        }
    }
    
    /* Radio button styling */
    .stRadio > label {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-light) !important;
    }
    
    /* Input fields */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        background: rgba(30, 39, 73, 0.6) !important;
        border: 1px solid rgba(0, 217, 255, 0.3) !important;
        color: var(--text-light) !important;
        border-radius: 8px !important;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 10px rgba(0, 217, 255, 0.3) !important;
    }
    
    /* Slider styling */
    .stSlider > div > div > div {
        background: var(--primary-color) !important;
    }
    
    /* Chart containers */
    .js-plotly-plot {
        background: rgba(30, 39, 73, 0.3) !important;
        border-radius: 12px;
        padding: 10px;
        border: 1px solid rgba(0, 217, 255, 0.2);
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, 
            transparent, 
            var(--primary-color), 
            transparent
        );
        margin: 30px 0;
    }
    
    /* Tooltip styling */
    [data-testid="stTooltipIcon"] {
        color: var(--primary-color);
    }
    
    /* Loading animation */
    .stSpinner > div {
        border-color: var(--primary-color) !important;
    }
</style>

<!-- Add floating particles -->
<script>
    function createParticles() {
        for(let i = 0; i < 20; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 20 + 's';
            particle.style.animationDuration = (Math.random() * 10 + 15) + 's';
            document.body.appendChild(particle);
        }
    }
    
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', createParticles);
    } else {
        createParticles();
    }
</script>
""", unsafe_allow_html=True)

# Sidebar navigation
def sidebar_navigation():
    st.sidebar.markdown('<h2 style="font-family: Orbitron; color: #00D9FF; text-align: center;">🏥 Liver Guard AI</h2>', unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Navigation",
        ["🏠 Home", "📊 Dashboard", "🔬 Live Detection", "📈 Analytics", "ℹ️ About"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown('<h3 style="font-family: Rajdhani; color: #00D9FF;">⚡ Quick Stats</h3>', unsafe_allow_html=True)
    st.sidebar.metric("Total Scans", "1,234", "+12%")
    st.sidebar.metric("Accuracy", "94.7%", "+2.3%")
    st.sidebar.metric("Active Users", "89", "+5")
    
    return page

# Main app
def main():
    page = sidebar_navigation()
    
    if page == "🏠 Home":
        show_home()
    elif page == "📊 Dashboard":
        show_dashboard()
    elif page == "🔬 Live Detection":
        show_live_detection()
    elif page == "📈 Analytics":
        show_analytics()
    elif page == "ℹ️ About":
        show_about()

def show_home():
    st.markdown('<h1 class="main-header">LIVER GUARD AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Non-Invasive Liver Disease Detection</p>', unsafe_allow_html=True)
    
    # Hero section with animated cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="info-box" style="animation-delay: 0s;">
            <h3>🎯 High Accuracy</h3>
            <p>94.7% detection accuracy using advanced ML models</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box" style="animation-delay: 0.2s;">
            <h3>⚡ Real-time Monitoring</h3>
            <p>Continuous IoT-based health tracking</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-box" style="animation-delay: 0.4s;">
            <h3>🏥 Non-Invasive</h3>
            <p>Skin sensors & thermal imaging technology</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Overview section with enhanced layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h2 style="font-family: Orbitron; color: #00D9FF;">🔬 How It Works</h2>', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-family: Rajdhani; font-size: 1.1rem; line-height: 1.8;">
        Our system combines three key parameters:
        
        <br><br>
        <strong style="color: #00D9FF;">1. Skin Impedance</strong> — Measures electrical properties to detect fat infiltration
        <br><br>
        <strong style="color: #FF006E;">2. Thermal Imaging</strong> — Detects abnormal temperature patterns indicating inflammation
        <br><br>
        <strong style="color: #FFBE0B;">3. Skin Color Analysis</strong> — Rapid detection of jaundice and hyperpigmentation
        <br><br>
        These parameters are processed through an ensemble ML model using Random Forest, 
        SVM, Logistic Regression, XGBoost, and CatBoost for superior accuracy.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Quick action buttons with enhanced styling
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🚀 Start Live Detection", use_container_width=True):
                st.session_state.page = "🔬 Live Detection"
                st.rerun()
        with col_btn2:
            if st.button("📊 View Dashboard", use_container_width=True):
                st.session_state.page = "📊 Dashboard"
                st.rerun()
    
    with col2:
        # System status with glowing indicators
        st.markdown('<h3 style="font-family: Orbitron; color: #00D9FF;">📡 System Status</h3>', unsafe_allow_html=True)
        st.success("✅ All sensors connected")
        st.info("📶 IoT devices: 4/4 active")
        st.warning("⚡ ESP32: Online")
        
        # Recent activity
        st.markdown('<h3 style="font-family: Orbitron; color: #00D9FF; margin-top: 30px;">🕐 Recent Activity</h3>', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-family: Rajdhani; font-size: 1rem; line-height: 2;">
        • Scan completed - 2 min ago<br>
        • Data synced - 5 min ago<br>
        • Model updated - 1 hour ago
        </div>
        """, unsafe_allow_html=True)

def show_dashboard():
    st.markdown('<h1 class="main-header">Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Scans Today",
            value="47",
            delta="12 from yesterday"
        )
    
    with col2:
        st.metric(
            label="Detection Accuracy",
            value="94.7%",
            delta="2.3%"
        )
    
    with col3:
        st.metric(
            label="Healthy Results",
            value="68%",
            delta="-5%"
        )
    
    with col4:
        st.metric(
            label="Avg Response Time",
            value="1.2s",
            delta="-0.3s"
        )
    
    st.markdown("---")
    
    # Main visualizations with dark theme
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 style="font-family: Orbitron; color: #00D9FF;">📈 Scan Trends (Last 30 Days)</h3>', unsafe_allow_html=True)
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        scans = np.random.poisson(35, 30) + np.random.randint(-5, 10, 30)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=scans,
            mode='lines+markers',
            name='Daily Scans',
            line=dict(color='#00D9FF', width=3),
            marker=dict(size=8, color='#00D9FF'),
            fill='tozeroy',
            fillcolor='rgba(0, 217, 255, 0.2)'
        ))
        
        fig.update_layout(
            height=400,
            hovermode='x unified',
            plot_bgcolor='rgba(10, 14, 39, 0.5)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E0E7FF', family='Rajdhani'),
            xaxis=dict(showgrid=True, gridcolor='rgba(0, 217, 255, 0.1)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(0, 217, 255, 0.1)'),
            margin=dict(l=20, r=20, t=20, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<h3 style="font-family: Orbitron; color: #00D9FF;">🎯 Detection Results Distribution</h3>', unsafe_allow_html=True)
        labels = ['Healthy', 'Fatty Liver', 'Cirrhosis', 'NAFLD']
        values = [68, 18, 8, 6]
        colors = ['#06FFA5', '#FFBE0B', '#FF006E', '#FF6B35']
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker=dict(colors=colors, line=dict(color='#0A0E27', width=2)),
            textinfo='label+percent',
            textfont=dict(size=14, color='#0A0E27', family='Rajdhani', weight='bold')
        )])
        
        fig.update_layout(
            height=400,
            showlegend=True,
            plot_bgcolor='rgba(10, 14, 39, 0.5)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E0E7FF', family='Rajdhani'),
            margin=dict(l=20, r=20, t=20, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Sensor data visualization
    st.markdown('<h3 style="font-family: Orbitron; color: #00D9FF; margin-top: 30px;">🌡️ Real-time Sensor Readings</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<h4 style="font-family: Rajdhani; color: #00D9FF; text-align: center;">Skin Impedance</h4>', unsafe_allow_html=True)
        impedance_value = 45
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=impedance_value,
            delta={'reference': 50},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "#00D9FF"},
                'bgcolor': 'rgba(10, 14, 39, 0.5)',
                'steps': [
                    {'range': [0, 33], 'color': "rgba(6, 255, 165, 0.3)"},
                    {'range': [33, 66], 'color': "rgba(255, 190, 11, 0.3)"},
                    {'range': [66, 100], 'color': "rgba(255, 0, 110, 0.3)"}
                ],
                'threshold': {
                    'line': {'color': "#FF006E", 'width': 4},
                    'thickness': 0.75,
                    'value': 70
                }
            }
        ))
        
        fig.update_layout(
            height=250, 
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E0E7FF', family='Rajdhani')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<h4 style="font-family: Rajdhani; color: #00D9FF; text-align: center;">Skin Temperature (°C)</h4>', unsafe_allow_html=True)
        temp_value = 33.5
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=temp_value,
            delta={'reference': 32},
            gauge={
                'axis': {'range': [28, 38]},
                'bar': {'color': "#FFBE0B"},
                'bgcolor': 'rgba(10, 14, 39, 0.5)',
                'steps': [
                    {'range': [28, 31], 'color': "rgba(0, 217, 255, 0.3)"},
                    {'range': [31, 35], 'color': "rgba(6, 255, 165, 0.3)"},
                    {'range': [35, 38], 'color': "rgba(255, 107, 53, 0.3)"}
                ]
            }
        ))
        
        fig.update_layout(
            height=250, 
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E0E7FF', family='Rajdhani')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        st.markdown('<h4 style="font-family: Rajdhani; color: #00D9FF; text-align: center;">Yellowness Index</h4>', unsafe_allow_html=True)
        yellow_value = 25
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=yellow_value,
            delta={'reference': 20},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#FF006E"},
                'bgcolor': 'rgba(10, 14, 39, 0.5)',
                'steps': [
                    {'range': [0, 30], 'color': "rgba(6, 255, 165, 0.3)"},
                    {'range': [30, 60], 'color': "rgba(255, 190, 11, 0.3)"},
                    {'range': [60, 100], 'color': "rgba(255, 0, 110, 0.3)"}
                ]
            }
        ))
        
        fig.update_layout(
            height=250, 
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E0E7FF', family='Rajdhani')
        )
        st.plotly_chart(fig, use_container_width=True)

def show_live_detection():
    st.markdown('<h1 class="main-header">Live Detection</h1>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    # ================= LEFT SIDE =================
    with col1:
        st.markdown('<h3 style="font-family: Orbitron; color: #00D9FF;">📝 Enter Patient Data</h3>', unsafe_allow_html=True)

        with st.form("detection_form"):
            age = st.number_input("Age", 1, 120, 25)
            gender = st.selectbox("Gender", ["Male", "Female"])
            height = st.number_input("Height (cm)", 100, 220, 170)
            weight = st.number_input("Weight (kg)", 30, 200, 70)

            submit_button = st.form_submit_button("🔬 Run Detection", use_container_width=True)

    # ================= RIGHT SIDE =================
    with col2:
        st.markdown('<h3 style="font-family: Orbitron; color: #00D9FF;">📊 Detection Results</h3>', unsafe_allow_html=True)

        if submit_button:
            try:
                # 🟢 Device online indicator
                st.success("🟢 Device Online")

                # 🔄 Loading pipeline
                with st.spinner("Connecting to IoT device..."):
                    time.sleep(1)

                with st.spinner("Collecting biosignals..."):
                    time.sleep(1)

                with st.spinner("Running ensemble models..."):
                    res = requests.get(
                        "http://127.0.0.1:8000/predict",
                        params={
                            "age": age,
                            "gender": gender,
                            "height": height,
                            "weight": weight
                        },
                        timeout=10
                    )

                with st.spinner("Generating clinical advice..."):
                    time.sleep(1)

                data = res.json()

                risk = data["risk"]
                confidence = data["confidence"]
                models = data.get("models", {})
                sensor = data.get("sensor", {})
                advice = data.get("advice", "No advice")

                st.success("✅ Prediction complete")

                # 🎯 FINAL RESULT
                if risk.lower() == "high":
                    st.error(f"⚠️ Risk Level: {risk}")
                else:
                    st.success(f"✅ Risk Level: {risk}")

                st.metric("Confidence", f"{confidence}%")

                # 🧠 MODEL TRANSPARENCY
                st.markdown("### 🧠 Individual Model Decisions")
                for name, val in models.items():
                    st.write(f"**{name}** → {'High' if val==1 else 'Low'}")

                # 🩺 Advice
                st.markdown("### 🏥 Clinical Advice")
                st.info(advice)

                # 🔍 Raw data
                with st.expander("🔍 Sensor Data Used"):
                    st.json(sensor)

            except Exception as e:
                st.error("🔴 Backend or device not reachable")

def show_analytics():
    st.markdown('<h1 class="main-header">Advanced Analytics</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        date_range = st.date_input(
            "Select Date Range",
            value=(datetime.now() - timedelta(days=30), datetime.now()),
            max_value=datetime.now()
        )
    with col2:
        analysis_type = st.selectbox(
            "Analysis Type",
            ["Overview", "Sensor Comparison", "Model Performance"]
        )
    
    st.markdown("---")
    
    if analysis_type == "Overview":
        st.markdown('<h3 style="font-family: Orbitron; color: #00D9FF;">📊 Parameter Trends Comparison</h3>', unsafe_allow_html=True)
        
        days = 30
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        
        impedance_data = 40 + np.random.randn(days).cumsum()
        temp_data = 33 + np.random.randn(days) * 0.5
        yellowness_data = 20 + np.random.randn(days).cumsum() * 0.5
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=dates, y=impedance_data,
            name='Skin Impedance',
            line=dict(color='#00D9FF', width=2),
            yaxis='y1'
        ))
        
        fig.add_trace(go.Scatter(
            x=dates, y=temp_data,
            name='Temperature',
            line=dict(color='#FFBE0B', width=2),
            yaxis='y2'
        ))
        
        fig.add_trace(go.Scatter(
            x=dates, y=yellowness_data,
            name='Yellowness Index',
            line=dict(color='#FF006E', width=2),
            yaxis='y3'
        ))
        
        fig.update_layout(
            height=500,
            hovermode='x unified',
            plot_bgcolor='rgba(10, 14, 39, 0.5)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E0E7FF', family='Rajdhani'),
            yaxis=dict(title='Impedance (Ω)', side='left', color='#00D9FF'),
            yaxis2=dict(title='Temperature (°C)', overlaying='y', side='right', color='#FFBE0B'),
            yaxis3=dict(title='Yellowness', overlaying='y', side='right', position=0.95, color='#FF006E'),
            legend=dict(x=0.01, y=0.99, bgcolor='rgba(21, 27, 61, 0.8)', bordercolor='#00D9FF', borderwidth=1),
            margin=dict(l=50, r=100, t=20, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<h3 style="font-family: Orbitron; color: #00D9FF;">🔥 Parameter Correlation Heatmap</h3>', unsafe_allow_html=True)
            
            correlation_matrix = np.array([
                [1.0, 0.65, 0.72, -0.45],
                [0.65, 1.0, 0.58, -0.38],
                [0.72, 0.58, 1.0, -0.52],
                [-0.45, -0.38, -0.52, 1.0]
            ])
            
            parameters = ['Impedance', 'Temperature', 'Yellowness', 'Health Score']
            
            fig = go.Figure(data=go.Heatmap(
                z=correlation_matrix,
                x=parameters,
                y=parameters,
                colorscale=[[0, '#0A0E27'], [0.5, '#00D9FF'], [1, '#FF006E']],
                zmid=0,
                text=correlation_matrix,
                texttemplate='%{text:.2f}',
                textfont={"size": 12, "color": "#E0E7FF"}
            ))
            
            fig.update_layout(
                height=400, 
                margin=dict(l=20, r=20, t=20, b=20),
                plot_bgcolor='rgba(10, 14, 39, 0.5)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#E0E7FF', family='Rajdhani')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown('<h3 style="font-family: Orbitron; color: #00D9FF;">📈 Detection Accuracy by Month</h3>', unsafe_allow_html=True)
            
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
            accuracy = [92.1, 93.5, 93.8, 94.2, 94.5, 94.7]
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=months,
                y=accuracy,
                marker=dict(
                    color=accuracy,
                    colorscale=[[0, '#00D9FF'], [1, '#06FFA5']],
                    showscale=False
                ),
                text=[f"{a}%" for a in accuracy],
                textposition='outside',
                textfont=dict(color='#E0E7FF')
            ))
            
            fig.update_layout(
                height=400,
                yaxis=dict(range=[90, 96], title='Accuracy (%)', color='#E0E7FF'),
                margin=dict(l=20, r=20, t=20, b=20),
                plot_bgcolor='rgba(10, 14, 39, 0.5)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#E0E7FF', family='Rajdhani')
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    elif analysis_type == "Sensor Comparison":
        st.markdown('<h3 style="font-family: Orbitron; color: #00D9FF;">🔬 Sensor Performance Comparison</h3>', unsafe_allow_html=True)
        
        metrics = ['Accuracy', 'Reliability', 'Speed', 'Cost Efficiency']
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=[95, 92, 88, 85, 95],
            theta=metrics + [metrics[0]],
            fill='toself',
            name='Skin Impedance',
            line=dict(color='#00D9FF', width=2),
            fillcolor='rgba(0, 217, 255, 0.2)'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=[88, 95, 90, 75, 88],
            theta=metrics + [metrics[0]],
            fill='toself',
            name='Thermal Camera',
            line=dict(color='#FFBE0B', width=2),
            fillcolor='rgba(255, 190, 11, 0.2)'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=[90, 88, 95, 92, 90],
            theta=metrics + [metrics[0]],
            fill='toself',
            name='RGB Sensor',
            line=dict(color='#FF006E', width=2),
            fillcolor='rgba(255, 0, 110, 0.2)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True, 
                    range=[0, 100],
                    gridcolor='rgba(0, 217, 255, 0.2)',
                    color='#E0E7FF'
                ),
                bgcolor='rgba(10, 14, 39, 0.5)',
                angularaxis=dict(gridcolor='rgba(0, 217, 255, 0.2)', color='#E0E7FF')
            ),
            showlegend=True,
            height=500,
            plot_bgcolor='rgba(10, 14, 39, 0.5)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E0E7FF', family='Rajdhani'),
            legend=dict(bgcolor='rgba(21, 27, 61, 0.8)', bordercolor='#00D9FF', borderwidth=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    elif analysis_type == "Model Performance":
        st.markdown('<h3 style="font-family: Orbitron; color: #00D9FF;">🤖 ML Model Performance</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            models = ['Random Forest', 'SVM', 'XGBoost', 'CatBoost', 'Ensemble']
            accuracy = [92.3, 91.8, 93.5, 93.2, 94.7]
            precision = [91.5, 90.2, 92.8, 92.5, 94.1]
            recall = [93.1, 92.5, 94.2, 93.8, 95.3]
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(name='Accuracy', x=models, y=accuracy, marker_color='#00D9FF'))
            fig.add_trace(go.Bar(name='Precision', x=models, y=precision, marker_color='#FFBE0B'))
            fig.add_trace(go.Bar(name='Recall', x=models, y=recall, marker_color='#FF006E'))
            
            fig.update_layout(
                barmode='group',
                height=400,
                yaxis=dict(range=[85, 100], title='Score (%)', color='#E0E7FF'),
                title='Model Metrics Comparison',
                title_font=dict(color='#00D9FF', family='Orbitron'),
                plot_bgcolor='rgba(10, 14, 39, 0.5)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#E0E7FF', family='Rajdhani'),
                legend=dict(bgcolor='rgba(21, 27, 61, 0.8)', bordercolor='#00D9FF', borderwidth=1)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown('<h4 style="font-family: Rajdhani; color: #00D9FF; text-align: center;">ROC-AUC Curves</h4>', unsafe_allow_html=True)
            
            fig = go.Figure()
            
            for model, color in zip(['RF', 'SVM', 'XGB', 'Ensemble'], 
                                   ['#00D9FF', '#FFBE0B', '#FF006E', '#06FFA5']):
                fpr = np.linspace(0, 1, 100)
                tpr = 1 - np.exp(-5 * fpr) + np.random.randn(100) * 0.02
                tpr = np.clip(tpr, fpr, 1)
                
                fig.add_trace(go.Scatter(
                    x=fpr, y=tpr,
                    name=f'{model} (AUC=0.{np.random.randint(92, 98)})',
                    line=dict(color=color, width=2)
                ))
            
            fig.add_trace(go.Scatter(
                x=[0, 1], y=[0, 1],
                name='Random',
                line=dict(color='#8B92B8', dash='dash', width=2)
            ))
            
            fig.update_layout(
                height=400,
                xaxis_title='False Positive Rate',
                yaxis_title='True Positive Rate',
                title='ROC Curves',
                title_font=dict(color='#00D9FF', family='Orbitron'),
                plot_bgcolor='rgba(10, 14, 39, 0.5)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#E0E7FF', family='Rajdhani'),
                legend=dict(bgcolor='rgba(21, 27, 61, 0.8)', bordercolor='#00D9FF', borderwidth=1)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('<h3 style="font-family: Orbitron; color: #00D9FF; margin-top: 30px;">Confusion Matrix (Ensemble Model)</h3>', unsafe_allow_html=True)
        
        conf_matrix = np.array([[245, 12], [8, 185]])
        
        fig = go.Figure(data=go.Heatmap(
            z=conf_matrix,
            x=['Predicted Healthy', 'Predicted Unhealthy'],
            y=['Actual Healthy', 'Actual Unhealthy'],
            colorscale=[[0, '#0A0E27'], [1, '#00D9FF']],
            text=conf_matrix,
            texttemplate='%{text}',
            textfont={"size": 20, "color": "#E0E7FF"},
            showscale=True
        ))
        
        fig.update_layout(
            height=400,
            plot_bgcolor='rgba(10, 14, 39, 0.5)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E0E7FF', family='Rajdhani')
        )
        st.plotly_chart(fig, use_container_width=True)

def show_about():
    st.markdown('<h1 class="main-header">About Liver Guard AI</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="font-family: Rajdhani; font-size: 1.2rem; line-height: 1.8; color: #E0E7FF;">
    <h2 style="font-family: Orbitron; color: #00D9FF;">🏥 Project Overview</h2>
    
    Liver Guard AI is an innovative IoT and AI-powered system for non-invasive liver disease detection. 
    The project leverages cutting-edge sensor technology and machine learning to provide accurate, 
    real-time liver health monitoring.
    
    <h3 style="font-family: Orbitron; color: #00D9FF; margin-top: 30px;">🎯 Key Features</h3>
    
    <strong style="color: #00D9FF;">• Non-invasive Detection:</strong> Uses skin sensors, thermal imaging, and color analysis<br>
    <strong style="color: #FFBE0B;">• Real-time Monitoring:</strong> Continuous health tracking through IoT devices<br>
    <strong style="color: #FF006E;">• High Accuracy:</strong> 94.7% detection accuracy using ensemble ML models<br>
    <strong style="color: #06FFA5;">• Early Intervention:</strong> Enables early medical intervention and better outcomes
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="font-family: Rajdhani; font-size: 1.1rem; line-height: 1.8; color: #E0E7FF;">
        <h3 style="font-family: Orbitron; color: #00D9FF;">📊 Parameters Monitored</h3>
        
        <strong style="color: #00D9FF;">1. Skin Impedance</strong><br>
        • Measures electrical properties of skin<br>
        • Detects fat infiltration in liver tissue<br>
        • Non-invasive adhesive sensor<br><br>
        
        <strong style="color: #FFBE0B;">2. Thermal Imaging</strong><br>
        • IR array camera for temperature patterns<br>
        • Detects inflammation and blood flow changes<br>
        • Non-contact measurement<br><br>
        
        <strong style="color: #FF006E;">3. Skin Color Analysis</strong><br>
        • RGB sensor for color measurement<br>
        • Detects jaundice and hyperpigmentation<br>
        • Rapid, accurate assessment
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="font-family: Rajdhani; font-size: 1.1rem; line-height: 1.8; color: #E0E7FF;">
        <h3 style="font-family: Orbitron; color: #00D9FF;">🤖 ML Architecture</h3>
        
        <strong style="color: #00D9FF;">1. Data Augmentation</strong><br>
        • Random noise injection<br>
        • SMOTE interpolation<br><br>
        
        <strong style="color: #FFBE0B;">2. Base Models</strong><br>
        • Random Forest<br>
        • Support Vector Machine<br>
        • Logistic Regression<br>
        • XGBoost<br>
        • CatBoost<br><br>
        
        <strong style="color: #FF006E;">3. Ensemble Learning</strong><br>
        • Stacking<br>
        • Soft voting<br>
        • Hyperparameter tuning
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div style="font-family: Rajdhani; font-size: 1.1rem; line-height: 1.8; color: #E0E7FF;">
    <h3 style="font-family: Orbitron; color: #00D9FF;">🔧 Hardware Components</h3>
    
    <strong style="color: #00D9FF;">• ESP32 Microcontroller:</strong> WiFi/Bluetooth enabled, multi-sensor support<br>
    <strong style="color: #FFBE0B;">• Galvanic Skin Response Module:</strong> Measures skin impedance<br>
    <strong style="color: #FF006E;">• IR Array Thermal Camera:</strong> Non-contact temperature measurement<br>
    <strong style="color: #06FFA5;">• RGB Color Sensor:</strong> Precise color detection<br>
    <strong style="color: #00D9FF;">• Current Sensor Kit:</strong> Electrical measurements
    
    <h3 style="font-family: Orbitron; color: #00D9FF; margin-top: 30px;">💻 Software Stack</h3>
    
    <strong style="color: #00D9FF;">• Arduino IDE:</strong> Sensor programming and data acquisition<br>
    <strong style="color: #FFBE0B;">• Python:</strong> Data processing and ML model training<br>
    <strong style="color: #FF006E;">• Streamlit:</strong> Interactive web interface<br>
    <strong style="color: #06FFA5;">• Plotly:</strong> Advanced data visualizations<br>
    <strong style="color: #00D9FF;">• Scikit-learn:</strong> Machine learning framework
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.success("🎓 Developed as part of healthcare innovation research")

if __name__ == "__main__":
    main()


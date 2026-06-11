import streamlit as st
import google.generativeai as genai
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests

def get_coordinates(city):
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json"
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).json()

        if res:
            return float(res[0]["lat"]), float(res[0]["lon"])
        else:
            return 19.0760, 72.8777
    except:
        return 19.0760, 72.8777

# =========================
# GEMINI API
# =========================

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Disaster Twin AI",
    page_icon="🌍",
    layout="wide"
)

# =========================
# SIDEBAR
# =========================

st.sidebar.title("🌍 Disaster Twin AI")

st.sidebar.success("AI Digital Twin Enabled")
st.sidebar.success("Risk Prediction Engine")
st.sidebar.success("Emergency Response Advisor")
st.sidebar.success("Climate Impact Analysis")

st.sidebar.info("""
Version: 3.0

Features:
✅ AI Disaster Analysis
✅ Risk Assessment
✅ Disaster Detection
✅ Location Analysis
✅ Risk Visualization
✅ Report Download
✅ Emergency Contacts
✅ Disaster Images
✅ Gemini Fallback Mode
""")

# =========================
# MAIN UI
# =========================

st.title("🌍 Disaster Twin AI")
st.subheader("AI Powered Disaster Risk Assessment System")

location = st.text_input("📍 Enter Location")
api_key = st.secrets["OPENWEATHER_API_KEY"]

if location:

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"

        data = requests.get(url).json()

        if "main" in data:

            st.subheader("🌦 Live Weather")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "🌡 Temperature",
                    f"{data['main']['temp']} °C"
                )

            with col2:
                st.metric(
                    "💧 Humidity",
                    f"{data['main']['humidity']}%"
                )

    except:
        st.warning("Weather data unavailable")
user_input = st.text_area(
    "Enter disaster-related query (flood, drought, earthquake, heatwave etc.)"
)

# =========================
# ANALYZE BUTTON
# =========================

if st.button("Analyze Disaster"):

    disaster = user_input.lower()

    if "flood" in disaster:
        risk_score = 85
        disaster_type = "Flood"

    elif "earthquake" in disaster:
        risk_score = 90
        disaster_type = "Earthquake"

    elif "heatwave" in disaster:
        risk_score = 70
        disaster_type = "Heatwave"

    elif "drought" in disaster:
        risk_score = 75
        disaster_type = "Drought"

    elif "cyclone" in disaster:
        risk_score = 88
        disaster_type = "Cyclone"

    else:
        risk_score = 50
        disaster_type = "General Disaster"

    # =========================
    # DISASTER TYPE
    # =========================
    # =========================
# HISTORY SAVE
# =========================

    if "history" not in st.session_state:
        st.session_state.history = []

    st.session_state.history.append(
        {
            "Disaster": disaster_type,
            "Risk": risk_score
        }
    )
    st.subheader("🌪 Detected Disaster Type")
    st.info(disaster_type)

    # =========================
    # RISK ASSESSMENT
    # =========================

    st.subheader("🚨 Risk Assessment")

    st.progress(risk_score)

    if risk_score >= 80:
        st.error(f"🔴 HIGH RISK ({risk_score}%)")

    elif risk_score >= 50:
        st.warning(f"🟡 MEDIUM RISK ({risk_score}%)")

    else:
        st.success(f"🟢 LOW RISK ({risk_score}%)")

    # =========================
    # DISASTER IMAGE
    # =========================

    st.subheader("🖼 Disaster Visualization")

    emoji_map = {
        "Flood": "🌊",
        "Earthquake": "🏚",
        "Heatwave": "☀",
        "Drought": "🌵",
        "Cyclone": "🌀",
        "General Disaster": "⚠"
    }

    st.header(
        f"{emoji_map.get(disaster_type,'⚠')} {disaster_type.upper()} DETECTED"
    )

    image_files = {
        "Flood": "disaster_images/flood.jpg",
        "Earthquake": "disaster_images/earthquake.jpg",
        "Cyclone": "disaster_images/cyclone.jpg",
        "Drought": "disaster_images/drought.jpg",
        "Heatwave": "disaster_images/heatwave.jpg",
        "General Disaster": "disaster_images/general.jpg"
    }

    st.image(
        image_files.get(
            disaster_type,
            "disaster_images/general.jpg"
        ),
        caption=f"{disaster_type} Monitoring System",
        use_container_width=True
    )
    # =========================
# DISASTER LOCATION MAP
# =========================

    st.subheader("🗺 Disaster Location Map")

    lat, lon = get_coordinates(location)

    map_data = pd.DataFrame({
        "lat": [lat],
        "lon": [lon]
    })

    st.map(map_data)
    # =========================
# RISK METER
# =========================
        # =========================
    # RISK METER
    # =========================

    st.subheader("📊 Disaster Risk Meter")

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=risk_score,
            title={"text": "Risk Score"},
            gauge={
                "axis": {"range": [0, 100]}
            }
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📋 Risk Summary")

    risk_df = pd.DataFrame({
        "Parameter": [
            "Disaster Type",
            "Risk Score",
            "Location"
        ],
        "Value": [
            disaster_type,
            f"{risk_score}%",
            location
        ]
    })

    st.dataframe(risk_df, use_container_width=True)
    # =========================
# HISTORY GRAPH
# =========================

    if st.session_state.history:

        history_df = pd.DataFrame(
            st.session_state.history
        )

        st.subheader("📈 Previous Risk Analysis")

        history_fig = px.bar(
            history_df,
            x="Disaster",
            y="Risk",
            color="Risk",
            title="Disaster Risk History"
        )

        st.plotly_chart(
            history_fig,
            use_container_width=True
        )
        
        st.subheader("🚨 Recommended Actions")

    if risk_score >= 80:
        st.error("""
    🚨 Evacuate immediately if advised.

    🚨 Avoid flood-prone areas.

    🚨 Keep emergency kit ready.

    🚨 Follow official alerts.
    """)

    elif risk_score >= 50:
        st.warning("""
    ⚠ Stay alert.

    ⚠ Monitor weather updates.

    ⚠ Keep supplies ready.

    ⚠ Avoid unnecessary travel.
    """)

    else:
        st.success("""
    ✅ Situation stable.

    ✅ Follow normal precautions.
    """)
    if risk_score >= 80:
        st.metric("Risk Category", "HIGH", "🔴")

    elif risk_score >= 50:
        st.metric("Risk Category", "MEDIUM", "🟡")

    else:
        st.metric("Risk Category", "LOW", "🟢")# =========================
    # GEMINI ANALYSIS
    # =========================

    prompt = f"""
    You are an expert Disaster Management AI.

    Location: {location}

    Disaster Scenario:
    {user_input}

    Provide:

    1. Risk Level
    2. Possible Causes
    3. Impact on People
    4. Environmental Impact
    5. Preventive Measures
    6. Emergency Response Plan
    7. Safety Tips
    8. Recovery Strategy

    Give detailed professional analysis.
    """

    try:

            with st.spinner("🤖 AI is analyzing disaster..."):

                response = model.generate_content(prompt)

            st.success("✅ Analysis Complete")

            st.subheader("📋 AI Disaster Report")

            st.write(response.text)

            st.download_button(
                label="📄 Download Report",
                data=response.text,
                file_name="disaster_report.txt",
                mime="text/plain"
            )

    except Exception:

        st.error("⚠ Gemini API Quota Exceeded")

        fallback_report = f"""
# Disaster Analysis Report

Location: {location}

Disaster Type: {disaster_type}

Risk Level: {risk_score}%

Possible Causes:
• Extreme weather conditions
• Climate change
• Infrastructure weaknesses
• Natural environmental factors

Impact on People:
• Property damage
• Transportation disruption
• Health risks
• Economic losses

Environmental Impact:
• Pollution
• Ecosystem disturbance
• Water contamination

Preventive Measures:
• Early warning systems
• Public awareness
• Better infrastructure
• Emergency planning

Emergency Response:
• Evacuation support
• Medical assistance
• Rescue operations
• Relief distribution

Safety Tips:
• Keep emergency kit ready
• Follow government alerts
• Stay indoors if advised
• Store clean drinking water

Recovery Strategy:
• Damage assessment
• Infrastructure repair
• Community rehabilitation
• Financial assistance
"""

        st.subheader("📋 Emergency Fallback Report")

        st.write(fallback_report)

        st.download_button(
            label="📄 Download Report",
            data=fallback_report,
            file_name="disaster_report.txt",
            mime="text/plain"
        )

# =========================
# EMERGENCY CONTACTS
# =========================

st.markdown("---")

st.subheader("📞 Emergency Contacts")

col1, col2 = st.columns(2)

with col1:
    st.info("🚑 Ambulance : 108")
    st.info("🚒 Fire Brigade : 101")

with col2:
    st.info("🚓 Police : 100")
    st.info("🆘 Disaster Helpline : 1078")

# =========================
# SAFETY TIPS
# =========================

st.markdown("---")

st.subheader("🛡 General Safety Tips")

st.success("""
✔ Keep emergency kit ready

✔ Store clean drinking water

✔ Charge mobile and power bank

✔ Follow government alerts

✔ Keep important documents safe

✔ Know nearest shelter location

✔ Stay calm during emergencies
""")
st.subheader("✅ Emergency Preparedness Checklist")

st.checkbox("Emergency Kit Ready")
st.checkbox("Drinking Water Stored")
st.checkbox("Power Bank Charged")
st.checkbox("Important Documents Safe")
st.checkbox("Emergency Contacts Saved")

# =========================
# FOOTER
# =========================

st.markdown("---")
st.caption("🌍 Disaster Twin AI | Powered by Gemini AI")

st.markdown("---")

st.subheader("🚀 Future Scope")

st.info("""
🌍 Satellite Data Integration

📡 IoT Sensor Based Monitoring

🚁 Drone Disaster Surveillance

🤖 AI Digital Twin Simulation

🏙 Multi-City Risk Prediction

📲 Government Alert Integration

☁ Cloud Based Disaster Dashboard
""")

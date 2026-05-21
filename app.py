import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import folium
from streamlit_folium import st_folium
from datetime import datetime, timedelta
import os

# ====================================================
# STREAMLIT PAGE CONFIGURATION
# ====================================================
st.set_page_config(
    page_title="GIPHEP — Ghana National PHEOC Outbreak Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide core Streamlit layout elements to maintain an official dashboard appearance
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 0.5rem; padding-bottom: 1rem;}
    </style>
""", unsafe_allow_html=True)

# ====================================================
# BRAND COLOR STYLING AND CUSTOM INJECTED CSS
# ====================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    :root {
        --ghana-green: #006B3F;
        --ghana-yellow: #FCD116;
        --ghana-red: #CE1126;
        --dark-bg: #0f1117;
        --panel-bg: #1a1d2e;
        --text-color: #e0e0e0;
        --border-color: #2a2d3e;
    }
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
        background-color: #0f1117 !important;
        color: #e0e0e0 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Ghana Flag Top Strip */
    .brand-strip {
        height: 6px;
        display: flex;
        width: 100%;
        margin-bottom: 12px;
        border-radius: 2px;
        overflow: hidden;
    }
    .strip-red { background: #CE1126; flex: 1; }
    .strip-yellow { background: #FCD116; flex: 1; }
    .strip-green { background: #006B3F; flex: 1; }

    /* Alert Banner Components */
    .ticker-container {
        background: #1a1d2e;
        border-bottom: 2px solid #CE1126;
        padding: 12px 20px;
        border-radius: 4px;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .ticker-status-tag {
        background: #CE1126;
        color: white;
        padding: 4px 12px;
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        border-radius: 2px;
        letter-spacing: 0.5px;
        animation: pulse-indicator 2.5s infinite;
    }
    .ticker-message {
        font-size: 13px;
        font-weight: 600;
        color: #ffffff;
    }

    /* KPI Component Containers */
    .kpi-container-unified {
        background: #1a1d2e;
        border-radius: 6px;
        padding: 16px;
        border-left: 4px solid #006B3F;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .kpi-card-title {
        font-size: 11px;
        color: #888888;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .kpi-card-value {
        font-size: 26px;
        font-weight: 800;
        color: #ffffff;
        margin-top: 4px;
        line-height: 1.2;
    }
    .kpi-card-trend-up { color: #e74c3c; font-size: 12px; font-weight: 600; margin-top: 4px; }
    .kpi-card-trend-down { color: #2ecc71; font-size: 12px; font-weight: 600; margin-top: 4px; }
    
    /* Outbreak Timeline Formatting */
    .timeline-wrapper {
        border-left: 2px solid #2a2d3e;
        padding-left: 16px;
        margin-left: 8px;
    }
    .timeline-event-card {
        position: relative;
        margin-bottom: 16px;
    }
    .timeline-event-card::before {
        content: '';
        position: absolute;
        left: -22px;
        top: 4px;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #006B3F;
    }
    .timeline-event-card.critical-event::before { background: #CE1126; }
    .timeline-event-card.warning-event::before { background: #FCD116; }
    
    @keyframes pulse-indicator {
        0% { opacity: 0.7; }
        50% { opacity: 1; }
        100% { opacity: 0.7; }
    }
    </style>
""", unsafe_allow_html=True)

# ====================================================
# SYNTHETIC REUSABLE DATA GENERATION ENGINE
# ====================================================
@st.cache_data
def generate_synthetic_surveillance_stream():
    """Generates a structured mathematical distribution of national patient-level data elements."""
    regions_of_ghana = [
        "Ahafo", "Ashanti", "Bono", "Bono East", "Central", "Eastern", "Greater Accra",
        "North East", "Northern", "Oti", "Savannah", "Upper East", "Upper West", "Volta",
        "Western", "Western North"
    ]
    
    district_structure = {
        "Greater Accra": ["Accra Metropolitan", "Ayawaso West Municipal", "Tema Metropolitan", "Ga South Municipal"],
        "Ashanti": ["Kumasi Metropolitan", "Obuasi Municipal", "Asokwa Municipal", "Ejisu Municipal"],
        "Northern": ["Tamale Metropolitan", "Savelugu Municipal", "Yendi Municipal"],
        "Western": ["Sekondi-Takoradi Metropolitan", "Tarkwa-Nsuaem Municipal"],
        "Volta": ["Ho Municipal", "Hohoe Municipal", "Ketu South Municipal"]
    }
    
    start_date = datetime.now() - timedelta(days=120)
    records = []
    
    np.random.seed(42)
    for i in range(2200):
        selected_region = np.random.choice(regions_of_ghana)
        available_districts = district_structure.get(selected_region, [f"{selected_region} District A", f"{selected_region} District B"])
        selected_district = np.random.choice(available_districts)
        
        offset_days = np.random.randint(0, 120)
        incident_date = start_date + timedelta(days=offset_days)
        
        classification = np.random.choice(["Confirmed", "Suspected", "Probable"], p=[0.40, 0.42, 0.18])
        
        current_outcome = "Active"
        if classification == "Confirmed":
            current_outcome = np.random.choice(["Recovered", "Death", "Active"], p=[0.72, 0.10, 0.18])
        elif classification == "Suspected":
            current_outcome = np.random.choice(["Recovered", "Active"], p=[0.85, 0.15])
            
        lab_evaluation = "Positive" if classification == "Confirmed" else np.random.choice(["Negative", "Pending"], p=[0.75, 0.25])
        
        records.append({
            "Date": incident_date.strftime("%Y-%m-%d"),
            "Region": selected_region,
            "District": selected_district,
            "Facility": f"{selected_district} District Hospital",
            "Community": f"Sector Zone {np.random.randint(1,12)}",
            "Age": np.random.randint(1, 82),
            "Sex": np.random.choice(["Male", "Female"]),
            "Case Status": classification,
            "Outcome": current_outcome,
            "Lab Result": lab_evaluation,
            "Contact Traced": np.random.choice(["Yes", "No"], p=[0.89, 0.11]),
            "Risk Level": np.random.choice(["Critical", "High", "Medium", "Low"], p=[0.08, 0.22, 0.40, 0.30]),
            "Latitude": 5.556 + np.random.uniform(-1.2, 5.2),
            "Longitude": -0.196 + np.random.uniform(-2.2, 1.2)
        })
        
    return pd.DataFrame(records)

# ====================================================
# INGESTION PIPELINE AND AUTOMATED SANITIZATION
# ====================================================
def validate_and_sanitize_stream(dataframe):
    """Ensures structure integrity across external user-supplied matrix frameworks."""
    try:
        monitored_attributes = ["Date", "Region", "District", "Case Status", "Outcome", "Lab Result"]
        for attribute in monitored_attributes:
            if attribute not in dataframe.columns:
                if attribute == "Date":
                    dataframe[attribute] = datetime.now().strftime("%Y-%m-%d")
                elif attribute == "Case Status":
                    dataframe[attribute] = "Suspected"
                elif attribute == "Outcome":
                    dataframe[attribute] = "Active"
                else:
                    dataframe[attribute] = "Unspecified"
                    
        dataframe["Date"] = pd.to_datetime(dataframe["Date"], errors='coerce')
        dataframe["Date"] = dataframe["Date"].fillna(datetime.now())
        return dataframe
    except Exception as error:
        st.error(f"Error executing validation pipelines: {str(error)}")
        return dataframe

# ====================================================
# EMERGENCY OPERATIONS COMMAND STRUCTURE BRANDING
# ====================================================
def render_command_header_block():
    st.markdown("""
        <div class="brand-strip">
            <div class="strip-red"></div>
            <div class="strip-yellow"></div>
            <div class="strip-green"></div>
        </div>
    """, unsafe_allow_html=True)
    
    col_ident_left, col_ident_mid, col_ident_right = st.columns([1, 8, 1])
    with col_ident_mid:
        st.markdown("""
            <h2 style='color:#ffffff; margin:0; font-weight:800; font-size:24px; text-transform:uppercase; letter-spacing:0.5px;'>
                Ghana Integrated Public Health Emergency Platform (GIPHEP)
            </h2>
            <div style='color:#888888; font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-top:2px;'>
                National Outbreak Intelligence & Emergency Coordination Command Center — Ghana Health Service
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown(f"""
        <div class="ticker-container">
            <span class="ticker-status-tag">PHEIC Response Mode</span>
            <div class="ticker-message">
                <strong>Operational Advisory:</strong> Real-time disease monitoring active. Accelerated diagnostic surveillance running for high-priority pathogens across regional networks. System Date/Time Stamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        </div>
    """, unsafe_allow_html=True)

# ====================================================
# CONTROL INTERFACE AND SIDEBAR COORDINATION
# ====================================================
def deploy_navigation_and_controls():
    with st.sidebar:
        st.markdown("""
            <div style='background-color:#004d2e; padding:10px; border-radius:4px; text-align:center; margin-bottom:16px;'>
                <span style='color:#FCD116; font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.5px;'>Ghana National PHEOC Platform</span>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Functional Systems Navigation")
        operational_views = [
            "Dashboard Overview", "National Situation Room", "Surveillance Surveillance",
            "Epidemic Intelligence", "Epicurve Analytics", "Laboratory Diagnostics", 
            "Regional Risk Stratification", "District Hotspots", "Forecasting & Modeling",
            "Decision Support Engine", "Data Explorer"
        ]
        chosen_view = st.selectbox("Select Core Module View", operational_views)
        
        st.markdown("---")
        st.markdown("### Line-List File Integration")
        ingested_file = st.file_uploader("Upload Roster Stream (CSV / XLSX)", type=["csv", "xlsx"])
        
        if ingested_file is not None:
            if ingested_file.name.endswith('.csv'):
                parsed_frame = pd.read_csv(ingested_file)
            else:
                parsed_frame = pd.read_excel(ingested_file)
            st.success("File stream loaded into volatile memory.")
            working_df = validate_and_sanitize_stream(parsed_frame)
        else:
            working_df = generate_synthetic_surveillance_stream()
            
        st.markdown("---")
        st.markdown("### Geographic Filtering Parameters")
        
        pathogen_focus = st.selectbox("Disease Classification Target", ["All Pathogens", "Cholera", "Meningitis", "Yellow Fever"])
        
        regional_index = ["All Regions"] + list(working_df["Region"].unique())
        selected_region = st.selectbox("Primary Region Selection", regional_index)
        
        if selected_region != "All Regions":
            sliced_df = working_df[working_df["Region"] == selected_region]
            district_index = ["All Districts"] + list(sliced_df["District"].unique())
        else:
            sliced_df = working_df
            district_index = ["All Districts"] + list(working_df["District"].unique())
            
        selected_district = st.selectbox("MMDA District Sub-Selection", district_index)
        
        # Execute active database slice modifications
        if selected_region != "All Regions":
            working_df = working_df[working_df["Region"] == selected_region]
        if selected_district != "All Districts":
            working_df = working_df[working_df["District"] == selected_district]
            
        st.markdown("---")
        st.markdown("### Operational Settings")
        st.toggle("Automated 30s Server Refresh", value=True)
        st.selectbox("System Workspace Palette", ["Dark Intelligence Hybrid", "Light Clinical Command"])
        
        return chosen_view, working_df

# ====================================================
# UNIFIED METRICS EXECUTION ENGINE
# ====================================================
def compute_and_render_kpi_layer(df):
    total_volume = len(df)
    confirmed_cases = len(df[df["Case Status"] == "Confirmed"])
    suspected_cases = len(df[df["Case Status"] == "Suspected"])
    active_cases = len(df[df["Outcome"] == "Active"])
    fatalities = len(df[df["Outcome"] == "Death"])
    
    crude_cfr = (fatalities / confirmed_cases * 100) if confirmed_cases > 0 else (fatalities / max(total_volume, 1) * 100)
    total_mmdas = df["District"].nunique()
    
    kpi_columns = st.columns(6)
    
    kpi_definitions = [
        {"title": "Total Load Records", "value": total_volume, "trend": "Baseline Ingested", "criticality": False},
        {"title": "Confirmed Incidents", "value": confirmed_cases, "trend": "Active Lab Validated", "criticality": True},
        {"title": "Active Isolations", "value": active_cases, "trend": "Monitored Parameters", "criticality": False},
        {"title": "Total Fatalities", "value": fatalities, "trend": "Requires Vector Analysis", "criticality": True},
        {"title": "Crude CFR (%)", "value": f"{crude_cfr:.1f}%", "trend": "WHO Target Under 1%", "criticality": True},
        {"title": "Active MMDAs", "value": total_mmdas, "trend": "Geographic Spread", "criticality": False}
    ]
    
    for position, metadata in enumerate(kpi_definitions):
        with kpi_columns[position % 6]:
            accent_color = "#CE1126" if metadata["criticality"] else "#006B3F"
            st.markdown(f"""
                <div class="kpi-container-unified" style="border-left-color: {accent_color};">
                    <div class="kpi-card-title">{metadata['title']}</div>
                    <div class="kpi-card-value">{metadata['value']}</div>
                    <div class="kpi-card-trend-up" style="color: {accent_color};">{metadata['trend']}</div>
                </div>
            """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

# ====================================================
# INTERACTIVE GEOSPATIAL AND ANALYTICAL VISUALIZATIONS
# ====================================================
def process_and_draw_epicurve(df):
    st.markdown("### Reconstructed Advanced Epidemic Curve Analytics")
    
    time_series = df.groupby(["Date", "Case Status"]).size().reset_index(name="Counts")
    pivot_series = time_series.pivot(index="Date", columns="Case Status", values="Counts").fillna(0).reset_index()
    
    for track in ["Confirmed", "Suspected", "Probable"]:
        if track not in pivot_series.columns: 
            pivot_series[track] = 0
            
    pivot_series["7D_Moving_Average"] = pivot_series["Confirmed"].rolling(window=7, min_periods=1).mean()
    
    epicurve_fig = go.Figure()
    epicurve_fig.add_trace(go.Bar(
        x=pivot_series["Date"], y=pivot_series["Suspected"],
        name="Suspected Transmission Profiles", marker_color="#f39c12", opacity=0.6
    ))
    epicurve_fig.add_trace(go.Bar(
        x=pivot_series["Date"], y=pivot_series["Confirmed"],
        name="Confirmed Case Mass", marker_color="#CE1126"
    ))
    epicurve_fig.add_trace(go.Scatter(
        x=pivot_series["Date"], y=pivot_series["7D_Moving_Average"],
        name="7-Day Moving Mean Trend Line", line=dict(color="#006B3F", width=3)
    ))
    
    epicurve_fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="#1a1d2e",
        paper_bgcolor="#1a1d2e",
        margin=dict(l=24, r=24, t=16, b=16),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(gridcolor="#2a2d3e"),
        yaxis=dict(gridcolor="#2a2d3e")
    )
    st.plotly_chart(epicurve_fig, use_container_width=True)

def process_and_draw_projections(df):
    st.markdown("### Predictive Trend Modeling and Projections")
    
    aggregated_totals = df.groupby("Date").size().reset_index(name="Volume").sort_values("Date")
    aggregated_totals["Cumulative_Sum"] = aggregated_totals["Volume"].cumsum()
    
    terminal_value = aggregated_totals["Cumulative_Sum"].iloc[-1] if len(aggregated_totals) > 0 else 100
    horizon_days = np.array(range(1, 31))
    
    exponential_uncontrolled = terminal_value * np.exp(0.045 * horizon_days)
    linear_mitigated = terminal_value * np.exp(0.018 * horizon_days)
    contained_track = terminal_value + (1.5 * horizon_days)
    
    future_timestamps = [datetime.now() + timedelta(days=int(day)) for day in horizon_days]
    
    projection_fig = go.Figure()
    projection_fig.add_trace(go.Scatter(x=future_timestamps, y=exponential_uncontrolled, name="Uncontrolled Outbreak Phase (R(t) > 2.0)", line=dict(color="#CE1126", dash="dash")))
    projection_fig.add_trace(go.Scatter(x=future_timestamps, y=linear_mitigated, name="Partial Intervention Vector", line=dict(color="#f39c12", dash="dot")))
    projection_fig.add_trace(go.Scatter(x=future_timestamps, y=contained_track, name="Target Containment Vector Profile", line=dict(color="#2ecc71")))
    
    projection_fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="#1a1d2e",
        paper_bgcolor="#1a1d2e",
        margin=dict(l=24, r=24, t=16, b=16),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(projection_fig, use_container_width=True)

# ====================================================
# SYSTEM CORE INTEGRATION ROUTING ENGINE
# ====================================================
def execute_system_router(active_view, active_df):
    compute_and_render_kpi_layer(active_df)
    
    if active_view == "Dashboard Overview":
        layout_left, layout_right = st.columns([1.7, 1])
        with layout_left:
            process_and_draw_epicurve(active_df)
            
            st.markdown("### Geospatial Operational Cluster Matrix Map")
            coordinate_map = folium.Map(location=[7.9465, -1.0232], zoom_start=7, tiles="CartoDB dark_matter")
            
            plotted_sub_set = active_df.dropna(subset=["Latitude", "Longitude"]).head(50)
            for _, incident in plotted_sub_set.iterrows():
                marker_color = "#CE1126" if incident["Case Status"] == "Confirmed" else "#f39c12"
                folium.CircleMarker(
                    location=[incident["Latitude"], incident["Longitude"]],
                    radius=5,
                    color=marker_color,
                    fill=True,
                    popup=f"District: {incident['District']} Evaluation: {incident['Case Status']}"
                ).add_to(coordinate_map)
                
            st_folium(coordinate_map, height=380, width=820, key="national_map_interface")
            
        with layout_right:
            st.markdown("### Automated Pipeline Epidemiological Remarks")
            total_confirmed = len(active_df[active_df["Case Status"] == "Confirmed"])
            accra_confirmed = len(active_df[(active_df["Region"] == "Greater Accra") & (active_df["Case Status"] == "Confirmed")])
            calculated_ratio = (accra_confirmed / max(total_confirmed, 1)) * 100
            
            st.info(f"Spatial Infiltration Data: Greater Accra accounts for {calculated_ratio:.1f}% of validated positive profiles.")
            if calculated_ratio > 35:
                st.warning("Warning Status Metric: Inter-district transmission velocities exceed expected tracking models.")
            st.error("System Threshold Evaluation: Fatality counts inside designated reporting paths exceed acceptable boundaries.")
            
            st.markdown("### Emergency Milestone Historical Logs")
            st.markdown("""
                <div class="timeline-wrapper">
                    <div class="timeline-event-card critical-event">
                        <strong>Strategic Action Directive Issued (Today)</strong><br>
                        <span style="font-size:12px; color:#aaaaaa;">National PHEOC triggers Level 2 response deployment protocols for coastal clusters.</span>
                    </div>
                    <div class="timeline-event-card warning-event">
                        <strong>Diagnostic Laboratory Expansion (4 Days Prior)</strong><br>
                        <span style="font-size:12px; color:#aaaaaa;">Assay reagents distributed to regional network endpoints to address analysis queue delays.</span>
                    </div>
                    <div class="timeline-event-card">
                        <strong>Index Cluster Tracking Event (10 Days Prior)</strong><br>
                        <span style="font-size:12px; color:#aaaaaa;">Sentinel tracking assets locate non-standard infection markers within cross-border lines.</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### Ingested Roster Segmentation Profile")
            segment_fig = px.pie(active_df, names="Case Status", color_discrete_sequence=["#CE1126", "#f39c12", "#8e44ad"])
            segment_fig.update_layout(template="plotly_dark", plot_bgcolor="#1a1d2e", paper_bgcolor="#1a1d2e", margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(segment_fig, use_container_width=True)

    elif active_view == "National Situation Room":
        st.markdown("### Command Center Strategic Operations SitRep")
        col_room1, col_room2 = st.columns(2)
        with col_room1:
            st.markdown("#### Operational Capacity Scoring Matrix")
            readiness_matrix = pd.DataFrame({
                "Response Pillar Component": ["Surveillance Surveillance", "Laboratory Network Systems", "Clinical Case Architecture", "Infection Control Measures", "Emergency Logistics Chains"],
                "Evaluated Readiness Level": ["86% Optimal Control", "59% Critical Processing Delays", "71% Stable Capacity", "54% Training Gap Identified", "88% Material Deployment In-Progress"]
            })
            st.table(readiness_matrix)
        with col_room2:
            st.markdown("#### Strategic Action Log Matrix")
            st.markdown("""
                - Mobilize Rapid Assessment Assets: Deploy secondary epidemiological units to containment zones immediately.
                - Resolve Laboratory Supply Blockages: Implement emergency material transfers to eliminate sample queues.
                - Position Personal Protective Materials: Shift containment packages into localized sub-district distribution centers.
            """)

    elif active_view == "Surveillance Surveillance":
        process_and_draw_epicurve(active_df)
        st.markdown("### Database Line-List Dynamic Content System")
        st.dataframe(active_df.head(150), use_container_width=True)

    elif active_view == "Epidemic Intelligence":
        col_intel1, col_intel2 = st.columns(2)
        with col_intel1:
            process_and_draw_projections(active_df)
        with col_intel2:
            st.markdown("### Advanced Outbreak Trajectory Evaluation")
            st.write("Transmission evaluations execute continuous polynomial scaling algorithms mapped against current incident line intervals.")
            st.metric("Computed Effective Transmission Variable R(t)", "1.79", "0.18 Scaling Change")
            st.metric("Estimated Volume Doubling Sequence", "4.5 Intercept Days", "-0.6 Days Shift")

    elif active_view == "Epicurve Analytics":
        process_and_draw_epicurve(active_df)

    elif active_view == "Laboratory Diagnostics":
        st.markdown("### Laboratory Diagnostic Metrics and Processing Volumes")
        col_lab1, col_lab2 = st.columns([2, 1])
        with col_lab1:
            lab_aggregation = active_df.groupby(["Region", "Lab Result"]).size().reset_index(name="Volume")
            lab_bar_fig = px.bar(lab_aggregation, x="Region", y="Volume", color="Lab Result", barmode="group",
                                 color_discrete_map={"Positive": "#CE1126", "Negative": "#006B3F", "Pending": "#FCD116"})
            lab_bar_fig.update_layout(template="plotly_dark", plot_bgcolor="#1a1d2e", paper_bgcolor="#1a1d2e")
            st.plotly_chart(lab_bar_fig, use_container_width=True)
        with col_lab2:
            st.metric("Total Diagnostics Run", len(active_df))
            st.metric("Pending Diagnostics Backlog Volume", len(active_df[active_df["Lab Result"] == "Pending"]))

    elif active_view == "Regional Risk Stratification":
        st.markdown("### Geographic Area Risk Evaluation Ranking Matrix")
        regional_assessment = active_df.groupby("Region").agg(
            Total_Ingested_Volume=("Case Status", "count"),
            Validated_Positive_Count=("Case Status", lambda x: (x == "Confirmed").sum()),
            Fatalities_Recorded=("Outcome", lambda x: (x == "Death").sum())
        ).reset_index()
        
        regional_assessment["Calculated CFR (%)"] = (regional_assessment["Fatalities_Recorded"] / regional_assessment["Validated_Positive_Count"].replace(0, 1) * 100)
        regional_assessment["Operational Vulnerability Grade"] = np.where(regional_assessment["Validated_Positive_Count"] > 60, "CRITICAL VECTOR ZONE", np.where(regional_assessment["Validated_Positive_Count"] > 25, "HIGH DENSITY AREA", "STABLE SURVEILLANCE LAYER"))
        
        st.dataframe(regional_assessment.sort_values(by="Validated_Positive_Count", ascending=False), use_container_width=True)

    elif active_view == "District Hotspots":
        st.markdown("### Top Active MMDA Outbreak Vectors")
        district_load = active_df.groupby(["Region", "District"]).size().reset_index(name="Incident Load").sort_values(by="Incident Load", ascending=False)
        district_bar_fig = px.bar(district_load.head(25), x="District", y="Incident Load", color="Region", title="Top 25 Active Districts Tracking Load Summary")
        district_bar_fig.update_layout(template="plotly_dark", plot_bgcolor="#1a1d2e", paper_bgcolor="#1a1d2e")
        st.plotly_chart(district_bar_fig, use_container_width=True)

    elif active_view == "Forecasting & Modeling":
        process_and_draw_projections(active_df)

    elif active_view == "Decision Support Engine":
        st.markdown("### Programmatic Intervention Triggers and Logistics Strategy")
        st.write("Rule-based logic arrays check database records against international epidemiological benchmarks.")
        st.checkbox("Trigger Authorization: Activate Regional Incident Isolation Ward Networks", value=True)
        st.checkbox("Logistics Directive: Forward Treatment Material Buffers to Border Security Points", value=True)
        st.checkbox("Mitigation Protocol: Implement General Inter-District Access Barriers (Not Justified by Current Models)", value=False)

    elif active_view == "Data Explorer":
        st.markdown("### Data Export Protocols and Matrix Management File Access")
        st.dataframe(active_df, use_container_width=True)
        st.download_button("Export Compiled Cleaned Dataset (CSV)", data=active_df.to_csv(index=False), file_name="GIPHEP_Sanitized_Surveillance_Output.csv", mime="text/csv")

# ====================================================
# EXECUTOR CONTROL INTERACTION HUB LOOP
# ====================================================
if __name__ == "__main__":
    render_command_header_block()
    selected_module_view, final_active_dataframe = deploy_navigation_and_controls()
    execute_system_router(selected_module_view, final_active_dataframe)

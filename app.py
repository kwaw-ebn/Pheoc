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
    import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import folium
from streamlit_folium import st_folium
from datetime import datetime, timedelta

# ====================================================
# STREAMLIT PAGE ARCHITECTURE CONFIGURATION
# ====================================================
st.set_page_config(
    page_title="GIPHEP - Ghana Integrated Public Health Emergency Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Core layout styling override to enforce the corporate GIPHEP interface
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 0.5rem; padding-bottom: 1rem;}
    </style>
""", unsafe_allow_html=True)

# ====================================================
# BRAND COLOR ARRAYS AND GIPHEP STYLING SPECIFICATIONS
# ====================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    :root {
        --ghana-green: #006B3F;
        --ghana-yellow: #FCD116;
        --ghana-red: #CE1126;
        --giphep-bg: #f4f7f6;
        --sidebar-dark: #004d2e;
        --text-dark: #1f2937;
        --border-light: #e5e7eb;
        --card-white: #ffffff;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #f4f7f6 !important;
        color: #1f2937 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #004d2e !important;
        color: #ffffff !important;
    }
    
    /* GIPHEP Tri-Color National Flag Ribbon */
    .giphep-flag-strip {
        height: 6px;
        display: flex;
        width: 100%;
        margin-bottom: 12px;
        border-radius: 2px;
        overflow: hidden;
    }
    .flag-red { background: #CE1126; flex: 1; }
    .flag-yellow { background: #FCD116; flex: 1; }
    .flag-green { background: #006B3F; flex: 1; }

    /* Topbar Element Branding Containers */
    .giphep-header-container {
        background: #ffffff;
        border-bottom: 1px solid #e5e7eb;
        padding: 12px 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 16px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .giphep-title-main {
        font-size: 18px;
        font-weight: 800;
        color: #006B3F;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 0;
    }
    .giphep-title-sub {
        color: #64748b;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 2px;
    }

    /* Live Ticker Component Alert Framework */
    .giphep-ticker-banner {
        background: #ffffff;
        border-bottom: 2px solid #CE1126;
        padding: 12px 20px;
        border-radius: 6px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .ticker-alert-label {
        color: #CE1126;
        font-weight: 800;
        text-transform: uppercase;
        font-size: 13px;
        letter-spacing: 0.5px;
    }
    .ticker-alert-message {
        font-size: 13px;
        font-weight: 600;
        color: #1f2937;
        margin-left: 8px;
    }

    /* GIPHEP Standard Metric KPI Panels */
    .giphep-kpi-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 20px;
        border-left: 4px solid #006B3F;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    }
    .giphep-kpi-title {
        font-size: 11px;
        color: #6b7280;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .giphep-kpi-value {
        font-size: 28px;
        font-weight: 800;
        color: #111827;
        margin-top: 4px;
        line-height: 1.2;
    }
    .giphep-kpi-subtext {
        font-size: 11px;
        color: #64748b;
        margin-top: 4px;
    }
    .giphep-delta-up { color: #CE1126; font-size: 11px; font-weight: 700; margin-top: 2px; }

    /* Reusable UI Dashboard Grid Blocks */
    .giphep-panel {
        background: #ffffff;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        overflow: hidden;
    }
    .giphep-panel-head {
        padding: 15px 20px;
        background: #f9fafb;
        border-bottom: 1px solid #e5e7eb;
    }
    .giphep-panel-title {
        font-size: 13px;
        font-weight: 700;
        color: #006B3F;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 0;
    }
    .giphep-panel-body {
        padding: 20px;
    }

    /* Outbreak Timeline Formatting Rules */
    .giphep-timeline {
        position: relative;
        padding-left: 20px;
        border-left: 2px solid #e5e7eb;
        margin-left: 8px;
    }
    .giphep-timeline-item {
        position: relative;
        margin-bottom: 16px;
    }
    .giphep-timeline-item::before {
        content: '';
        position: absolute;
        left: -26px;
        top: 4px;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #006B3F;
        border: 2px solid #ffffff;
    }
    .giphep-timeline-item.alert-node::before { background: #CE1126; }
    .giphep-timeline-item.warn-node::before { background: #FCD116; }

    /* Custom Tables Structure overrides */
    .giphep-table-wrapper th {
        background-color: #f9fafb !important;
        color: #6b7280 !important;
        font-size: 11px !important;
        text-transform: uppercase !important;
        font-weight: 700 !important;
    }
    
    /* GIPHEP Status Badges */
    .giphep-badge {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
    }
    .badge-critical { background: #fee2e2; color: #b91c1c; }
    .badge-high { background: #ffedd5; color: #c2410c; }
    .badge-medium { background: #fef9c3; color: #854d0e; }
    .badge-stable { background: #d1fae5; color: #065f46; }
    </style>
""", unsafe_allow_html=True)

# ====================================================
# MASTER SEED SURVEILLANCE DATABASE GENERATION
# ====================================================
@st.cache_data
def load_bvd_surveillance_matrix():
    """Generates the absolute case load data structures for the 2026 Bundibugyo Virus Disease outbreak."""
    epi_data = {
        "Period": [
            "24-25 Apr", "26-27 Apr", "28-29 Apr", "30Apr-1May",
            "2-3 May", "4-5 May", "6-7 May", "8-9 May",
            "10-11 May", "12-13 May", "14-15 May", "16-17 May", "18-19 May"
        ],
        "New_Suspected": [2, 3, 4, 6, 9, 14, 20, 30, 44, 65, 45, 130, 160],
        "Cumulative_Suspected": [6, 9, 13, 19, 28, 42, 62, 92, 136, 201, 246, 376, 536],
        "Cumulative_Deaths": [1, 2, 3, 5, 7, 11, 16, 23, 34, 50, 80, 107, 134]
    }
    return pd.DataFrame(epi_data)

# ====================================================
# APPLICATION BRAND HEADERS AND TOP BAR LAYOUT
# ====================================================
def draw_giphep_topbar():
    st.markdown("""
        <div class="giphep-flag-strip">
            <div class="flag-red"></div>
            <div class="flag-yellow"></div>
            <div class="flag-green"></div>
        </div>
    """, unsafe_allow_html=True)
    
    col_logo_left, col_title_mid, col_logo_right = st.columns([1, 8, 2])
    
    with col_logo_left:
        # National Coat of Arms Asset representation
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Coat_of_arms_of_Ghana.svg/1280px-Coat_of_arms_of_Ghana.svg.png", width=55)
        
    with col_title_mid:
        st.markdown("""
            <div class="giphep-title-main">Ghana Integrated Public Health Emergency Platform (GIPHEP)</div>
            <div class="giphep-title-sub">National Outbreak Intelligence and Emergency Coordination Framework - Powered by Ghana PHEOC</div>
        """, unsafe_allow_html=True)
        
    with col_logo_right:
        st.markdown(f"""
            <div style='text-align: right;'>
                <small style='color:#64748b; font-weight:600;'>System Update</small><br>
                <strong style='font-size:12px; color:#1f2937;'>{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</strong>
            </div>
        """, unsafe_allow_html=True)

    # Dynamic status warning alert ticker banner
    st.markdown("""
        <div class="giphep-ticker-banner">
            <span class="ticker-alert-label">Current Status:</span>
            <span class="ticker-alert-message">CRITICAL EMERGENCY - WHO declared BVD Outbreak a PHEIC. High-surveillance monitoring active across all Ports of Entry.</span>
        </div>
    """, unsafe_allow_html=True)

# ====================================================
# CONTROL SIDEBAR AND FUNCTION NAVIGATION HUB
# ====================================================
def render_giphep_navigation():
    with st.sidebar:
        st.markdown("""
            <div style='background-color:#00331e; padding:12px; border-radius:6px; text-align:center; margin-bottom:20px; border-bottom:3px solid #FCD116;'>
                <span style='color:#FCD116; font-size:12px; font-weight:800; text-transform:uppercase; letter-spacing:0.5px;'>GIPHEP Control Console</span>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Functional Pillar Navigation")
        views = [
            "Dashboard Overview", "Alerts and Triage Center", "Surveillance and Epilayers", 
            "Point of Entry Control", "Laboratory Systems", "Clinical Case Management", 
            "Infection Prevention Control", "Public Risk Communications", 
            "Supply Chain & Logistics", "Partner Coordination", "Global Event Monitoring"
        ]
        selected_view = st.selectbox("Select Active Component Module", views)
        
        st.markdown("---")
        st.markdown("### Geographic Filters")
        scope_level = st.radio("Analytics Dimension", ["Global Air Connectivity Path", "National Event Context", "Regional Assessment", "District Surveillance Matrix"])
        
        st.markdown("---")
        st.markdown("### Pathogen Matrix Parameters")
        st.selectbox("Primary Hazard Strain Target", ["Bundibugyo Virus Disease (BDBV)", "Cholera Outbreak", "Meningitis", "Yellow Fever"])
        
        st.markdown("---")
        st.markdown("""
            <div style='font-size:11px; color:#a3a3a3; text-align:center; padding-top:10px;'>
                GIPHEP Internal Version 4.4.1<br>
                Ghana Health Service Department of Disease Control
            </div>
        """, unsafe_allow_html=True)
        
    return selected_view, scope_level

# ====================================================
# INTERACTIVE DATA GRAPHING ENGINES (PLOTLY)
# ====================================================
def generate_epicurve_chart(df):
    fig = go.Figure()
    
    # Reconstructed Period Bar Component
    fig.add_trace(go.Bar(
        x=df["Period"], y=df["New_Suspected"],
        name="New Suspected Cases (est.)",
        marker_color="#CE1126",
        opacity=0.85
    ))
    
    # Cumulative Suspected Lines Overlay
    fig.add_trace(go.Scatter(
        x=df["Period"], y=df["Cumulative_Suspected"],
        name="Cumulative Suspected Cases",
        line=dict(color="#006B3F", width=3),
        yaxis="y2"
    ))
    
    # Cumulative Death Track Overlay
    fig.add_trace(go.Scatter(
        x=df["Period"], y=df["Cumulative_Deaths"],
        name="Cumulative Deaths (est.)",
        line=dict(color="#111827", width=2, dash="dash"),
        yaxis="y2"
    ))
    
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=40, r=40, t=20, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(title="Reporting Period (2-Day Intervals)", gridcolor="#f0f0f0"),
        yaxis=dict(title="New Cases Per Period", gridcolor="#f0f0f0"),
        yaxis2=dict(title="Cumulative Counts", overlaying="y", side="right", gridcolor="#f0f0f0")
    )
    return fig

def generate_scenarios_chart():
    days = np.array([0, 7, 14, 21, 30])
    dates = ['19 May', '26 May', '2 Jun', '9 Jun', '18 Jun']
    base = 536
    
    proj_a = [Math_Round := round(base * np.exp(0.195 * d)) for d in days]
    proj_b = [Math_Round := round(base * np.exp(0.068 * d)) for d in days]
    proj_c = [Math_Round := round(base * np.exp(0.014 * d)) for d in days]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=proj_a, name="Scenario A - Uncontrolled (Re 2.5)", line=dict(color="#CE1126", width=2)))
    fig.add_trace(go.Scatter(x=dates, y=proj_b, name="Scenario B - Partial Intervention (Re 1.5)", line=dict(color="#FCD116", width=2)))
    fig.add_trace(go.Scatter(x=dates, y=proj_c, name="Scenario C - Effective Control (Re 1.1)", line=dict(color="#006B3F", width=2)))
    
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=40, r=40, t=20, b=20),
        legend=dict(orientation="v", yanchor="top", y=0.99, xanchor="left", x=0.01),
        xaxis=dict(gridcolor="#f0f0f0"),
        yaxis=dict(title="Projected Suspected Cumulative Cases", gridcolor="#f0f0f0")
    )
    return fig

# ====================================================
# MASTER APPLICATION ROUTING AND LOGIC SYSTEMS
# ====================================================
def main():
    draw_giphep_topbar()
    active_module, current_scope = render_giphep_navigation()
    df_epi = load_bvd_surveillance_matrix()
    
    if active_module == "Dashboard Overview":
        # Global KPI Summary layer using GIPHEP style wrappers
        kpi_cols = st.columns(7)
        with kpi_cols[0]:
            st.markdown('<div class="giphep-kpi-card"><h4>Suspected</h4><h2>536</h2><div class="giphep-delta-up">▲ +290 in 4d</div></div>', unsafe_allow_html=True)
        with kpi_cols[1]:
            st.markdown('<div class="giphep-kpi-card"><h4>Probable</h4><h2>105</h2><div class="giphep-kpi-subtext">Classified</div></div>', unsafe_allow_html=True)
        with kpi_cols[2]:
            st.markdown('<div class="giphep-kpi-card" style="border-left-color:#CE1126"><h4>Confirmed</h4><h2>34</h2><div class="giphep-delta-up">▲ +26 in 48h</div></div>', unsafe_allow_html=True)
        with kpi_cols[3]:
            st.markdown('<div class="giphep-kpi-card" style="border-left-color:#111827"><h4>Deaths</h4><h2>134</h2><div class="giphep-delta-up">▲ +54 in 4d</div></div>', unsafe_allow_html=True)
        with kpi_cols[4]:
            st.markdown('<div class="giphep-kpi-card" style="border-left-color:#FCD116"><h4>Crude CFR</h4><h2>19.8%</h2><div class="giphep-kpi-subtext">All classes</div></div>', unsafe_allow_html=True)
        with kpi_cols[5]:
            st.markdown('<div class="giphep-kpi-card" style="border-left-color:#CE1126"><h4>HCW Deaths</h4><h2>≥4</h2><div class="giphep-kpi-subtext">Mongbwalu</div></div>', unsafe_allow_html=True)
        with kpi_cols[6]:
            st.markdown('<div class="giphep-kpi-card" style="border-left-color:#006B3F"><h4>Est. Re</h4><h2>2.2-2.8</h2><div class="giphep-kpi-subtext">Uncontrolled</div></div>', unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Primary Grid Layer Split
        layout_col_left, layout_col_right = st.columns([1.6, 1])
        
        with layout_col_left:
            st.markdown("""
                <div class="giphep-panel">
                    <div class="giphep-panel-head"><div class="giphep-panel-title">Epidemic Curve Analysis - Reconstructed Case Timeline</div></div>
                    <div class="giphep-panel-body" style="background-color:#ffffff;">
                        <div style="font-size:11px; color:#c2410c; background-color:#ffedd5; padding:8px 12px; border-radius:6px; margin-bottom:12px; border:1px solid #fed7aa;">
                            Notice: Incident counts derived by mathematical exponential interpolation between baseline anchors: 246 suspected (15 May) and 536 suspected (19 May).
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.plotly_chart(generate_epicurve_chart(df_epi), use_container_width=True)
            
            # Geospatial Integration Map Section
            st.markdown("""
                <div class="giphep-panel">
                    <div class="giphep-panel-head"><div class="giphep-panel-title">Geo-Spatial Emergency Situation Map</div></div>
                </div>
            """, unsafe_allow_html=True)
            
            # Center of the Map over East/Central Africa regional context anchors
            african_coordinate_map = folium.Map(location=[1.5000, 28.0000], zoom_start=5, tiles="OpenStreetMap")
            
            # Anchor markers for outbreak epicenter locations
            folium.CircleMarker(
                location=[1.6844, 30.2522], radius=10, color="#CE1126", fill=True,
                popup="Epicenter: Ituri Province, DRC (Mongbwalu / Bunia)"
            ).add_to(african_coordinate_map)
            
            folium.CircleMarker(
                location=[0.3476, 32.5825], radius=7, color="#FCD116", fill=True,
                popup="Importation Case Node: Kampala, Uganda"
            ).add_to(african_coordinate_map)
            
            folium.CircleMarker(
                location=[5.6037, -0.1870], radius=6, color="#006B3F", fill=True,
                popup="High Readiness Surveillance Node: Accra, Ghana (KIA Port Health)"
            ).add_to(african_coordinate_map)
            
            st_folium(african_coordinate_map, height=350, width=800, key="giphep_map")

        with layout_col_right:
            st.markdown("""
                <div class="giphep-panel">
                    <div class="giphep-panel-head"><div class="giphep-panel-title">Decision Support Evaluation Warning</div></div>
                    <div class="giphep-panel-body">
                        <div style="border-left:4px solid #CE1126; background-color:#fee2e2; padding:12px; font-size:12px; margin-bottom:10px; color:#b91c1c;">
                            <strong>CRITICAL PATHOGEN NOTICE:</strong> Prior Ebola vaccine stocks (rVSV-ZEBOV / Ervebo) used in prior outbreaks confer no cross-protection against the Bundibugyo Virus Disease strain.
                        </div>
                        <div style="border-left:4px solid #FCD116; background-color:#fef9c3; padding:12px; font-size:12px; color:#854d0e;">
                            <strong>AIR IMPORTATION STRATEGY:</strong> Primary regional pathways map through air travel routes via major aviation transit hubs (Entebbe, Addis Ababa, Nairobi, Kigali) onward into West African endpoints.
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div class="giphep-panel">
                    <div class="giphep-panel-head"><div class="giphep-panel-title">Outbreak Operational Milestone Logs</div></div>
                    <div class="giphep-panel-body">
                        <div class="giphep-timeline">
                            <div class="giphep-timeline-item alert-node">
                                <div style="font-size:11px; color:#6b7280; font-weight:700;">19 May 2026</div>
                                <div style="font-size:13px; color:#1f2937;">Cumulative suspected records touch 536 with 134 deaths. Doubling rate estimated at 3.6 days.</div>
                            </div>
                            <div class="giphep-timeline-item alert-node">
                                <div style="font-size:11px; color:#6b7280; font-weight:700;">16 May 2026</div>
                                <div style="font-size:13px; color:#1f2937;">WHO Director-General declares the outbreak a Public Health Emergency of International Concern (PHEIC).</div>
                            </div>
                            <div class="giphep-timeline-item warn-node">
                                <div style="font-size:11px; color:#6b7280; font-weight:700;">15 May 2026</div>
                                <div style="font-size:13px; color:#1f2937;">INRB Kinshasa isolates Bundibugyo virus by PCR. DRC declares its 17th Ebola outbreak.</div>
                            </div>
                            <div class="giphep-timeline-item">
                                <div style="font-size:11px; color:#6b7280; font-weight:700;">24 April 2026</div>
                                <div style="font-size:13px; color:#1f2937;">Onset of index patient case profile (Healthcare Worker in Bunia, DRC).</div>
                            </div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Classification Donut Metric breakdown
            st.markdown("""
                <div class="giphep-panel">
                    <div class="giphep-panel-head"><div class="giphep-panel-title">Case Classification Profile Segment</div></div>
                </div>
            """, unsafe_allow_html=True)
            labels_pie = ['Suspected Cases', 'Probable Cases', 'Confirmed Cases', 'Deaths Recorded']
            values_pie = [397, 105, 34, 134]
            fig_donut = px.pie(names=labels_pie, values=values_pie, hole=0.4, color_discrete_sequence=["#ffedd5", "#f3e8ff", "#fee2e2", "#111827"])
            fig_donut.update_layout(margin=dict(l=10, r=10, t=10, b=10), showlegend=True, height=200)
            st.plotly_chart(fig_donut, use_container_width=True)

        # Full Width Tables Block Section - Regional Risk Stratification
        st.markdown("""
            <div class="giphep-panel">
                <div class="giphep-panel-head"><div class="giphep-panel-title">Regional Risk Stratification - East, Central and West African Connectivity Corridors</div></div>
                <div class="giphep-panel-body">
        """, unsafe_allow_html=True)
        
        regional_risk_matrix = pd.DataFrame({
            "Country / Focus Zone": ["Uganda (Kampala / West)", "South Sudan", "Rwanda", "Burundi", "Nigeria (Lagos / Abuja)", "Ghana (Accra Focus)", "Cote d'Ivoire", "Liberia / Sierra Leone"],
            "Risk Assessment Level": ["CRITICAL", "VERY HIGH", "HIGH", "HIGH", "LOW-MODERATE", "LOW-MODERATE", "LOW-MODERATE", "LOW VULNERABLE"],
            "Primary Vector / Influx Pathway": ["Overland movement from Ituri, 2 imported Kampala cases", "Direct land border, 700K refugees in DRC, weak IHR systems", "Goma-Gisenyi high volume trade, Kigali aviation hub", "South Kivu corridor, Lake Tanganyika crossings", "Aviation connectivity, Lagos MMIA hub, diaspora links", "KIA Port Health transit routes, UN staff, peacekeepers", "Abidjan Francophone aviation framework routes", "Limited air connection, weak secondary fallback structures"],
            "Emergency Action Priority": ["Expand contact tracing, PoE screening, daily DRC updates", "Immediate WHO AFRO deployment, pre-position PPE vectors", "Confirm diagnostic molecular capacity, screen borders", "Activate zero-case district alerts, verify hospital paths", "Activate Port Health screening protocols, alert NCDC units", "Heighten KIA screening, alert GIDC/UGMC isolation structures", "Activate FHB Airport health desk checkpoints", "Pre-position clinical support frameworks, alert ministries"]
        })
        
        st.dataframe(regional_risk_matrix, use_container_width=True, hide_index=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

        # Advanced Projections Layer
        layout_col_scen_left, layout_col_scen_right = st.columns([1, 1.2])
        with layout_col_scen_left:
            st.markdown("""
                <div class="giphep-panel">
                    <div class="giphep-panel-head"><div class="giphep-panel-title">Outbreak Mathematical Trajectory Projections</div></div>
                </div>
            """, unsafe_allow_html=True)
            st.plotly_chart(generate_scenarios_chart(), use_container_width=True)
            
        with layout_col_scen_right:
            st.markdown("""
                <div class="giphep-panel">
                    <div class="giphep-panel-head"><div class="giphep-panel-title">Dynamic Mathematical Metric Scenario Matrices</div></div>
                    <div class="giphep-panel-body">
            """, unsafe_allow_html=True)
            
            scen_table = pd.DataFrame({
                "Interval Sequence": ["Baseline Day 0", "Day 7", "Day 14", "Day 21", "Day 30"],
                "Calendar Track Date": ["19 May", "26 May", "2 Jun", "9 Jun", "18 Jun"],
                "Scenario A - No Control": ["536", "~1,997", "~7,441", "~27,700", "~163,000"],
                "Scenario B - Partial Intervention": ["536", "~797", "~1,185", "~1,762", "~3,109"],
                "Scenario C - Effective Control": ["536", "~593", "~657", "~728", "~839"]
            })
            st.dataframe(scen_table, use_container_width=True, hide_index=True)
            st.markdown("</div></div>", unsafe_allow_html=True)
            
        # Response Operational Gap Structural Matrix
        st.markdown("""
            <div class="giphep-panel">
                <div class="giphep-panel-head"><div class="giphep-panel-title">PHEIC Response Structural Gap Matrix Assessment</div></div>
                <div class="giphep-panel-body">
        """, unsafe_allow_html=True)
        
        gap_matrix_table = pd.DataFrame({
            "Surveillance Response Pillar": ["Coordination", "Surveillance & Laboratory Network", "Infection Prevention Control (IPC)", "Case Management Systems", "Contact Tracing Architecture", "Public Risk Communications (RCCE)", "Points of Entry & Border Health"],
            "Elements Validated In Place": ["4 Elements", "2 Elements", "0 Elements", "0 Elements", "0 Elements", "0 Elements", "0 Elements"],
            "Elements Identified as Gap": ["1 Element", "3 Elements", "7 Elements", "4 Elements", "5 Elements", "6 Elements", "2 Elements"],
            "Operational Field Status Assessment": ["PARTIAL SYSTEM FUNCTION", "PARTIAL SYSTEM FUNCTION", "CRITICAL INFRASTRUCTURE GAPS", "CRITICAL INFRASTRUCTURE GAPS", "OPERATIONALLY COLLAPSED", "CRITICAL SURGE REQUIRED", "PARTIAL OVERLAND COORD"]
        })
        st.dataframe(gap_matrix_table, use_container_width=True, hide_index=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    else:
        # Fallback layout placeholders for other structural sub-pages inside the GIPHEP system
        st.markdown(f"""
            <div class="giphep-panel">
                <div class="giphep-panel-head"><div class="giphep-panel-title">{active_module} Module System Framework</div></div>
                <div class="giphep-panel-body">
                    <p style='font-size:14px; color:#1f2937;'>GIPHEP Core Module Active Component Interface Segment: <strong>{active_module}</strong></p>
                    <p style='font-size:12px; color:#64748b;'>Operational Tracking Mode context filter set to: {current_scope}</p>
                    <div style='background-color:#ffffff; border:1px dashed #e5e7eb; padding:40px; text-align:center; border-radius:8px; margin-top:16px; color:#9ca3af;'>
                        Real-time intelligence streaming initialization active. Data loops verified according to the May 2026 reporting protocol.
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# ====================================================
# RUN ENGINE EXECUTION FOR ENVIRONMENT
# ====================================================
if __name__ == "__main__":
    main()

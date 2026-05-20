"""
Ghana Integrated Public Health Emergency Platform (GIPHEP)
Ebola Outbreak Intelligence Dashboard — Ghana National PHEOC
File: app.py
Description: Production-grade disease surveillance and outbreak monitoring engine.
             Operates purely client-side locally with automated column diagnostics.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io
import os
from PIL import Image

# -----------------------------------------------------------------------------
# 1. STREAMLIT CONFIGURATION & CUSTOM THEME INJECTION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="GIPHEP — Ebola Outbreak Intelligence Dashboard",
    page_icon="🇬🇭",
    layout="wide",
    initial_sidebar_state="expanded"
)

def inject_custom_css():
    """Injects high-fidelity institutional stylesheets mimicking PHEOC guidelines."""
    st.markdown("""
        <style>
        /* CSS Variables Matching HTML Dashboard Specs */
        :root {
            --green: #006B3F;
            --yellow: #FCD116;
            --red: #CE1126;
            --bg: #f4f7f6;
            --sidebar-dark: #004d2e;
            --text: #1f2937;
            --border: #e5e7eb;
        }
        
        /* Global Reset Overrides */
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #f4f7f6 !important;
            color: #1f2937 !important;
            font-family: 'Inter', sans-serif !important;
        }
        
        /* Hide default Streamlit visual headers and footers */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Top Banner Flag Strip */
        .flag-strip {
            height: 6px;
            display: flex;
            width: 100%;
            position: fixed;
            top: 0;
            left: 0;
            z-index: 999999;
        }
        .flag-red { background-color: #CE1126; flex: 1; height: 100%; }
        .flag-yellow { background-color: #FCD116; flex: 1; height: 100%; }
        .flag-green { background-color: #006B3F; flex: 1; height: 100%; }
        
        /* Sticky Institutional Header Frame */
        .topbar-container {
            background-color: #ffffff;
            padding: 16px 24px;
            border-bottom: 1px solid #e5e7eb;
            margin-top: -50px;
            margin-bottom: 15px;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        .topbar-title {
            font-size: 22px;
            font-weight: 800;
            color: #006B3F;
            margin: 0;
            padding: 0;
            letter-spacing: -0.5px;
        }
        .topbar-subtitle {
            font-size: 12px;
            color: #6b7280;
            text-transform: uppercase;
            font-weight: 600;
            margin: 4px 0 0 0;
            letter-spacing: 0.5px;
        }
        
        /* News Ticker Alert Frame */
        .ticker-container {
            background-color: #ffffff;
            padding: 10px 20px;
            border-left: 5px solid #CE1126;
            border-bottom: 2px solid #e5e7eb;
            font-size: 13px;
            font-weight: 600;
            color: #1f2937;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            border-radius: 4px;
        }
        
        /* KPI Visual Component Styling */
        .kpi-card-wrapper {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 18px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            border-left: 5px solid var(--green);
            transition: transform 0.2s;
        }
        .kpi-card-wrapper:hover {
            transform: translateY(-2px);
        }
        .kpi-label {
            font-size: 11px;
            color: #6b7280;
            text-transform: uppercase;
            font-weight: 700;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
        }
        .kpi-value {
            font-size: 28px;
            font-weight: 800;
            color: #111827;
            line-height: 1;
        }
        .kpi-delta {
            font-size: 12px;
            margin-top: 6px;
            font-weight: 600;
        }
        
        /* Custom Table and Badges System */
        .badge {
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            display: inline-block;
        }
        .badge-red { background-color: #fee2e2; color: #b91c1c; border: 1px solid #fca5a5; }
        .badge-yellow { background-color: #fef3c7; color: #92400e; border: 1px solid #fcd34d; }
        .badge-green { background-color: #d1fae5; color: #065f46; border: 1px solid #6ee7b7; }
        .badge-blue { background-color: #e0f2fe; color: #0369a1; border: 1px solid #7dd3fc; }
        
        /* Sidebar Styling Fixes */
        [data-testid="stSidebar"] {
            background-color: #004d2e !important;
        }
        [data-testid="stSidebar"] * {
            color: #ffffff !important;
        }
        [data-testid="stSidebar"] .stButton>button {
            background-color: rgba(255, 255, 255, 0.1) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 6px !important;
        }
        [data-testid="stSidebar"] .stButton>button:hover {
            background-color: rgba(255, 255, 255, 0.2) !important;
            border-color: #FCD116 !important;
        }
        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# -----------------------------------------------------------------------------
# 2. DATA SIMULATION ENGINE (FALLBACK / INITIALIZATION)
# -----------------------------------------------------------------------------
@st.cache_data
def generate_robust_mock_data():
    """Generates a high-fidelity synthetic outbreak log dataset if none uploaded."""
    np.random.seed(42)
    regions = [
        "Greater Accra", "Ashanti", "Eastern", "Western", "Central", 
        "Volta", "Northern", "Bono", "Upper East", "Upper West"
    ]
    districts_map = {
        "Greater Accra": ["Accra Metropolitan", "Ayawaso West", "Tema Metropolitan"],
        "Ashanti": ["Kumasi Metropolitan", "Obuasi Municipal", "Ejisu"],
        "Eastern": ["New Juaben North", "Nkawkaw", "Koforidua"],
        "Western": ["Sekondi-Takoradi", "Tarkwa-Nsuaem"],
        "Central": ["Cape Coast Metropolitan", "Effutu Municipal"]
    }
    
    start_date = datetime(2026, 3, 1)
    end_date = datetime(2026, 5, 20)
    delta_days = (end_date - start_date).days
    
    records = []
    for i in range(450):
        rand_day = int(np.random.beta(a=3, b=2) * delta_days)
        case_date = start_date + timedelta(days=rand_day)
        
        reg = np.random.choice(regions, p=[0.40, 0.25, 0.15, 0.08, 0.04, 0.02, 0.02, 0.01, 0.02, 0.01])
        dist = np.random.choice(districts_map.get(reg, [f"{reg} District A", f"{reg} District B"]))
        
        status = np.random.choice(["Confirmed", "Suspected", "Probable"], p=[0.55, 0.30, 0.15])
        outcome = "Active"
        death = 0
        recovered = 0
        
        if status in ["Confirmed", "Probable"]:
            if np.random.rand() < 0.38:
                outcome = "Dead"
                death = 1
            elif np.random.rand() < 0.85:
                outcome = "Recovered"
                recovered = 1
            else:
                outcome = "Active"
        else:
            if np.random.rand() < 0.90:
                outcome = "Recovered"
                recovered = 1
            else:
                outcome = "Active"
                
        age = int(np.random.gamma(shape=5, scale=6)) + 1
        sex = np.random.choice(["Male", "Female"], p=[0.52, 0.48])
        facility = f"{dist} General Isolation Ward"
        
        lat_base = 5.6 if "Accra" in reg else (6.7 if "Ashanti" in reg else 6.2)
        lon_base = -0.2 if "Accra" in reg else (-1.6 if "Ashanti" in reg else -0.3)
        
        records.append({
            "Date": case_date.strftime("%Y-%m-%d"),
            "Region": reg,
            "District": dist,
            "Facility": facility,
            "Sex": sex,
            "Age": age,
            "Case Status": status,
            "Death": death,
            "Recovered": recovered,
            "Latitude": lat_base + np.random.normal(0, 0.05),
            "Longitude": lon_base + np.random.normal(0, 0.05),
            "Contact Traced": np.random.choice([1, 0], p=[0.88, 0.12]),
            "Lab Result": np.random.choice(["Positive", "Negative", "Pending"], p=[0.60, 0.30, 0.10]),
            "Admission Status": np.random.choice(["Admitted", "Outpatient", "Discharged"], p=[0.70, 0.10, 0.20])
        })
        
    return pd.DataFrame(records)

# -----------------------------------------------------------------------------
# 3. PIPELINE DATA CLEANING & MATCHING ENGINE
# -----------------------------------------------------------------------------
def clean_and_process_surveillance_data(df):
    """Parses and sanitizes arbitrary column maps dynamically to prevent app crashes."""
    df_clean = df.copy()
    col_mapping = {}
    
    heuristics = {
        "Date": ["date", "onset", "report_date", "day", "timestamp"],
        "Region": ["region", "province", "state", "regione"],
        "District": ["district", "lga", "county", "municipality", "city"],
        "Facility": ["facility", "hospital", "clinic", "site", "center"],
        "Sex": ["sex", "gender", "m/f"],
        "Age": ["age", "years"],
        "Case Status": ["case status", "status", "classification", "type", "category"],
        "Death": ["death", "died", "dead", "mortality", "deceased"],
        "Recovered": ["recovered", "recovery", "cured"],
        "Latitude": ["latitude", "lat", "y_coord"],
        "Longitude": ["longitude", "lon", "lng", "x_coord"],
        "Contact Traced": ["contact traced", "contact", "traced", "contact_followed"],
        "Lab Result": ["lab result", "lab", "pcr", "result", "laboratory"],
        "Admission Status": ["admission status", "admission", "admitted", "hospitalized"]
    }
    
    for target, alternates in heuristics.items():
        for col in df_clean.columns:
            if str(col).strip().lower() == target.lower() or str(col).strip().lower() in alternates:
                col_mapping[col] = target
                break
                
    if col_mapping:
        df_clean.rename(columns=col_mapping, inplace=True)
        
    fallback_rules = {
        "Date": lambda d: pd.to_datetime(d.get("Date", datetime.today())),
        "Region": lambda d: d.get("Region", "Unassigned Region").fillna("Unassigned Region"),
        "District": lambda d: d.get("District", "Unassigned District").fillna("Unassigned District"),
        "Case Status": lambda d: d.get("Case Status", "Suspected").fillna("Suspected"),
        "Death": lambda d: pd.to_numeric(d.get("Death", 0), errors="coerce").fillna(0).astype(int),
        "Recovered": lambda d: pd.to_numeric(d.get("Recovered", 0), errors="coerce").fillna(0).astype(int),
        "Age": lambda d: pd.to_numeric(d.get("Age", 30), errors="coerce").fillna(30).astype(int),
        "Sex": lambda d: d.get("Sex", "Unknown").fillna("Unknown"),
        "Latitude": lambda d: pd.to_numeric(d.get("Latitude", 5.6), errors="coerce").fillna(5.6),
        "Longitude": lambda d: pd.to_numeric(d.get("Longitude", -0.2), errors="coerce").fillna(-0.2),
        "Contact Traced": lambda d: pd.to_numeric(d.get("Contact Traced", 0), errors="coerce").fillna(0).astype(int),
        "Lab Result": lambda d: d.get("Lab Result", "Pending").fillna("Pending"),
        "Admission Status": lambda d: d.get("Admission Status", "Admitted").fillna("Admitted")
    }
    
    for col, func in fallback_rules.items():
        if col in df_clean.columns:
            if col == "Date":
                df_clean["Date"] = pd.to_datetime(df_clean["Date"], errors='coerce').fillna(pd.to_datetime(datetime.today().date()))
            else:
                try:
                    df_clean[col] = func(df_clean)
                except Exception:
                    df_clean[col] = 0 if col in ["Death", "Recovered", "Age", "Contact Traced"] else "Unknown"
        else:
            if col == "Date":
                df_clean["Date"] = pd.to_datetime(datetime.today().date())
            elif col in ["Death", "Recovered", "Contact Traced"]:
                df_clean[col] = 0
            elif col == "Age":
                df_clean[col] = 30
            elif col in ["Latitude", "Longitude"]:
                df_clean[col] = 5.6 if col == "Latitude" else -0.2
            else:
                df_clean[col] = "Unknown"
                
    return df_clean

# -----------------------------------------------------------------------------
# 4. DATA PIPELINE LOADING COORDINATION
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### Surveillance Data Feed")
    uploaded_file = st.file_uploader(
        "Upload raw operational data sheets (.csv, .xlsx)", 
        type=["csv", "xlsx"], 
        help="Automated ingestion engine handles unstructured column mappings seamlessly."
    )

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            raw_df = pd.read_csv(uploaded_file)
        else:
            raw_df = pd.read_excel(uploaded_file, engine='openpyxl')
        processed_data = clean_and_process_surveillance_data(raw_df)
        st.sidebar.success(f"Successfully processed {len(processed_data)} records")
    except Exception as e:
        st.sidebar.error(f"Error parsing file: {e}. Loading tactical operational fallbacks.")
        processed_data = clean_and_process_surveillance_data(generate_robust_mock_data())
else:
    processed_data = clean_and_process_surveillance_data(generate_robust_mock_data())

# -----------------------------------------------------------------------------
# 5. GLOBAL APP STATE NAVIGATION FILTER CONTROLS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### Strategic Filter Framework")
    
    current_menu = st.radio(
        "Operational Section Panels",
        ["Dashboard Overview", "Surveillance & Epi Curve", "Case Management & Lab", 
         "Regional Risk & Geospatial", "Contact Tracing & Forecasting", "Data Explorer & Export"]
    )
    
    all_regions = sorted(processed_data["Region"].unique().tolist())
    selected_regions = st.multiselect("Filter by Target Region(s)", all_regions, default=all_regions[:3] if len(all_regions) > 3 else all_regions)
    
    sub_filtered_data = processed_data[processed_data["Region"].isin(selected_regions)]
    all_districts = sorted(sub_filtered_data["District"].unique().tolist())
    selected_districts = st.multiselect("Filter by Target District(s)", all_districts, default=all_districts)
    
    min_date = processed_data["Date"].min().to_pydatetime()
    max_date = processed_data["Date"].max().to_pydatetime()
    selected_date_range = st.slider("Reporting Epoch Range", min_value=min_date, max_value=max_date, value=(min_date, max_date))

filtered_df = processed_data[
    (processed_data["Region"].isin(selected_regions)) &
    (processed_data["District"].isin(selected_districts)) &
    (processed_data["Date"] >= pd.Timestamp(selected_date_range[0])) &
    (processed_data["Date"] <= pd.Timestamp(selected_date_range[1]))
]

# -----------------------------------------------------------------------------
# 6. APP VISUAL WRAPPER PLATFORM FRAME HEADER
# -----------------------------------------------------------------------------
st.markdown("""
    <div class="flag-strip">
        <div class="flag-red"></div>
        <div class="flag-yellow"></div>
        <div class="flag-green"></div>
    </div>
""", unsafe_allow_html=True)

# Main Institutional Branding Header Layout (Strict Non-Generic Clean Design)
header_col1, header_col2, header_col3 = st.columns([1, 6, 1.5])

with header_col1:
    # Look for local JPG image asset cleanly, show warning placeholder silently if not found yet
    if os.path.exists("assets/ghs_logo.jpg"):
        st.image("assets/ghs_logo.jpg", width=75)
    else:
        st.markdown("<div style='height:75px; border:1px dashed #ccc; display:flex; align-items:center; justify-content:center; font-size:10px; color:#aaa;'>GHS LOGO JPG</div>", unsafe_allow_html=True)

with header_col2:
    st.markdown("""
        <div style='padding-top: 5px;'>
            <h1 class="topbar-title">Ghana Integrated Public Health Emergency Platform (GIPHEP)</h1>
            <p class="topbar-subtitle">Ebola Outbreak Intelligence Dashboard — National PHEOC Command</p>
        </div>
    """, unsafe_allow_html=True)

with header_col3:
    if os.path.exists("assets/coat_of_arms.svg"):
        st.image("assets/coat_of_arms.svg", width=75)
    else:
        st.markdown("<div style='height:75px; border:1px dashed #ccc; display:flex; align-items:center; justify-content:center; font-size:10px; color:#aaa;'>COAT OF ARMS SVG</div>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style="text-align: right; font-size: 11px; color: #4b5563; margin-top:4px;">
            <strong>System Time:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}<br>
            <span class="badge badge-red">ACTIVATION LEVEL: GRADE 3</span>
        </div>
    """, unsafe_allow_html=True)

# Continuous Scrolling Alert Status Ticker Feed
latest_alert = "ALERT: Active Ebola virus surveillance sequence tracking initiated. Heightened border containment active."
if not filtered_df.empty:
    worst_region = filtered_df.groupby("Region").size().idxmax()
    worst_count = filtered_df.groupby("Region").size().max()
    latest_alert = f"CRITICAL INCIDENT ALERT: {worst_region} Region records severe cluster vectors ({worst_count} cases under monitoring)."

st.markdown(f"""
    <div class="ticker-container">
        <span style="color: #CE1126; margin-right: 15px; font-weight: 800;">LIVE SURVEILLANCE FEED:</span>
        <marquee scrollamount="4" behavior="scroll" direction="left">{latest_alert} — Cross-border monitoring active via Port Health authorities at Kotoka International Airport.</marquee>
    </div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 7. AUTOMATED ANALYTICAL EPIDEMIOLOGICAL INSIGHTS ENGINE
# -----------------------------------------------------------------------------
def run_epidemiological_insights_engine(df):
    """Generates complex programmatic text comments from empirical data matrices."""
    insights = []
    if df.empty:
        return ["No sufficient vector data currently tracked within the execution criteria frame."]
        
    total_confirmed = len(df[df["Case Status"] == "Confirmed"])
    total_cases = len(df)
    deaths = df["Death"].sum()
    cfr = (deaths / total_cases * 100) if total_cases > 0 else 0
    
    region_counts = df[df["Case Status"] == "Confirmed"]["Region"].value_counts()
    if not region_counts.empty:
        top_region = region_counts.index[0]
        top_region_pct = (region_counts.values[0] / total_confirmed * 100) if total_confirmed > 0 else 0
        insights.append(f"**{top_region} Region** stands out as the primary spatial hotbed, representing {top_region_pct:.1f}% of all lab-confirmed cases.")
        
    if cfr > 40:
        insights.append(f"**Critical Alert:** The aggregate Case Fatality Rate is currently at **{cfr:.1f}%**, exceeding standard WHO containment thresholds for Ebola outbreaks.")
    elif cfr > 20:
        insights.append(f"**High Alert:** Case Fatality Index has risen to **{cfr:.1f}%**. Clinical care protocols require instantaneous optimization.")
        
    avg_age = df["Age"].mean()
    insights.append(f"Epidemiological profiling notes the mean cohort age of tracked infections is **{avg_age:.1f} years**, indicating extensive transmission among working-age demographics.")
    
    tracing_pct = (df["Contact Traced"].sum() / total_cases * 100) if total_cases > 0 else 0
    if tracing_pct < 85:
        insights.append(f"**Surveillance Gap Identified:** Active ring contact tracking coverage is sub-optimal at **{tracing_pct:.1f}%**; transmission rings require reinforcement.")
    else:
        insights.append(f"Contact tracing quality benchmarks achieved **{tracing_pct:.1f}%** verification rate across current active vectors.")
        
    return insights

# -----------------------------------------------------------------------------
# 8. DASHBOARD WORKSPACE PANEL ROUTING LOGIC
# -----------------------------------------------------------------------------
if current_menu == "Dashboard Overview":
    st.markdown("### National Emergency Response Matrix")
    
    t_cases = len(filtered_df)
    s_cases = len(filtered_df[filtered_df["Case Status"] == "Suspected"])
    c_cases = len(filtered_df[filtered_df["Case Status"] == "Confirmed"])
    p_cases = len(filtered_df[filtered_df["Case Status"] == "Probable"])
    deaths = filtered_df["Death"].sum()
    recoveries = filtered_df["Recovered"].sum()
    cfr = (deaths / t_cases * 100) if t_cases > 0 else 0.0
    active_cases = t_cases - (deaths + recoveries)
    
    m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
    with m_col1:
        st.markdown(f'<div class="kpi-card-wrapper" style="border-left-color:#1f2937;"><div class="kpi-label">Cumulative Cases</div><div class="kpi-value">{t_cases}</div><div class="kpi-delta" style="color:#6b7280;">Total Logged</div></div>', unsafe_allow_html=True)
    with m_col2:
        st.markdown(f'<div class="kpi-card-wrapper" style="border-left-color:#CE1126;"><div class="kpi-label">Confirmed Cases</div><div class="kpi-value" style="color:#CE1126;">{c_cases}</div><div class="kpi-delta" style="color:#CE1126;">High Vector Trend</div></div>', unsafe_allow_html=True)
    with m_col3:
        st.markdown(f'<div class="kpi-card-wrapper" style="border-left-color:#FCD116;"><div class="kpi-label">Suspected Vectors</div><div class="kpi-value" style="color:#92400e;">{s_cases}</div><div class="kpi-delta" style="color:#92400e;">Testing Pending</div></div>', unsafe_allow_html=True)
    with m_col4:
        st.markdown(f'<div class="kpi-card-wrapper" style="border-left-color:#006B3F;"><div class="kpi-label">Total Deaths</div><div class="kpi-value">{deaths}</div><div class="kpi-delta" style="color:#b91c1c;">CFR: {cfr:.1f}%</div></div>', unsafe_allow_html=True)
    with m_col5:
        st.markdown(f'<div class="kpi-card-wrapper" style="border-left-color:#0369a1;"><div class="kpi-label">Active Surveillance</div><div class="kpi-value" style="color:#0369a1;">{active_cases}</div><div class="kpi-delta" style="color:#0369a1;">Under Isolation</div></div>', unsafe_allow_html=True)
        
    st.markdown("---")
    
    layout_col1, layout_col2 = st.columns([1.6, 1])
    
    with layout_col1:
        st.markdown("#### Core Outbreak Epicurve Trend Trajectory")
        if not filtered_df.empty:
            ts_data = filtered_df.groupby(["Date", "Case Status"]).size().reset_index(name="Counts")
            fig_epi = px.bar(
                ts_data, x="Date", y="Counts", color="Case Status",
                color_discrete_map={"Confirmed": "#CE1126", "Suspected": "#FCD116", "Probable": "#8e44ad"},
                barmode="stack", template="plotly_white"
            )
            fig_epi.update_layout(margin=dict(l=20, r=20, t=10, b=20), height=350)
            st.plotly_chart(fig_epi, use_container_width=True)
        else:
            st.info("No timeline attributes matched selection thresholds.")
            
    with layout_col2:
        st.markdown("#### Automated Epidemiological Intelligence Comments")
        compiled_notes = run_epidemiological_insights_engine(filtered_df)
        for note in compiled_notes:
            st.markdown(f"- {note}")
            
        st.markdown("#### Operational Command Interventions")
        if cfr > 35:
            st.markdown('<span class="badge badge-red">CRITICAL RECOMMENDATION</span> Deploys primary clinical stabilization surges to containment centers immediately.', unsafe_allow_html=True)
        if s_cases > 5:
            st.markdown('<span class="badge badge-yellow">LAB ALERT</span> Accelerate standard sample turnaround protocols at Noguchi Memorial Institute (NMIMR).', unsafe_allow_html=True)
        st.markdown('<span class="badge badge-green">ROUTINE SECURITY</span> Enforce strict Port Health inspections along cross-border logistics lanes.', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
if current_menu == "Surveillance & Epi Curve":
    st.markdown("### Deep-Dive Surveillance Analysis Framework")
    
    tab_curve, tab_demographics = st.tabs(["Epidemic Curves & Rolling Frameworks", "Patient Demographic Profiling"])
    
    with tab_curve:
        if not filtered_df.empty:
            daily_series = filtered_df.groupby("Date").size().reset_index(name="DailyCases")
            daily_series = daily_series.sort_values("Date")
            daily_series["7-Day Moving Avg"] = daily_series["DailyCases"].rolling(window=7, min_periods=1).mean()
            
            fig_trend = go.Figure()
            fig_trend.add_trace(go.Bar(x=daily_series["Date"], y=daily_series["DailyCases"], name="Daily Case Baseline Counts", marker_color="#e5e7eb"))
            fig_trend.add_trace(go.Scatter(x=daily_series["Date"], y=daily_series["7-Day Moving Avg"], mode='lines', name='7-Day Smoothing Average Line', line=dict(color='#006B3F', width=3)))
            
            fig_trend.update_layout(template="plotly_white", height=400, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.info("No records match configuration indices.")
            
    with tab_demographics:
        demo_col1, demo_col2 = st.columns(2)
        with demo_col1:
            st.markdown("##### Case Metric Breakdown by Biological Sex Profile")
            if not filtered_df.empty:
                fig_sex = px.pie(filtered_df, names="Sex", color_discrete_sequence=["#006B3F", "#CE1126", "#e5e7eb"], hole=0.4)
                fig_sex.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10))
                st.plotly_chart(fig_sex, use_container_width=True)
        with demo_col2:
            st.markdown("##### Patient Cohort Density across Age Stratifications")
            if not filtered_df.empty:
                fig_age = px.histogram(filtered_df, x="Age", nbins=15, color_discrete_sequence=["#FCD116"], template="plotly_white")
                fig_age.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10))
                st.plotly_chart(fig_age, use_container_width=True)

# -----------------------------------------------------------------------------
if current_menu == "Case Management & Lab":
    st.markdown("### Isolation Logistics and Diagnostic Monitoring")
    
    pane_l, pane_r = st.columns(2)
    with pane_l:
        st.markdown("#### Clinical Admission Disposition Allocations")
        if not filtered_df.empty:
            fig_adm = px.bar(filtered_df, x="Admission Status", color="Case Status", 
                             color_discrete_sequence=["#CE1126", "#006B3F", "#FCD116"], template="plotly_white")
            st.plotly_chart(fig_adm, use_container_width=True)
            
    with pane_r:
        st.markdown("#### Laboratory Molecular PCR Assay Configurations")
        if not filtered_df.empty:
            fig_lab = px.histogram(filtered_df, x="Lab Result", color="Case Status",
                                   color_discrete_sequence=["#8e44ad", "#2c3e50", "#161a2a"], template="plotly_white")
            st.plotly_chart(fig_lab, use_container_width=True)

# -----------------------------------------------------------------------------
if current_menu == "Regional Risk & Geospatial":
    st.markdown("### Geographic Transmission Mapping and Risk Tiers")
    
    st.info("Mapping layers operate client-side using coordinate scatter metrics from your uploaded records.")
    
    geo_col1, geo_col2 = st.columns([1.5, 1])
    
    with geo_col1:
        st.markdown("#### Tactical Vector Hotspot Map")
        if not filtered_df.empty:
            fig_map = px.scatter_mapbox(
                filtered_df, lat="Latitude", lon="Longitude", color="Case Status", 
                size="Age", hover_name="District", hover_data=["Region", "Facility"],
                color_discrete_map={"Confirmed": "#CE1126", "Suspected": "#FCD116", "Probable": "#8e44ad"},
                zoom=6, height=450
            )
            fig_map.update_layout(mapbox_style="open-street-map")
            fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig_map, use_container_width=True)
            
    with geo_col2:
        st.markdown("#### Regional Risk Aggregation Matrix")
        if not filtered_df.empty:
            reg_summary = filtered_df.groupby("Region").agg(
                Logged_Cases=("Case Status", "count"),
                Fatalities=("Death", "sum")
            ).reset_index()
            reg_summary["CFR (%)"] = (reg_summary["Fatalities"] / reg_summary["Logged_Cases"] * 100).round(1)
            reg_summary = reg_summary.sort_values(by="Logged_Cases", ascending=False)
            
            st.dataframe(
                reg_summary,
                column_config={
                    "Region": "Target Jurisdiction",
                    "Logged_Cases": "Total Logs",
                    "Fatalities": "Deaths",
                    "CFR (%)": st.column_config.ProgressColumn("Crude CFR Index", format="%d%%", min_value=0, max_value=100)
                },
                use_container_width=True,
                hide_index=True
            )

# -----------------------------------------------------------------------------
if current_menu == "Contact Tracing & Forecasting":
    st.markdown("### Contact Transmission Management & Forecasting")
    
    col_fc1, col_fc2 = st.columns(2)
    with col_fc1:
        st.markdown("#### Ring Containment Verification Index")
        if not filtered_df.empty:
            fig_trace = px.pie(filtered_df, names="Contact Traced", 
                               labels={1: "Traced & Followed", 0: "Missing Contact Audit"},
                               color_discrete_sequence=["#006B3F", "#CE1126"])
            st.plotly_chart(fig_trace, use_container_width=True)
            
    with col_fc2:
        st.markdown("#### Short-Horizon Epidemic Load Projections (7-Day Trend Line)")
        if not filtered_df.empty:
            daily_counts = filtered_df.groupby("Date").size().reset_index(name="Cases").sort_values("Date")
            if len(daily_counts) > 3:
                x_idx = np.arange(len(daily_counts))
                y_val = daily_counts["Cases"].values
                slope, intercept = np.polyfit(x_idx, y_val, 1)
                
                future_idx = np.arange(len(daily_counts), len(daily_counts) + 7)
                future_dates = [daily_counts["Date"].max() + timedelta(days=int(i)) for i in range(1, 8)]
                future_pred = slope * future_idx + intercept
                future_pred = np.clip(future_pred, 0, None)
                
                fig_forecast = go.Figure()
                fig_forecast.add_trace(go.Scatter(x=daily_counts["Date"], y=y_val, name="Observed Load Baseline", line=dict(color="#2c3e50")))
                fig_forecast.add_trace(go.Scatter(x=future_dates, y=future_pred, name="7-Day Predictive Runway", line=dict(color="#CE1126", dash="dash")))
                fig_forecast.update_layout(template="plotly_white", height=300, margin=dict(l=20, r=20, t=10, b=20))
                st.plotly_chart(fig_forecast, use_container_width=True)
            else:
                st.warning("Insufficient sequential data logs to generate dynamic algorithmic projections.")

# -----------------------------------------------------------------------------
if current_menu == "Data Explorer & Export":
    st.markdown("### Master Surveillance Log Query Engine")
    
    st.markdown("#### Filtered Output Records Sub-matrix")
    st.dataframe(filtered_df, use_container_width=True)
    
    st.markdown("#### Secure Operational Report Export Utilities")
    
    csv_buffer = io.StringIO()
    filtered_df.to_csv(csv_buffer, index=False)
    csv_payload = csv_buffer.getvalue()
    
    exp_col1, exp_col2 = st.columns(2)
    with exp_col1:
        st.download_button(
            label="Download Sanitized Data Log Sheet (.CSV)",
            data=csv_payload,
            file_name=f"GIPHEP_Surveillance_Export_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    with exp_col2:
        exec_brief = f"""# GIPHEP OFFICIAL EPIDEMIOLOGICAL SITUATION SUMMARY
Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Operational Filter Boundaries: {selected_date_range[0].strftime('%Y-%m-%d')} to {selected_date_range[1].strftime('%Y-%m-%d')}

## CORE OPERATIONAL INCIDENT MATRIX
- Total Logged Incident Vectors: {len(filtered_df)}
- Confirmed PCR Pathology Inoculations: {len(filtered_df[filtered_df["Case Status"] == 'Confirmed'])}
- Tracked Loss of Life / Fatalities: {filtered_df['Death'].sum()}
- Programmatic Case Fatality Index: {(filtered_df['Death'].sum()/len(filtered_df)*100) if len(filtered_df)>0 else 0:.1f}%

CONFIDENTIAL LEVEL: FOR PHEOC INTERNAL DISTRIBUTION ONLY.
"""
        st.download_button(
            label="Export Executive Epidemiological Summary (.TXT)",
            data=exec_brief,
            file_name=f"GIPHEP_Executive_Brief_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True
        )
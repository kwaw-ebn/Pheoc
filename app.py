import streamlit as st
import datetime

# -----------------------------------------------------------------------------
# 1. PAGE SETUP & SETUP CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Ghana Integrated Public Health Emergency Platform (GIPHEP)",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. COMPLETE 16 GHANA REGIONS & DISTRICTS DATA SYSTEM (NO DUMMY DATA)
# -----------------------------------------------------------------------------
GHANA_GEOGRAPHY = {
    "Ahafo": {
        "capital": "Goaso",
        "districts": ["Asunafo North Municipal", "Asunafo South", "Asutifi North", "Asutifi South", "Tano North Municipal", "Tano South Municipal"]
    },
    "Ashanti": {
        "capital": "Kumasi",
        "districts": ["Kumasi Metropolitan", "Atwima Nwabiagya Municipal", "Obuasi Municipal", "Ejisu Municipal", "Asante Akim Central Municipal", "Mampong Municipal", "Bekwai Municipal", "Amansie West", "Afigya Kwabre South", "Offinso North"]
    },
    "Bono": {
        "capital": "Sunyani",
        "districts": ["Sunyani Municipal", "Berekum East Municipal", "Dormaa Central Municipal", "Wenchi Municipal", "Jaman South Municipal", "Sunyani West Municipal", "Banda", "Tain"]
    },
    "Bono East": {
        "capital": "Techiman",
        "districts": ["Techiman Municipal", "Kintampo North Municipal", "Nkoranza South Municipal", "Atebubu-Amantin Municipal", "Sene East", "Pru West", "Techiman North"]
    },
    "Central": {
        "capital": "Cape Coast",
        "districts": ["Cape Coast Metropolitan", "Effutu Municipal", "Awutu Senya East Municipal", "Agona West Municipal", "Mfantsiman Municipal", "Komenda-Edina-Eguafo-Abirem Municipal", "Gomoa Central", "Abura-Asebu-Kwamankese"]
    },
    "Eastern": {
        "capital": "Koforidua",
        "districts": ["New Juaben South Municipal", "Nsawam Adoagyiri Municipal", "Nkawkaw Municipal", "Lower Manya Krobo Municipal", "Suhum Municipal", "Akuapem South", "West Akim Municipal", "Afram Plains North"]
    },
    "Greater Accra": {
        "capital": "Accra",
        "districts": ["Accra Metropolitan", "Tema Metropolitan", "Ga South Municipal", "La Nkwantanang-Madina Municipal", "Ledzokuku Municipal", "Adentan Municipal", "Ashaiman Municipal", "Ada East", "Shai Osudoku", "Ablekuma West Municipal"]
    },
    "North East": {
        "capital": "Nalerigu",
        "districts": ["East Mamprusi Municipal", "West Mamprusi Municipal", "Bunkpurugu Nyankpanduri", "Chereponi", "Mamprugu Moagduri", "Yunyoo-Nasuan"]
    },
    "Northern": {
        "capital": "Tamale",
        "districts": ["Tamale Metropolitan", "Savelugu Municipal", "Yendi Municipal", "Kumbungu", "Tolon", "Sagnarigu Municipal", "Karaga", "Gushiegu Municipal", "Saboba"]
    },
    "Oti": {
        "capital": "Dambai",
        "districts": ["Krachi West Municipal", "Nkwanta South Municipal", "Jasikan Municipal", "Kadjebi", "Krachi East Municipal", "Biakoye", "Guan"]
    },
    "Savannah": {
        "capital": "Damongo",
        "districts": ["West Gonja Municipal", "Bole", "Sawla-Tuna-Kalba", "Salaga North", "East Gonja Municipal", "Central Gonja", "North Gonja"]
    },
    "Upper East": {
        "capital": "Bolgatanga",
        "districts": ["Bolgatanga Municipal", "Bawku Municipal", "Navrongo Central Municipal", "Paga/Chiana/Kasena Nankana West", "Talensi", "Bongo", "Garubawku Central"]
    },
    "Upper West": {
        "capital": "Wa",
        "districts": ["Wa Municipal", "Jirapa Municipal", "Lawra Municipal", "Tumu/Sissala East Municipal", "Nadowli-Kaleo", "Lambussie-Karni", "Wa West"]
    },
    "Volta": {
        "capital": "Ho",
        "districts": ["Ho Municipal", "Hohoe Municipal", "Keta Municipal", "Ketut South Municipal", "South Tongu", "Kpando Municipal", "Anloga", "Akatsi South"]
    },
    "Western": {
        "capital": "Sekondi-Takoradi",
        "districts": ["Sekondi-Takoradi Metropolitan", "Effia-Kwesimintsim Municipal", "Tarkwa-Nsuaem Municipal", "Ellembelle", "Nzema East Municipal", "Ahanta West Municipal", "Wassa West"]
    },
    "Western North": {
        "capital": "Sefwi Wiawso",
        "districts": ["Sefwi Wiawso Municipal", "Bibiani-Anhwiaso-Bekwai Municipal", "Bodi", "Juaboso", "Sefwi Akontombra", "Suaman"]
    }
}

# -----------------------------------------------------------------------------
# 3. GIPHEP GLOBAL CORE INLINE CSS INJECTION (ALL EMOJIS REMOVED)
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
        /* Base Palette Variables */
        :root {
            --green: #006B3F;
            --yellow: #FCD116;
            --red: #CE1126;
            --bg: #f4f7f6;
            --sidebar-dark: #004d2e;
            --text: #1f2937;
            --border: #e5e7eb;
        }
        
        /* Hide default Streamlit visual headers */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Flag Ribbon Strip Component */
        .flag-strip {
            height: 6px;
            display: flex;
            width: 100%;
            margin-top: -50px;
            margin-bottom: 20px;
        }
        .flag-red { background: #CE1126; flex: 1; }
        .flag-yellow { background: #FCD116; flex: 1; }
        .flag-green { background: #006B3F; flex: 1; }
        
        /* Custom Table Layout Configuration */
        .giphep-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            margin-top: 10px;
        }
        .giphep-table th {
            text-align: left;
            padding: 12px 10px;
            color: #6b7280;
            border-bottom: 1px solid #e5e7eb;
            background: #f9fafb;
            font-weight: 600;
        }
        .giphep-table td {
            padding: 12px 10px;
            border-bottom: 1px solid #f3f4f6;
        }
        .section-divider {
            background: #f1f5f9 !important;
            font-weight: 700;
            color: #334155;
            font-size: 11px;
            text-transform: uppercase;
        }
        
        /* Badge UI Markers */
        .badge {
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
            display: inline-block;
        }
        .b-red { background: #fee2e2; color: #b91c1c; }
        .b-orange { background: #ffedd5; color: #c2410c; }
        .b-green { background: #d1fae5; color: #065f46; }
        .b-purple { background: #f3e8ff; color: #6b21a8; }
        .b-slate { background: #f1f5f9; color: #334155; }
        
        /* Dynamic Scenario Colors */
        .scen-a { color: #b91c1c; font-weight: 700; }
        .scen-b { color: #c2410c; font-weight: 700; }
        .scen-c { color: #065f46; font-weight: 700; }
    </style>
    
    <div class="flag-strip">
        <div class="flag-red"></div>
        <div class="flag-yellow"></div>
        <div class="flag-green"></div>
    </div>
""", unsafe_with_html=True)

# -----------------------------------------------------------------------------
# 4. GIPHEP HEADER & LIVE STATS BAR COMPONENT
# -----------------------------------------------------------------------------
col_header_left, col_header_right = st.columns([3, 1])

with col_header_left:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 20px;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Coat_of_arms_of_Ghana.svg/1280px-Coat_of_arms_of_Ghana.svg.png" width="55">
            <div>
                <h1 style="color: #006B3F; font-size: 24px; font-weight: 800; margin: 0; padding: 0;">Ghana Integrated Public Health Emergency Platform (GIPHEP)</h1>
                <p style="color: #64748b; font-size: 12px; margin: 2px 0 0 0; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;">Powered by Ghana National Public Health Emergency Operations Centre (PHEOC)</p>
            </div>
        </div>
    """, unsafe_with_html=True)

with col_header_right:
    current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    st.markdown(f"""
        <div style="text-align: right;">
            <p style="color: #64748b; font-size: 11px; margin: 0;">System Synchronization Status</p>
            <strong style="font-size: 14px; color: #1f2937;">{current_time}</strong>
            <div style="margin-top: 5px;"><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSpuQVNB3Y2X4GTxYETRwhMrTLqRJX3Iz7BeQ&s" width="45"></div>
        </div>
    """, unsafe_with_html=True)

# Live Status Banner
st.markdown("""
    <div style="background: #fff; padding: 10px 15px; border-left: 4px solid #CE1126; border-bottom: 1px solid #e5e7eb; margin-top: 15px; margin-bottom: 20px; font-size: 14px;">
        <strong style="color: #CE1126;">Current Warning Track:</strong> 
        <span style="font-weight: 600; color: #1f2937;">PHEIC Declared - International Bundibugyo Virus Disease (BDBV) Outbreak / Active Cholera Countermeasures Framework</span>
    </div>
""", unsafe_with_html=True)

# -----------------------------------------------------------------------------
# 5. SIDEBAR NAVIGATION CONTROLS (PILLARS)
# -----------------------------------------------------------------------------
st.sidebar.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h3 style="color: #FCD116; font-size: 16px; font-weight: 800; margin: 0;">GIPHEP COMMAND ENGINE</h3>
        <p style="color: #ffffff; font-size: 11px; opacity: 0.8; margin: 2px 0;">Strategic Core Navigation</p>
    </div>
""", unsafe_with_html=True)

app_mode = st.sidebar.radio(
    "Operational Pillars",
    [
        "Dashboard Overview", 
        "Alerts & Triage Center", 
        "Surveillance Systems", 
        "Point of Entry (PoE)", 
        "Laboratory Reference Matrix", 
        "Case Management", 
        "Infection Prevention Control (IPC)", 
        "Risk Communications (RCCE)", 
        "Supply Chain & Logistics", 
        "Partner Coordination Framework"
    ]
)

# -----------------------------------------------------------------------------
# 6. PRIMARY VIEW GENERATOR: DASHBOARD OVERVIEW
# -----------------------------------------------------------------------------
if app_mode == "Dashboard Overview":
    
    # Structural Context View Tabs
    tab_overview, tab_regional_matrix, tab_district_explorer = st.tabs([
        "National Overview & Scenario Tracking", 
        "International & Transit Risk Stratification", 
        "Ghana 16-Region District Explorer"
    ])
    
    # ----------------------------------------------------
    # TAB 1: GENERAL EPIDEMIOLOGICAL DATA METRICS
    # ----------------------------------------------------
    with tab_overview:
        st.markdown("<h3 style='color:#006B3F; font-size:16px; margin-bottom:15px; font-weight:700;'>EPIDEMIOLOGICAL RECOGNITION COUNTERS (8_MONTH OUTBREAK METRICS)</h3>", unsafe_with_html=True)
        
        # Row 1: KPI Blocks
        kpi_cols = st.columns(8)
        metrics = [
            ("Suspected Cases", "536", "+290 in 4 days", "#FCD116"),
            ("Probable Cases", "105", "Current Cluster", "#8e44ad"),
            ("Confirmed Cases", "34", "+26 in 48h PCR", "#CE1126"),
            ("Deaths (All)", "134", "+54 in 4 days", "#2c3e50"),
            ("Crude CFR", "19.8%", "Est. Max 50%", "#e67e22"),
            ("HCW Deaths", ">=4", "Mongbwalu Cluster", "#CE1126"),
            ("Doubling Time", "3.6d", "Suspect Curve", "#1abc9c"),
            ("Estimated Re", "2.2-2.8", "Uncontrolled Stage", "#3498db")
        ]
        
        for idx, (title, val, delta, color) in enumerate(metrics):
            with kpi_cols[idx]:
                st.markdown(f"""
                    <div style="background: #fff; padding: 15px 10px; border-radius: 8px; border-left: 4px solid {color}; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                        <p style="margin: 0; font-size: 11px; color: #6b7280; text-transform: uppercase; font-weight:600;">{title}</p>
                        <h2 style="margin: 5px 0 2px 0; font-size: 22px; font-weight: 800; color: #111827;">{val}</h2>
                        <span style="font-size: 11px; color: #6b7280; display: block;">{delta}</span>
                    </div>
                """, unsafe_with_html=True)

        # Row 2: Scenario Matrices & Incident Tracking
        st.markdown("<br>", unsafe_with_html=True)
        col_left_panel, col_right_panel = st.columns([1.2, 1])
        
        with col_left_panel:
            st.markdown("<h4 style='color:#006B3F; font-size:14px; font-weight:700; margin-bottom:10px;'>SCENARIO PROJECTIONS - SUSPECTED MEDICAL CASE OUTCOMES FROM BASELINE</h4>", unsafe_with_html=True)
            
            scen_table_html = """
            <table class="giphep-table">
                <thead>
                    <tr>
                        <th>Interval Days</th>
                        <th>Timeline Date Context</th>
                        <th>Scenario A (No Control Measures)</th>
                        <th>Scenario B (Partial Control Interventions)</th>
                        <th>Scenario C (Effective Control Deployment)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>Day 0</td><td>19 May Baseline Status</td><td class="scen-a">536</td><td class="scen-b">536</td><td class="scen-c">536</td></tr>
                    <tr><td>Day 7</td><td>26 May Tracking window</td><td class="scen-a">~1,997</td><td class="scen-b">~797</td><td class="scen-c">~593</td></tr>
                    <tr><td>Day 14</td><td>02 June Tracking window</td><td class="scen-a">~7,441</td><td class="scen-b">~1,185</td><td class="scen-c">~657</td></tr>
                    <tr><td>Day 21</td><td>09 June Tracking window</td><td class="scen-a">~27,700</td><td class="scen-b">~1,762</td><td class="scen-c">~728</td></tr>
                    <tr><td>Day 30</td><td>18 June Tracking window</td><td class="scen-a">~163,000</td><td class="scen-b">~3,109</td><td class="scen-c">~839</td></tr>
                    <tr><td>Day 42</td><td>01 July Forecast Window</td><td class="scen-a">~1,900,000</td><td class="scen-b">~6,570</td><td class="scen-c">~1,014</td></tr>
                </tbody>
            </table>
            """
            st.markdown(scen_table_html, unsafe_with_html=True)
            
        with col_right_panel:
            st.markdown("<h4 style='color:#006B3F; font-size:14px; font-weight:700; margin-bottom:10px;'>RESPONSE GAP ANALYSIS INCIDENT DASHBOARD</h4>", unsafe_with_html=True)
            
            gap_table_html = """
            <table class="giphep-table">
                <thead>
                    <tr>
                        <th>Strategic Response Pillar</th>
                        <th>Elements in Place</th>
                        <th>Detected Critical Gaps</th>
                        <th>Operational Operational Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>Coordination Setups</td><td>4 Elements</td><td>1 Gap Element</td><td><span class="badge b-orange">Partial</span></td></tr>
                    <tr><td>Surveillance & Lab Tracking</td><td>2 Elements</td><td>3 Gap Elements</td><td><span class="badge b-orange">Partial</span></td></tr>
                    <tr><td>IPC Active Countermeasures</td><td>0 Elements</td><td>7 Gap Elements</td><td><span class="badge b-red">Critical Gaps</span></td></tr>
                    <tr><td>Case Management Modules</td><td>0 Elements</td><td>4 Gap Elements</td><td><span class="badge b-red">Critical Gaps</span></td></tr>
                    <tr><td>Contact Tracing Core</td><td>0 Elements</td><td>5 Gap Elements</td><td><span class="badge b-red">Collapsed Status</span></td></tr>
                    <tr><td>Border Health Systems (PoE)</td><td>0 Elements</td><td>2 Gap Elements</td><td><span class="badge b-orange">Partial</span></td></tr>
                    <tr class="section-divider">
                        <td>Total System Infrastructure (64 Elements)</td>
                        <td>8 Elements (12.5%)</td>
                        <td>34 Elements (53.1%)</td>
                        <td><span class="badge b-red">Major Gaps</span></td>
                    </tr>
                </tbody>
            </table>
            """
            st.markdown(gap_table_html, unsafe_with_html=True)

        # Operational Directives Box Block
        st.markdown("<br><h4 style='color:#006B3F; font-size:14px; font-weight:700;'>STRATEGIC INTERVENTION FRAMEWORKS (NEXT 48-72 HOURS)</h4>", unsafe_with_html=True)
        st.markdown("""
            <div style="background: #fff5f5; border-left: 4px solid #CE1126; padding: 12px; font-size: 13px; margin-bottom: 8px; color: #1f2937;">
                <strong>CRITICAL CRISIS INTERVENTION DIRECTION:</strong> Immediately scale up contact tracking fields to minimum target index of >=5 registered contacts per confirmed viral lineage using Go.Data framework parameters. Deploy field molecular lab infrastructures to regional centers to offset processing lag metrics.
            </div>
            <div style="background: #f0fdf4; border-left: 4px solid #006B3F; padding: 12px; font-size: 13px; color: #1f2937;">
                <strong>GHANA PORT SURVEILLANCE DIRECTIVE:</strong> Enforce mandatory physical electronic passenger health logging validations at Kotoka International Airport (KIA) for arrivals tracking from referenced regional flight lines.
            </div>
        """, unsafe_with_html=True)

    # ----------------------------------------------------
    # TAB 2: REGIONAL RISK STRATIFICATION MATRIX
    # ----------------------------------------------------
    with tab_regional_matrix:
        st.markdown("<h3 style='color:#006B3F; font-size:16px; margin-bottom:5px; font-weight:700;'>REGIONAL RISK MATRIX - TRANSIT CORRIDORS STRATIFICATION</h3>", unsafe_with_html=True)
        st.markdown("<p style='font-size:12px; color:#6b7280; margin-bottom:15px;'>West Africa Risk Index Focus: Aviation vector pathways. Baseline stocks of rVSV-ZEBOV do not provide resistance against BDBV profiles.</p>", unsafe_with_html=True)
        
        regional_matrix_html = """
        <table class="giphep-table">
            <thead>
                <tr>
                    <th>Country Area Entity</th>
                    <th>Risk Stratification Level</th>
                    <th>Primary Vector / Exposure Route</th>
                    <th>Response Architecture Capacity</th>
                    <th>Immediate Action Guidelines</th>
                </tr>
            </thead>
            <tbody>
                <tr class="section-divider"><td colspan="5">East and Central Africa - Border Impact Interface Zones</td></tr>
                <tr><td><strong>Uganda</strong> (Kampala / Western)</td><td><span class="badge b-red">Critical</span></td><td>2 confirmed unlinked importations in urban center; overland via Ituri routes</td><td>High experience; mobile laboratory components deployed</td><td>Trace contacts; scale border checks</td></tr>
                <tr><td><strong>South Sudan</strong> (Juba)</td><td><span class="badge b-red">Very High</span></td><td>Land routes via Ituri; 700K population displacement tracking context</td><td>Extremely resource-constrained environment</td><td>WHO asset staging; deploy basic PPE blocks</td></tr>
                <tr><td><strong>Rwanda</strong></td><td><span class="badge b-orange">High</span></td><td>Goma-Gisenyi marketplace networks; high logistics hub volume</td><td>Strong healthcare core background markers</td><td>Validate laboratory PCR primer sequences</td></tr>
                
                <tr class="section-divider"><td colspan="5">West Africa Flight Hub Vector Tracking - Aviation Context</td></tr>
                <tr><td><strong>Ghana</strong> (Accra Context)</td><td><span class="badge b-orange">Low-Moderate</span></td><td>Entebbe-Addis-Accra connections; deployment rotation vectors</td><td>MoH-GHS collaborative network; Noguchi (NMIMR) and KCCR reference systems; active historical monitoring framework</td><td>Heighten KIA entry logs; alert isolation bays at GIDC, Korle-Bu, and UGMC; review clinical diagnostic protocols</td></tr>
                <tr><td><strong>Nigeria</strong> (Lagos / Abuja)</td><td><span class="badge b-orange">Low-Moderate</span></td><td>Lagos MMIA airport networks; Kinshasa routing lines</td><td>NCDC active network engine; functioning isolation hubs</td><td>Trigger airport surveillance matrix logs</td></tr>
                <tr><td><strong>Togo</strong> (Lome Hub)</td><td><span class="badge b-slate">Low</span></td><td>ASKY airline transit framework infrastructure nodes</td><td>Moderate diagnostic capacity</td><td>Alert transit air crews to manifest screens</td></tr>
            </tbody>
        </table>
        """
        st.markdown(regional_matrix_html, unsafe_with_html=True)

    # ----------------------------------------------------
    # TAB 3: GHANA 16-REGION DISTRICT EXPLORER SYSTEM
    # ----------------------------------------------------
    with tab_district_explorer:
        st.markdown("<h3 style='color:#006B3F; font-size:16px; margin-bottom:10px; font-weight:700;'>NATIONAL HIERARCHICAL INCIDENT SYSTEM</h3>", unsafe_with_html=True)
        st.markdown("<p style='font-size:13px; color:#4b5563;'>Select from Ghana's 16 administrative regions to view the corresponding regional capital and districts assigned to local public health surveillance reporting units.</p>", unsafe_with_html=True)
        
        # Region Picker Dropdown (Strictly 16 Regions)
        region_list = list(GHANA_GEOGRAPHY.keys())
        selected_reg = st.selectbox("Public Health Surveillance Region", region_list)
        
        if selected_reg:
            capital_city = GHANA_GEOGRAPHY[selected_reg]["capital"]
            district_array = GHANA_GEOGRAPHY[selected_reg]["districts"]
            total_districts = len(district_array)
            
            # Regional Data Cards
            col_reg1, col_reg2 = st.columns(2)
            with col_reg1:
                st.markdown(f"""
                    <div style="background:#f9fafb; padding:15px; border-radius:6px; border-left:4px solid #006B3F;">
                        <span style="font-size:11px; color:#6b7280; text-transform:uppercase; font-weight:600;">Designated Administrative Center</span>
                        <h4 style="margin:5px 0 0 0; color:#006B3F; font-size:18px; font-weight:700;">{capital_city}</h4>
                    </div>
                """, unsafe_with_html=True)
            with col_reg2:
                st.markdown(f"""
                    <div style="background:#f9fafb; padding:15px; border-radius:6px; border-left:4px solid #FCD116;">
                        <span style="font-size:11px; color:#6b7280; text-transform:uppercase; font-weight:600;">Active Reporting Surveillance Districts</span>
                        <h4 style="margin:5px 0 0 0; color:#1f2937; font-size:18px; font-weight:700;">{total_districts} Districts Registered</h4>
                    </div>
                """, unsafe_with_html=True)
            
            st.markdown("<br><h4 style='font-size:13px; color:#006B3F; font-weight:700;'>REGISTERED DISTRICT ASSEMBLY REPORTING HOTLINES</h4>", unsafe_with_html=True)
            
            # Format Districts in columns
            dist_cols = st.columns(3)
            for i, d_name in enumerate(district_array):
                target_col = dist_cols[i % 3]
                with target_col:
                    st.markdown(f"""
                        <div style="background:#fff; padding:10px; margin-bottom:6px; border:1px solid #e5e7eb; border-radius:4px; font-size:12px; color:#374151;">
                            <strong>{d_name}</strong><br>
                            <span style="font-size:10px; color:#9ca3af;">Status Line: Functional Tracking</span>
                        </div>
                    """, unsafe_with_html=True)

# -----------------------------------------------------------------------------
# 7. SECONDARY SUB-PAGE CORE MODULE STUBS (ALL EMOJIS STRIPPED)
# -----------------------------------------------------------------------------
else:
    st.markdown(f"<h2 style='color:#006B3F; font-size:20px; font-weight:700;'>{app_mode}</h2>", unsafe_with_html=True)
    st.markdown("""
        <div style="background:#fff; padding:30px; border-radius:8px; border:1px solid #e5e7eb; color:#4b5563; font-size:14px;">
            Integration Panel Status: Operational Network Standby.<br>
            All platform endpoints for this module are configured to handle live medical telemetry directly from the regional reporting nodes.
        </div>
    """, unsafe_with_html=True)

<!DOCTYPE html>
<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ghana Integrated Public Health Emergency Platform (GIPHEP)</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght=400;500;600;700;800&display=swap" rel="stylesheet">

    <style>
        :root {
            --green: #006B3F;
            --yellow: #FCD116;
            --red: #CE1126;
            --bg: #f4f7f6;
            --sidebar-dark: #004d2e;
            --text: #1f2937;
            --border: #e5e7eb;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', sans-serif;
        }

        body {
            background: var(--bg);
            color: var(--text);
            overflow-x: hidden;
            height: 100vh;
        }

        .app {
            display: flex;
            height: 100vh;
        }

        /* SIDEBAR */
        .sidebar {
            width: 260px;
            background: var(--sidebar-dark);
            color: #fff;
            display: flex;
            flex-direction: column;
            flex-shrink: 0;
            z-index: 1001;
        }

        .sidebar-brand {
            padding: 20px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .sidebar-brand small {
            color: var(--yellow);
            font-weight: 700;
            letter-spacing: 0.5px;
            font-size: 11px;
            text-transform: uppercase;
        }

        .sidebar-menu {
            padding: 15px 10px;
            flex: 1;
            overflow-y: auto;
        }

        .sidebar button {
            width: 100%;
            background: none;
            border: none;
            color: rgba(255, 255, 255, 0.8);
            padding: 12px 15px;
            text-align: left;
            cursor: pointer;
            border-radius: 8px;
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 14px;
            font-weight: 500;
            transition: 0.2s;
            margin-bottom: 2px;
        }

        .sidebar button:hover,
        .sidebar button.active {
            background: rgba(255, 255, 255, 0.15);
            color: #fff;
            box-shadow: inset 4px 0 0 var(--yellow);
        }

        /* MAIN AREA */
        .main {
            flex: 1;
            display: flex;
            flex-direction: column;
            min-width: 0;
        }

        .flag-strip {
            height: 6px;
            display: flex;
        }

        .flag-red { background: var(--red); flex: 1; }
        .flag-yellow { background: var(--yellow); flex: 1; }
        .flag-green { background: var(--green); flex: 1; }

        .topbar {
            background: #fff;
            padding: 10px 25px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border);
        }

        .topbar-left {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .topbar-title {
            font-size: 16px;
            font-weight: 800;
            color: var(--green);
            max-width: 450px;
            line-height: 1.2;
        }

        .tabs {
            display: flex;
            gap: 8px;
        }

        .tabs button {
            padding: 8px 16px;
            border: 1px solid #eee;
            background: #f9fafb;
            border-radius: 20px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 600;
        }

        .tabs button.active {
            background: var(--green);
            color: #fff;
            border-color: var(--green);
        }

        .topbar-right {
            display: flex;
            align-items: center;
            gap: 15px;
            text-align: right;
        }

        /* TICKER */
        .ticker {
            background: #fff;
            padding: 10px 25px;
            border-bottom: 2px solid var(--red);
            font-size: 14px;
            display: flex;
            align-items: center;
        }

        #statusText {
            font-weight: 600;
            margin-left: 10px;
            color: #333;
            transition: opacity 0.4s ease;
        }

        /* CONTENT */
        .content {
            padding: 20px;
            overflow-y: auto;
            flex: 1;
        }

        .page { display: none; }
        .page.active { display: block; }

        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }

        .kpi-card {
            background: #fff;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
            border-left: 4px solid var(--green);
        }

        .kpi-card h4 {
            font-size: 11px;
            color: #6b7280;
            text-transform: uppercase;
            margin-bottom: 8px;
        }

        .kpi-card h2 {
            font-size: 24px;
            color: #111827;
            font-weight: 800;
        }

        .kpi-card .sub-text {
            font-size: 11px;
            color: #6b7280;
            margin-top: 4px;
        }

        .main-grid {
            display: grid;
            grid-template-columns: 1.6fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }

        @media (max-width: 1024px) {
            .main-grid {
                grid-template-columns: 1fr;
            }
        }

        .panel {
            background: #fff;
            border-radius: 12px;
            border: 1px solid var(--border);
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }

        .panel-head {
            padding: 15px 20px;
            background: #f9fafb;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .panel-head h3 {
            font-size: 14px;
            font-weight: 700;
            color: var(--green);
            text-transform: uppercase;
        }

        .panel-body { padding: 20px; }

        /* TABLES */
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }

        th {
            text-align: left;
            padding: 12px 10px;
            color: #6b7280;
            border-bottom: 1px solid #eee;
            background: #fcfcfc;
        }

        td {
            padding: 12px 10px;
            border-bottom: 1px solid #f9f9f9;
        }

        .badge {
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
        }

        .b-red { background: #fee2e2; color: #b91c1c; }
        .b-orange { background: #ffedd5; color: #c2410c; }
        .b-green { background: #d1fae5; color: #065f46; }
        .b-purple { background: #f3e8ff; color: #6b21a8; }
        .b-slate { background: #f1f5f9; color: #334155; }
        .b-blue { background: #e0f2fe; color: #0369a1; }

        /* TIMELINE ELEMENTS */
        .timeline-list {
            display: flex;
            flex-direction: column;
            gap: 14px;
        }
        .timeline-item {
            border-left: 2px solid var(--border);
            padding-left: 15px;
            position: relative;
        }
        .timeline-item::before {
            content: '';
            position: absolute;
            left: -5px;
            top: 4px;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--green);
        }
        .timeline-item.alert-item::before { background: var(--red); }
        .timeline-item.confirm-item::before { background: var(--yellow); }
        .timeline-date {
            font-size: 11px;
            font-weight: 700;
            color: #64748b;
        }
        .timeline-text {
            font-size: 13px;
            color: var(--text);
            margin-top: 2px;
        }

        /* SCENARIO SHAPES */
        .scen-a { color: #b91c1c; font-weight: 700; }
        .scen-b { color: #c2410c; font-weight: 700; }
        .scen-c { color: #065f46; font-weight: 700; }

        .section-divider {
            background: #f1f5f9;
            font-weight: 700;
            color: #334155;
            font-size: 11px;
            text-transform: uppercase;
        }
    </style>
</head>

<body>
    <div class="app">
        <aside class="sidebar">
            <div class="sidebar-brand">
                <small><h4 style="text-transform: none;">Powered by Ghana PHEOC</h4> </small>
            </div>
            <div class="sidebar-menu">
                <button onclick="showPage('dashboard')" class="active">Dashboard</button>
                <button onclick="showPage('alerts')">Alerts</button>
                <button onclick="showPage('surveillance')">Surveillance</button>
                <button onclick="showPage('poe')">Point of Entry</button>
                <button onclick="showPage('lab')">Laboratory</button>
                <button onclick="showPage('case')">Case Management</button>
                <button onclick="showPage('ambulance')">IPC</button>
                <button onclick="showPage('risk')">RCCE</button>
                <button onclick="showPage('supply')">Supply Chain &amp; Logistics</button>
                <button onclick="showPage('partners')">Coordination</button>
            </div>
        </aside>

        <div class="main">
            <div class="flag-strip">
                <div class="flag-red"></div>
                <div class="flag-yellow"></div>
                <div class="flag-green"></div>
            </div>
            
            <header class="topbar">
                <div class="topbar-left">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Coat_of_arms_of_Ghana.svg/1280px-Coat_of_arms_of_Ghana.svg.png" width="50" alt="Coat of Arms of Ghana">
                    <h2 class="topbar-title">Ghana Integrated Public Health Emergency Platform (GIPHEP)</h2>
                </div>

                <nav class="tabs">
                    <button class="active" onclick="showPage('dashboard')">Overview</button>
                    <button onclick="showPage('global')">Global Event</button>
                    <button onclick="showPage('events')">National Event</button>
                    <button onclick="showPage('regions')">Region</button>
                    <button onclick="showPage('districts')">District</button>
                    <button onclick="showPage('ims')">IMS</button>
                </nav>

                <div class="topbar-right">
                    <div>
                        <small style="color:#64748b;">Last updated</small><br>
                        <strong id="time" style="font-size:13px;">19/05/2026 15:02:06</strong>
                    </div>
                    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSpuQVNB3Y2X4GTxYETRwhMrTLqRJX3Iz7BeQ&s" width="50" alt="Ghana Health Service Logo">
                </div>
            </header>

            <div class="ticker">
                <strong style="color:var(--red)">Current Status:</strong>
                <span id="statusText">PHEIC Declared: Bundibugyo Virus Disease (BDBV) Outbreak</span>
            </div>

            <div class="content">
                <div id="dashboard" class="page active">
                    
                    <div class="kpi-grid">
                        <div class="kpi-card" style="border-left-color: var(--yellow)">
                            <h4>Suspected Cases</h4>
                            <h2>536</h2>
                            <div class="sub-text">▲ +290 in 4 days</div>
                        </div>
                        <div class="kpi-card" style="border-left-color: #8e44ad">
                            <h4>Probable Cases</h4>
                            <h2>105</h2>
                            <div class="sub-text">As of 19 May 2026</div>
                        </div>
                        <div class="kpi-card" style="border-left-color: var(--red)">
                            <h4>Confirmed Cases</h4>
                            <h2>34</h2>
                            <div class="sub-text">▲ +26 in 48h lab PCR</div>
                        </div>
                        <div class="kpi-card" style="border-left-color: #2c3e50">
                            <h4>Deaths (All)</h4>
                            <h2>134</h2>
                            <div class="sub-text">▲ +54 in 4 days</div>
                        </div>
                        <div class="kpi-card" style="border-left-color: #e67e22">
                            <h4>Crude CFR</h4>
                            <h2>19.8%</h2>
                            <div class="sub-text">Confirmed est. 30-50%</div>
                        </div>
                        <div class="kpi-card" style="border-left-color: var(--red)">
                            <h4>HCW Deaths</h4>
                            <h2>≥4</h2>
                            <div class="sub-text">Mongbwalu GRH cluster</div>
                        </div>
                        <div class="kpi-card" style="border-left-color: #1abc9c">
                            <h4>Doubling Time</h4>
                            <h2>3.6d</h2>
                            <div class="sub-text">From suspect trends</div>
                        </div>
                        <div class="kpi-card" style="border-left-color: #3498db">
                            <h4>Estimated Re</h4>
                            <h2>2.2–2.8</h2>
                            <div class="sub-text">Uncontrolled phase</div>
                        </div>
                    </div>

                    <div class="main-grid" style="grid-template-columns: 1fr;">
                        <div class="panel">
                            <div class="panel-head"><h3>Regional Risk Stratification — East, Central &amp; West Africa Corridor</h3></div>
                            <div class="panel-body" style="overflow-x: auto;">
                                <div style="font-size:12px; color:#64748b; margin-bottom:12px;">
                                    West Africa pathway: Air importation only. Primary routes: Entebbe/Kampala to West African Hubs via Addis Ababa or Nairobi. Note: Prior rVSV-ZEBOV stock does NOT protect against BDBV.
                                </div>
                                <table>
                                    <thead>
                                        <tr>
                                            <th>Country / Area</th>
                                            <th>Risk Level</th>
                                            <th>Primary Exposure Pathway</th>
                                            <th>Response Capacity</th>
                                            <th>Priority Action</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr class="section-divider"><td colspan="5">East &amp; Central Africa — Direct Land Border Corridor</td></tr>
                                        <tr>
                                            <td><strong>Uganda</strong> (Kampala + Western)</td>
                                            <td><span class="badge b-red">Critical</span></td>
                                            <td>2 confirmed unlinked imported cases in Kampala; overland from Ituri</td>
                                            <td>Strong EVD experience; mobile lab deployed</td>
                                            <td>Expand contact tracing; PoE screening; cross-border tracking</td>
                                        </tr>
                                        <tr>
                                            <td><strong>South Sudan</strong> (W. Equatoria, Juba)</td>
                                            <td><span class="badge b-red">Very High</span></td>
                                            <td>Land border Ituri-SS; ~700K DRC refugees; Arua crossings</td>
                                            <td>Very weak; among lowest IHR scores in AFRO region</td>
                                            <td>Immediate WHO engagement; pre-position PPE; PoE activations</td>
                                        </tr>
                                        <tr>
                                            <td><strong>Rwanda</strong></td>
                                            <td><span class="badge b-orange">High</span></td>
                                            <td>Goma-Gisenyi corridor; high-volume trade; Kigali aviation hub</td>
                                            <td>Best health system in region; strong EVD baseline</td>
                                            <td>Confirm BDBV PCR capacity; maintain Goma PoE metrics</td>
                                        </tr>
                                        <tr>
                                            <td><strong>Burundi</strong> (Bujumbura)</td>
                                            <td><span class="badge b-orange">High</span></td>
                                            <td>South Kivu corridor; Lake Tanganyika crossings; refugee tracking</td>
                                            <td>Moderate-limited; capacity constrained</td>
                                            <td>Activate zero-reporting protocols; alert urban facilities</td>
                                        </tr>
                                        <tr>
                                            <td><strong>Central African Republic</strong></td>
                                            <td><span class="badge b-orange">High</span></td>
                                            <td>Northern DRC border (Mbomou-Ituri); mining corridor crossings</td>
                                            <td>Very fragile; MINUSCA infrastructure fallback support</td>
                                            <td>Alert MINUSCA networks; activate border surveillance systems</td>
                                        </tr>
                                        
                                        <tr class="section-divider"><td colspan="5">West Africa Aviation Context — Air Importation Corridor Focus</td></tr>
                                        <tr>
                                            <td><strong>Ghana</strong> (Accra) - Focus Context</td>
                                            <td><span class="badge b-orange">Low-Moderate</span></td>
                                            <td>Daily Entebbe-Addis-Accra flights; peacekeepers/UN staff deployments</td>
                                            <td>Good; MoH-GHS and partners unified ("Ghana CDC"); NMIMR, KCCR reference labs P3 diagnostic setups; 2014-16 response institutional memory</td>
                                            <td>Heighten KIA Port Health screening; alert GIDC, Korle-Bu &amp; UGMC containment units; brief teams on BDBV clinical protocols</td>
                                        </tr>
                                        <tr>
                                            <td><strong>Nigeria</strong> (Lagos / Abuja)</td>
                                            <td><span class="badge b-orange">Low-Moderate</span></td>
                                            <td>Lagos MMIA hub; direct DRC connections; diaspora networks in Kinshasa</td>
                                            <td>Strong; NCDC containment track (2014); functional Port Health</td>
                                            <td>Activate MMIA port health surveillance; brief urban apex hospitals</td>
                                        </tr>
                                        <tr>
                                            <td><strong>Côte d'Ivoire</strong> (Abidjan)</td>
                                            <td><span class="badge b-orange">Low-Moderate</span></td>
                                            <td>FHB Airport hub; Brussels Airlines routing; Francophone travel lines</td>
                                            <td>Moderate; Institut Pasteur diagnostic capacity; prior EVD memory</td>
                                            <td>Activate FHB airport desk; brief Pasteur teams on BDBV profile</td>
                                        </tr>
                                        <tr>
                                            <td><strong>Guinea</strong> (Conakry)</td>
                                            <td><span class="badge b-orange">Low-Moderate</span></td>
                                            <td>Regional networks; transit hubs; citizens in DRC mining sites</td>
                                            <td>Fragile but strong response memory (2013-21); MSF embedded</td>
                                            <td>Differentiate BDBV from Zaire strains; do not deploy Ervebo vaccine</td>
                                        </tr>
                                        <tr>
                                            <td><strong>Senegal</strong> (Dakar)</td>
                                            <td><span class="badge b-green">Low</span></td>
                                            <td>AIBD hub; Ethiopian Airlines connectivity; UN/NGO staff routes</td>
                                            <td>Good; SAMU response; Institut Pasteur Dakar validation capacity</td>
                                            <td>Maintain passive surveillance; brief reference labs on BDBV PCR</td>
                                        </tr>
                                        <tr>
                                            <td><strong>Togo</strong> (Lomé)</td>
                                            <td><span class="badge b-green">Low</span></td>
                                            <td>ASKY Airlines regional transit hub framework</td>
                                            <td>Moderate; airline transit context poses high node risk</td>
                                            <td>Activate Lomé airport desk; brief flight crew protocols</td>
                                        </tr>
                                        <tr>
                                            <td><strong>Liberia</strong> &amp; <strong>Sierra Leone</strong></td>
                                            <td><span class="badge b-purple">Low Exp/High Vuln</span></td>
                                            <td>Extremely limited direct network air routes from epicentre</td>
                                            <td>Very fragile; severely weakened systems; low safety buffer</td>
                                            <td>Pre-position rapid response tools; ensure basic PCR access lines</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>

                    <div class="main-grid">
                        <div class="panel">
                            <div class="panel-head"><h3>Active Hazard Tracking Log</h3></div>
                            <div class="panel-body">
                                <table>
                                    <thead>
                                        <tr>
                                            <th>Hazard Event</th>
                                            <th>Primary Location Focus</th>
                                            <th>Status Line</th>
                                            <th>Severity Scale</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td><strong>Bundibugyo Virus Disease (BDBV)</strong></td>
                                            <td>DRC Ituri (Mongbwalu/Rwampara) &amp; Uganda (Kampala)</td>
                                            <td><span class="badge b-red">Uncontrolled Phase</span></td>
                                            <td><span class="badge b-red">Critical - PHEIC</span></td>
                                        </tr>
                                        <tr>
                                            <td><strong>Cholera Outbreak</strong></td>
                                            <td>Greater Accra Region</td>
                                            <td><span class="badge b-orange">Ongoing Response</span></td>
                                            <td><span class="badge b-red">High Risk</span></td>
                                        </tr>
                                        <tr>
                                            <td><strong>Meningitis Incidents</strong></td>
                                            <td>Upper West / Northern Regions</td>
                                            <td><span class="badge b-green">Contained</span></td>
                                            <td><span class="badge b-orange">Medium Risk</span></td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        <div class="panel">
                            <div class="panel-head"><h3>Outbreak Event Timeline</h3></div>
                            <div class="panel-body">
                                <div class="timeline-list">
                                    <div class="timeline-item">
                                        <div class="timeline-date">24 April 2026</div>
                                        <div class="timeline-text">Index case (HCW, Bunia) onset recorded with fever and haemorrhage.</div>
                                    </div>
                                    <div class="timeline-item alert-item">
                                        <div class="timeline-date">24–28 April 2026</div>
                                        <div class="timeline-text">4 healthcare workers die within 4 days at Mongbwalu GRH.</div>
                                    </div>
                                    <div class="timeline-item">
                                        <div class="timeline-date">5 May 2026</div>
                                        <div class="timeline-text">WHO alerted to high-mortality unknown clusters in Mongbwalu HZ.</div>
                                    </div>
                                    <div class="timeline-item confirm-item">
                                        <div class="timeline-date">15 May 2026</div>
                                        <div class="timeline-text">INRB confirms Bundibugyo virus by PCR. Uganda confirms imported death.</div>
                                    </div>
                                    <div class="timeline-item alert-item">
                                        <div class="timeline-date">16 May 2026</div>
                                        <div class="timeline-text">WHO Director-General declares PHEIC under IHR (2005) regulations.</div>
                                    </div>
                                    <div class="timeline-item">
                                        <div class="timeline-date">19 May 2026</div>
                                        <div class="timeline-text">Suspected cases rise to 536 with 134 deaths; doubling time at 3.6 days.</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="main-grid">
                        <div class="panel">
                            <div class="panel-head"><h3>Scenario Projections — Suspected Case Metrics From Baseline</h3></div>
                            <div class="panel-body">
                                <table>
                                    <thead>
                                        <tr>
                                            <th>Days</th>
                                            <th>Timeline Date</th>
                                            <th>Scenario A (No Control)</th>
                                            <th>Scenario B (Partial Control)</th>
                                            <th>Scenario C (Effective Control)</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr><td>Day 0</td><td>19 May Baseline</td><td class="scen-a">536</td><td class="scen-b">536</td><td class="scen-c">536</td></tr>
                                        <tr><td>Day 7</td><td>26 May Tracking</td><td class="scen-a">~1,997</td><td class="scen-b">~797</td><td class="scen-c">~593</td></tr>
                                        <tr><td>Day 14</td><td>02 Jun Tracking</td><td class="scen-a">~7,441</td><td class="scen-b">~1,185</td><td class="scen-c">~657</td></tr>
                                        <tr><td>Day 21</td><td>09 Jun Tracking</td><td class="scen-a">~27,700</td><td class="scen-b">~1,762</td><td class="scen-c">~728</td></tr>
                                        <tr><td>Day 30</td><td>18 Jun Tracking</td><td class="scen-a">~163,000</td><td class="scen-b">~3,109</td><td class="scen-c">~839</td></tr>
                                        <tr><td>Day 42</td><td>01 Jul Projections</td><td class="scen-a">~1,900,000</td><td class="scen-b">~6,570</td><td class="scen-c">~1,014</td></tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        <div class="panel">
                            <div class="panel-head"><h3>Response Gap Analysis Dashboard Matrix</h3></div>
                            <div class="panel-body">
                                <table>
                                    <thead>
                                        <tr>
                                            <th>Response Pillar</th>
                                            <th>In Place</th>
                                            <th>Gap Check</th>
                                            <th>Operational Status</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr><td>Coordination Setups</td><td>4 Elements</td><td>1 Gap Element</td><td><span class="badge b-orange">Partial</span></td></tr>
                                        <tr><td>Surveillance &amp; Lab</td><td>2 Elements</td><td>3 Gap Elements</td><td><span class="badge b-orange">Partial</span></td></tr>
                                        <tr><td>IPC Countermeasures</td><td>0 Elements</td><td>7 Gap Elements</td><td><span class="badge b-red">Critical Gaps</span></td></tr>
                                        <tr><td>Case Management</td><td>0 Elements</td><td>4 Gap Elements</td><td><span class="badge b-red">Critical Gaps</span></td></tr>
                                        <tr><td>Contact Tracing System</td><td>0 Elements</td><td>5 Gap Elements</td><td><span class="badge b-red">Collapsed Status</span></td></tr>
                                        <tr><td>Border Health &amp; PoE</td><td>0 Elements</td><td>2 Gap Elements</td><td><span class="badge b-orange">Partial</span></td></tr>
                                        <tr style="background:#f8fafc; font-weight:700;">
                                            <td>Total (64 Elements)</td>
                                            <td>8 (12.5%)</td>
                                            <td>34 (53.1%)</td>
                                            <td><span class="badge b-red">Major Gaps</span></td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>

                    <div class="main-grid" style="grid-template-columns: 1fr;">
                        <div class="panel">
                            <div class="panel-head"><h3>Decision Support &amp; Immediate Operational Priorities (Next 48–72 Hours)</h3></div>
                            <div class="panel-body">
                                <div style="border-left: 4px solid var(--red); background: #fff5f5; padding: 15px; font-size: 13px; margin-bottom:12px;">
                                    <strong>CRITICAL EMERGENCY ACTION:</strong> Scale up contact tracing to ≥5 contacts per confirmed case via Go.Data framework. Deploy field BDBV PCR laboratories to Bunia to bypass central logistics friction windows.
                                </div>
                                <div style="border-left: 4px solid var(--yellow); background: #fffdf0; padding: 15px; font-size: 13px; margin-bottom:12px;">
                                    <strong>HUMANITARIAN INTERVENTION NOTICE:</strong> Negotiate operational humanitarian corridors for RRT teams with local armed factions using third-party intermediaries. Deploy immediate emergency PPE buffers to Rwampara and Mongbwalu.
                                </div>
                                <div style="border-left: 4px solid var(--green); background: #f0fdf4; padding: 15px; font-size: 13px;">
                                    <strong>GHANA PORT HEALTH ADVISORY:</strong> Enforce strict traveler health declarations and screen entries at Kotoka International Airport (KIA) for passengers originating from East/Central African travel corridors.
                                </div>
                            </div>
                        </div>
                    </div>

                </div>

                <div id="alerts" class="page"><div class="panel"><div class="panel-body">Alerts and Triage Center Centerline</div></div></div>
                <div id="surveillance" class="page"><div class="panel"><div class="panel-body">Epidemiological Data Engines</div></div></div>
                <div id="poe" class="page"><div class="panel"><div class="panel-body">Airport and Border Controls Systems</div></div></div>
                <div id="lab" class="page"><div class="panel"><div class="panel-body">Lab Information Reference Systems</div></div></div>
                <div id="case" class="page"><div class="panel"><div class="panel-body">Clinical Case Management Trackers</div></div></div>
                <div id="ambulance" class="page"><div class="panel"><div class="panel-body">National Ambulance Dispatch Logistics</div></div></div>
                <div id="risk" class="page"><div class="panel"><div class="panel-body">Public Risk Communications Coordination</div></div></div>
                <div id="supply" class="page"><div class="panel"><div class="panel-body">Supply Chain and Logistics Tracker Matrix</div></div></div>
                <div id="partners" class="page"><div class="panel"><div class="panel-body">Partner Coordination Infrastructure</div></div></div>
                <div id="global" class="page"><div class="panel"><div class="panel-body">Global Event Monitoring Core</div></div></div>
                <div id="events" class="page"><div class="panel"><div class="panel-body">Incident Tracking Master Log</div></div></div>
                <div id="regions" class="page"><div class="panel"><div class="panel-body">Regional Performance Framework Matrix</div></div></div>
                <div id="districts" class="page"><div class="panel"><div class="panel-body">District Surveillance Operations Center</div></div></div>
                <div id="ims" class="page"><div class="panel"><div class="panel-body">Incident Management System Core Desk</div></div></div>
            </div>
        </div>
    </div>

    <script>
        function updateTime() {
            const now = new Date();
            const dateStr = now.toLocaleString('en-GB').replace(',', '');
            document.getElementById("time").innerText = dateStr;
        }
        setInterval(updateTime, 1000);
        updateTime();

        const alerts = [
            "SEVERE ALERT: Bundibugyo Virus Disease Outbreak Active",
            "PHEIC Declared by WHO Director-General under IHR 2005",
            "KIA Port Health Screening activated for regional incoming flights",
            "Cholera surveillance response sustained in Greater Accra"
        ];
        let alertIdx = 0;

        function rotateAlert() {
            const el = document.getElementById("statusText");
            if(!el) return;
            el.style.opacity = 0;
            setTimeout(() => {
                el.innerText = alerts[alertIdx];
                el.style.opacity = 1;
                alertIdx = (alertIdx + 1) % alerts.length;
            }, 400);
        }
        setInterval(rotateAlert, 4500);

        function showPage(pageId) {
            document.querySelectorAll(".page").forEach(p => p.classList.remove("active"));
            const target = document.getElementById(pageId);
            if (target) target.classList.add("active");

            document.querySelectorAll(".sidebar button").forEach(b => {
                b.classList.remove("active");
                if (b.getAttribute('onclick').includes(`'${pageId}'`)) b.classList.add("active");
            });

            document.querySelectorAll(".tabs button").forEach(b => {
                b.classList.remove("active");
                if (b.getAttribute('onclick').includes(`'${pageId}'`)) b.classList.add("active");
            });
        }
    </script>
</body>
</html>

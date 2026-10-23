import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 🌟 Set clean layout configuration
st.set_page_config(
    page_title="Weather Data Analysis System Pro",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎨 Custom Premium Styling Injection
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    h1 { color: #1e3a8a; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-weight: 800; }
    h2 { color: #1e40af; font-weight: 700; }
    h3 { color: #0f172a; font-weight: 600; }
    .welcome-card {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        padding: 35px;
        border-radius: 15px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        margin-bottom: 25px;
    }
    .stAlert p { font-size: 16px !important; font-weight: 500; }
    .error-box {
        background-color: #fef2f2;
        border-left: 6px solid #dc2626;
        padding: 20px;
        border-radius: 8px;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 🏛️ GRAND ENTRY WELCOME HERO BLOCK
st.markdown("""
    <div class="welcome-card">
        <h1>🌦️ Weather Data Analysis System</h1>
        <p style="font-size: 18px; alpha: 0.9;">Welcome to the production-grade weather cleaning, preprocessing, and analytical visualization workspace.</p>
        <hr style="border-color: rgba(255,255,255,0.2);">
        <p style="font-size: 14px; font-weight: bold;">🚀 Developed by Team Leads: V.SriHasini, P.Akshara, P.Nagadevi, S.Dhanasri</p>
        <p style="font-size: 13px; alpha: 0.8;">Guided by: BHUSARAPU HEMA NAGAMANI, Assistant Professor</p>
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR CONTROL PANEL ---
st.sidebar.markdown("### ⚙️ System Controls")
temperature_scale = st.sidebar.selectbox("Preferred Temperature Scale", ["Celsius (°C)", "Fahrenheit (°F)"])
outlier_threshold = st.sidebar.slider("Maximum Temp Safety Guardrail (°C)", 40, 60, 50)

st.sidebar.divider()
st.sidebar.markdown("### 📥 Step 1: Ingest Data")
uploaded_file = st.sidebar.file_uploader("Upload your Weather Dataset (Excel or CSV format)", type=["xlsx", "csv", "xls"])

# --- CORE SYSTEM CORE ENGINE ---
if uploaded_file is None:
    # Beautiful default dynamic landing placeholder instructing the user what to do next
    st.info("### 👋 Welcome! Let's get started by feeding data into the engine.")
    st.markdown("""
    To begin cleaning and analyzing your records, please upload your weather file using the sidebar panel on the left.
    
    📋 **Your dataset should ideally contain columns tracking:**
    * **Dates** (e.g., 01-01-2024)
    * **Temperature** values
    * **Humidity** percentages
    * **Wind Speed** values
    * **Weather Conditions** (e.g., Sunny, Cloudy, Rainy)
    """)
else:
    # 🏃 Process starts immediately upon file upload
    raw_df = None
    try:
        if uploaded_file.name.endswith('.csv'):
            raw_df = pd.read_csv(uploaded_file)
        else:
            raw_df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.markdown(f"""
        <div class="error-box">
            <h3>❌ The uploaded file is corrupted or unreadable</h3>
            <p>The processing framework cannot unpack the file structure.</p>
            <p>💡 <b>How to fix this:</b> Open the document in your computer spreadsheet editor (Excel/Numbers), click 'Save As', choose standard <b>Excel Workbook (.xlsx)</b> or <b>CSV (.csv)</b>, and re-upload the new file here.</p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    # --- DATAFRAME UTILITY PRE-CHECK ---
    if raw_df is not None:
        st.markdown("## 🔍 Step 1: Intelligent Column Layout Mapping")
        
        expected_keywords = {
            'Date': ['date', 'time', 'timestamp', 'day'],
            'Temperature': ['temp', 'temperature', 'celsius', '°c', 't'],
            'Humidity': ['humidity', 'humid', 'moisture', '%'],
            'Wind': ['wind', 'speed', 'km/h', 'velocity'],
            'Condition': ['condition', 'weather', 'status', 'sky']
        }

        mapped_columns = {}
        cleaned_cols = [str(c).strip().lower() for c in raw_df.columns]
        missing_fields = []

        # Smart search map to match raw user header columns safely
        for standard_name, variants in expected_keywords.items():
            matched = None
            for i, orig_col in enumerate(raw_df.columns):
                if any(v in cleaned_cols[i] for v in variants):
                    matched = orig_col
                    break
            if matched:
                mapped_columns[standard_name] = matched
            else:
                missing_fields.append(standard_name)

        # Intercept schema errors elegantly and show human steps
        if missing_fields:
            missing_text = ", ".join([f"<b>{field}</b>" for field in missing_fields])
            st.markdown(f"""
            <div class="error-box">
                <h3>📋 Missing Essential Data Columns</h3>
                <p>The system successfully read your file, but could not detect columns representing: {missing_text}.</p>
                <p>💡 <b>How to fix this layout:</b> Ensure your file's header row contains clear names. For example, rename your temperature column header to 'Temperature', and your humidity column header to 'Humidity'. Save your file and upload it again.</p>
            </div>
            """, unsafe_allow_html=True)
            st.stop()

        # Build clean processing matrix frame safely
        try:
            process_df = pd.DataFrame()
            process_df['Raw_Date'] = raw_df[mapped_columns['Date']]
            process_df['Temp_C'] = pd.to_numeric(raw_df[mapped_columns['Temperature']], errors='coerce')
            process_df['Humidity'] = pd.to_numeric(raw_df[mapped_columns['Humidity']], errors='coerce')
            process_df['Wind_Speed'] = pd.to_numeric(raw_df[mapped_columns['Wind']], errors='coerce')
            process_df['Condition'] = raw_df[mapped_columns['Condition']].astype(str).str.strip().str.capitalize()
        except Exception as data_err:
            st.markdown("""
            <div class="error-box">
                <h3>⚠️ Data Conversion Breakdown</h3>
                <p>The system had trouble converting text values inside your numeric columns into real metrics.</p>
                <p>💡 <b>How to fix this:</b> Make sure your Temperature, Humidity, and Wind columns only contain plain numbers. Remove any letters, symbols, or text labels inside those rows.</p>
            </div>
            """, unsafe_allow_html=True)
            st.stop()

        # --- STEP 3: AUTOMATED DATA CLEANING & REPAIR PIPELINE ---
        st.markdown("## 🧼 Step 2: Automated Pipeline Repair & Metrics Sanitization")

        orig_rows = len(process_df)
        null_temps = process_df['Temp_C'].isnull().sum()
        null_hum = process_df['Humidity'].isnull().sum()

        # Execute dynamic statistical mean adjustments
        mean_temp = process_df['Temp_C'].mean() if not process_df['Temp_C'].isnull().all() else 25.0
        mean_hum = process_df['Humidity'].mean() if not process_df['Humidity'].isnull().all() else 70.0

        process_df['Temp_C'] = process_df['Temp_C'].fillna(mean_temp)
        process_df['Humidity'] = process_df['Humidity'].fillna(mean_hum)
        process_df['Wind_Speed'] = process_df['Wind_Speed'].fillna(0.0)

        # Identify environmental hardware sensor outlier values
        outlier_mask = process_df['Temp_C'] > outlier_threshold
        outlier_count = outlier_mask.sum()
        if outlier_count > 0:
            st.warning(f"⚠️ Anomaly Guardrail Triggered: Adjusted {outlier_count} extreme temperature spikes exceeding your safety threshold limit ({outlier_threshold}°C).")
            process_df.loc[outlier_mask, 'Temp_C'] = mean_temp

        # Clear duplicate rows
        duplicate_rows = process_df.duplicated().sum()
        process_df = process_df.drop_duplicates()

        # Safe DateTime parser guardrail
        process_df['Clean_Date'] = pd.to_datetime(process_df['Raw_Date'], errors='coerce')
        invalid_dates = process_df['Clean_Date'].isnull().sum()
        if invalid_dates > 0:
            st.markdown(f"""
            <div class="error-box">
                <h3>📅 Invalid Date Format Detected</h3>
                <p>The system found {invalid_dates} rows with unreadable calendar date formats.</p>
                <p>💡 <b>How to fix this:</b> Ensure all dates in your date column use standard formats like <b>YYYY-MM-DD</b> or <b>DD-MM-YYYY</b>. Blanks or non-date text cannot be processed.</p>
            </div>
            """, unsafe_allow_html=True)
            st.stop()

        # Compute conversions
        process_df['Temp_F'] = (process_df['Temp_C'] * 9/5) + 32

        # Format and display dashboard output dataset grid layout
        final_display_df = process_df[['Clean_Date', 'Temp_C', 'Temp_F', 'Humidity', 'Wind_Speed', 'Condition']].copy()
        final_display_df.columns = ['Date', 'Temperature (°C)', 'Temperature (°F)', 'Humidity (%)', 'Wind Speed (km/h)', 'Weather Condition']

        # Render Premium Scorecards
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        with kpi1:
            st.metric("Total Rows Processed", orig_rows)
        with kpi2:
            st.metric("Missing Values Imputed", int(null_temps + null_hum), delta="Fixed via Mean", delta_color="normal")
        with kpi3:
            st.metric("Duplicate Entries Removed", int(duplicate_rows))
        with kpi4:
            st.metric("Dataset Quality Health", f"{int((1 - (null_temps/orig_rows if orig_rows > 0 else 0))*100)}%")

        st.dataframe(final_display_df, use_container_width=True)

        # --- STEP 4: INTERACTIVE VISUAL ENGINE ---
        st.markdown("## 📊 Step 3: Interactive Visual Insights Engine")
        

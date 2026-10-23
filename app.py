import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 🌟 Set clean layout configuration
st.set_page_config(
    page_title="Weather Data Analysis System Pro",
    page_icon="🌦️",
    layout="wide"
)

# 🎨 Premium Custom CSS Injection for a "Grand Entry" Appearance
st.markdown("""
    <style>
    .main { background-color: #fdfefe; }
    .grand-title {
        color: #1e3a8a;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }
    .grand-subtitle {
        color: #475569;
        font-size: 18px;
        text-align: center;
        margin-bottom: 25px;
        font-style: italic;
    }
    .team-badge {
        background-color: #f1f5f9;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #2563eb;
        margin-bottom: 30px;
    }
    .step-box {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        margin-bottom: 25px;
    }
    .step-header {
        color: #0f172a;
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 15px;
        border-bottom: 2px solid #cbd5e1;
        padding-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# 🚀 GRAND ENTRY HEADER ARCHITECTURE
st.markdown("<div class='grand-title'>🌦️ Weather Data Analysis System Pro</div>", unsafe_allow_html=True)
st.markdown("<div class='grand-subtitle'>Enterprise Preprocessing, Standardization & Trend Visualization Engine</div>", unsafe_allow_html=True)

# Project Metadata Context Panel
st.markdown("""
<div class='team-badge'>
    <strong>🎓 Project Lead & Contributors:</strong> V.SriHasini (Lead), P.Akshara, P.Nagadevi, S.Dhanasri <br>
    <strong>👨‍🏫 Project Guide:</strong> BHUSARAPU HEMA NAGAMANI, Assistant Professor
</div>
""", unsafe_allow_html=True)

# --- STEP 1: CLEAN UPLOAD PORTAL ---
st.markdown("<div class='step-box'>", unsafe_allow_html=True)
st.markdown("<div class='step-header'>📂 Step 1: Upload Raw Weather Dataset</div>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Please choose an Excel (.xlsx, .xls) or CSV (.csv) weather document to initialize the platform analytics pipeline:", type=["csv", "xlsx", "xls"])

st.markdown("</div>", unsafe_allow_html=True)

# Execute framework ONLY when a file is provided by the user
if uploaded_file is None:
    st.info("💡 Welcome! The system is clean and idling safely. Please drop or upload your data file above to trigger the analysis engine interfaces.")
else:
    # Safe File Ingestion Wrapper
    try:
        if uploaded_file.name.endswith('.csv'):
            raw_df = pd.read_csv(uploaded_file)
        else:
            raw_df = pd.read_excel(uploaded_file)
    except Exception:
        st.error("### ❌ Human Readable Notification: The document format is corrupted.")
        st.markdown("💡 **Action Step:** Open the file on your local device using Excel, click 'Save As', select regular `.csv` or `.xlsx` format, and upload that newly saved copy.")
        st.stop()

    # Dynamic Raw Data Display Block
    st.markdown("<div class='step-box'>", unsafe_allow_html=True)
    st.markdown("<div class='step-header'>📋 Step 2: Ingested File Data Grid Preview</div>", unsafe_allow_html=True)
    st.markdown("Here is a sample view of the columns and data rows discovered inside your uploaded document:")
    st.dataframe(raw_df.head(10), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # --- STEP 2: INTERACTIVE PIPELINE EXECUTION BUTTON ---
    st.markdown("<div class='step-box'>", unsafe_allow_html=True)
    st.markdown("<div class='step-header'>⚙️ Step 3: Analytics Optimization Engine</div>", unsafe_allow_html=True)
    st.markdown("Click the execution button below to parse, auto-clean anomalies, standardize scale units, and compile trend metrics.")
    
    # User must explicitly click this button to show the next steps
    trigger_analysis = st.button("🚀 Analyze & Generate Visualizations", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if trigger_analysis:
        st.markdown("<div class='step-box'>", unsafe_allow_html=True)
        st.markdown("<div class='step-header'>🧼 Step 4: Automated Pipeline Quality Optimization & Diagnostics</div>", unsafe_allow_html=True)
        
        # Build processing layout securely
        clean_df = raw_df.copy()
        
        # Track pipeline changes for user diagnostics
        original_row_count = len(clean_df)
        duplicate_count = clean_df.duplicated().sum()
        
        # Execute automated repairs
        clean_df = clean_df.drop_duplicates()
        
        # Dynamically separate numerical data columns from categorical blocks safely
        numeric_cols = clean_df.select_dtypes(include=[np.number]).columns.tolist()
        text_cols = clean_df.select_dtypes(exclude=[np.number]).columns.tolist()
        
        repaired_cells = 0
        for col in numeric_cols:
            null_mask = clean_df[col].isnull()
            null_count = null_mask.sum()
            if null_count > 0:
                col_mean = clean_df[col].mean() if not clean_df[col].isnull().all() else 0.0
                clean_df[col] = clean_df[col].fillna(col_mean)
                repaired_cells += null_count

        # Display performance logs
        st.success("✅ Operational pipelines completed smoothly with zero critical code breakdown exceptions!")
        
        diag_c1, diag_c2, diag_c3 = st.columns(3)
        with diag_c1:
            st.metric("Total Records Ingested", original_row_count)
        with diag_c2:
            st.metric("Duplicate Entries Removed", int(duplicate_count))
        with diag_c3:
            st.metric("Missing Data Fields Restored", int(repaired_cells))
            
        # Automated Conversions Logic: Scan for any temperature field to calculate Fahrenheit alternatives safely
        temp_col_found = None
        for col in numeric_cols:
            if 'temp' in col.lower() or '°c' in col.lower() or 'celsius' in col.lower():
                temp_col_found = col
                break
                
        if temp_col_found:
            clean_df['Temperature (°F)'] = (clean_df[temp_col_found] * 9/5) + 32
            st.info(f"✨ Custom Feature Engineering Active: Detected temperature source column '{temp_col_found}' and computed scaled mathematical conversions into 'Temperature (°F)' safely.")
            
        st.markdown("#### Standardized Processed Output Data Matrix Grid Layout")
        st.dataframe(clean_df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # --- STEP 3: VISUAL CHARTS INTERFACE ---
        st.markdown("<div class='step-box'>", unsafe_allow_html=True)
        st.markdown("<div class='step-header'>📊 Step 5: Production Analytics Data Dashboards</div>", unsafe_allow_html=True)
        
        chart_layout_col1, chart_layout_col2 = st.columns(2)
        
        with chart_layout_col1:
            if temp_col_found:
                st.markdown("📈 **Chronological Metric Trend Line Profiling**")
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.plot(clean_df.index, clean_df[temp_col_found], marker='o', color='#2563eb', linewidth=2.5, linestyle='-')
                ax.set_title(f"Sequential Evaluation Profile: {temp_col_found}", fontweight='bold', fontsize=12)
                ax.set_xlabel("Observation Record Index Row Sequence")
                ax.set_ylabel(temp_col_found)
                ax.grid(True, linestyle=':', alpha=0.6)
                sns.despine()
                st.pyplot(fig)
            else:
                st.info("ℹ️ Note: No specific temperature tracking column detected to map visual line charts.")
                
        with chart_layout_col2:
            if len(numeric_cols) > 0:
                target_dist_col = numeric_cols[-1]
                st.markdown(f"📊 **Distribution Analytics: {target_dist_col}**")
                fig, ax = plt.subplots(figsize=(10, 5))
                sns.histplot(data=clean_df, x=target_dist_col, kde=True, color='#0d9488', ax=ax)
                ax.set_title(f"Density Range Diagnostics: {target_dist_col}", fontweight='bold', fontsize=12)
                sns.despine()
                st.pyplot(fig)
            else:
                st.info("ℹ️ Note: No numerical fields available to map distribution histograms.")
                
        # Categorical Volume Block
        if len(text_cols) > 0:
            st.divider()
            target_txt_col = text_cols[0]
            st.markdown(f"🗂️ **Categorical Volumetric Distributions: {target_txt_col}**")
            fig, ax = plt.subplots(figsize=(12, 4))
            sns.countplot(data=clean_df, x=target_txt_col, palette='Blues_r', ax=ax)
            ax.set_title(f"Log Volume Frequencies Per Discovered State: {target_txt_col}", fontweight='bold')
            sns.despine()
            st.pyplot(fig)
            
        st.markdown("</div>", unsafe_allow_html=True)

        # --- STEP 4: DATA EXPORT PORTAL ---
        st.markdown("<div class='step-box'>", unsafe_allow_html=True)
        st.markdown("<div class='step-header'>💾 Step 6: Secure Data Persistence Pipeline Export</div>", unsafe_allow_html=True)
        
        csv_export_bytes = clean_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Cleanized System Production File (final_weather_analytics.csv)",
            data=csv_export_bytes,
            file_name="final_weather_analytics.csv",
            mime="text/csv",
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)


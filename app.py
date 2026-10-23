import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Set website configurations
st.set_page_config(page_title="Weather Data Analysis System", layout="wide")

# App Header & Branding
st.title("🌦️ Weather Data Analysis System")
st.markdown("### Data cleaning, temperature analysis, and visualization platform")
st.write("**Project Team:** V. SriHasini (Lead), P. Akshara, P. Nagadevi, S. Dhanasri | **Guide:** Bhusarapu Hema Nagamani")
st.markdown("---")

# Sidebar for file upload
st.sidebar.header("📁 Upload Weather Dataset")
uploaded_file = st.sidebar.file_uploader("Upload your Excel (.xlsx) or CSV file", type=["xlsx", "csv"])

if uploaded_file is not None:
    try:
        # 1. LOAD DATASET
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.success("🎉 Dataset loaded successfully!")
        
        # Tabs for different pipeline stages
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Raw Data Summary", "⚙️ Data Cleaning & Processing", "📊 Visual Trends", "💾 Export Analytics"])
        
        with tab1:
            st.subheader("Raw Dataset Preview")
            st.dataframe(df.head())
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Dataset Shape:**", df.shape)
            with col2:
                st.write("**Missing Values Checklist:**")
                st.write(df.isnull().sum())

        with tab2:
            st.subheader("Executing Pipeline Transformations...")
            
            # --- Pipeline Step: Renaming Columns for Standardization ---
            if len(df.columns) >= 5:
                df.columns = ['Date', 'Temperature_C', 'Humidity', 'Wind_Speed', 'Condition'] + list(df.columns[5:])
                st.info("🔄 Column names standardized.")
            
            # --- Pipeline Step: Handle Missing Values ---
            if 'Temperature_C' in df.columns:
                df['Temperature_C'] = pd.to_numeric(df['Temperature_C'], errors='coerce')
                df['Temperature_C'] = df['Temperature_C'].fillna(df['Temperature_C'].mean())
            if 'Humidity' in df.columns:
                df['Humidity'] = pd.to_numeric(df['Humidity'], errors='coerce')
                df['Humidity'] = df['Humidity'].fillna(df['Humidity'].mean())
            st.info("🛠️ Missing values filled using column mean imputation.")
            
            # --- Pipeline Step: Remove Duplicates ---
            initial_shape = df.shape
            df = df.drop_duplicates()
            if df.shape < initial_shape:
                st.info(f"🗑️ Removed {initial_shape - df.shape} duplicate records.")
            else:
                st.info("✅ No duplicate records found.")
                
            # --- Pipeline Step: Date Conversion ---
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.strftime('%d-%m-%Y')
            st.info("📅 Date column formatted to DateTime structure.")

            # --- Pipeline Step: Unit Conversion (Feature Engineering) ---
            if 'Temperature_C' in df.columns:
                df['Temperature (°F)'] = (df['Temperature_C'] * 9/5) + 32
                st.info("🌡️ Temperature engineered from Celsius to Fahrenheit.")
            
            st.success("✨ Data Cleaning & Preprocessing Pipeline Complete!")
            st.subheader("Processed Clean Dataset Preview")
            st.dataframe(df)
            
            st.markdown("### 📈 Descriptive Statistical Insights")
            st.dataframe(df.describe())

        with tab3:
            st.subheader("Interactive Climate Visualizations")
            
            # Figure 1: Line Chart for Temperature Fluctuations
            if 'Date' in df.columns and 'Temperature_C' in df.columns:
                st.markdown("#### 📉 Time-Series Temperature Trend Analysis")
                fig1, ax1 = plt.subplots(figsize=(10, 4))
                ax1.plot(df['Date'], df['Temperature_C'], marker='o', color='#d62728', linewidth=2)
                ax1.set_title('Daily Temperature Fluctuations over Time', fontsize=12, fontweight='bold')
                ax1.set_xlabel('Observation Date')
                ax1.set_ylabel('Temperature (°C)')
                ax1.grid(True, linestyle='--', alpha=0.5)
                plt.xticks(rotation=45)
                st.pyplot(fig1)
            
            col_viz1, col_viz2 = st.columns(2)
            with col_viz1:
                if 'Condition' in df.columns:
                    st.markdown("#### 📊 Categorical Distribution of Weather Conditions")
                    fig2, ax2 = plt.subplots(figsize=(6, 4))
                    sns.countplot(x='Condition', data=df, palette='Set2', ax=ax2)
                    ax2.set_title('Frequency Distribution of Climatic Conditions', fontsize=10, fontweight='bold')
                    ax2.set_xlabel('Weather Type')
                    ax2.set_ylabel('Number of Days')
                    st.pyplot(fig2)
                    
            with col_viz2:
                if 'Humidity' in df.columns:
                    st.markdown("#### 🌊 Humidity Level Distribution Analysis")
                    fig3, ax3 = plt.subplots(figsize=(6, 4))
                    sns.histplot(df['Humidity'], kde=True, color='teal', bins=5, ax=ax3)
                    ax3.set_title('Humidity Density Spread & Range Detection', fontsize=10, fontweight='bold')
                    ax3.set_xlabel('Humidity (%)')
                    ax3.set_ylabel('Frequency')
                    st.pyplot(fig3)

        with tab4:
            st.subheader("Downstream Readiness Export")
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download final_weather_analytics.csv",
                data=csv_data,
                file_name="final_weather_analytics.csv",
                mime="text/csv",
            )
            st.balloons()
            
    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
else:
    st.info("💡 Please upload an Excel or CSV file in the sidebar to run the Data Cleaning Pipeline.")

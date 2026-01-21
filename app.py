"""
Business Segmenter - Main Application
A comprehensive tool for customer segmentation and market basket analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import sys
import os

#Add utils to path
sys.path.append(os.path.dirname(__file__))

from utils.data_generator import generate_demo_data
from assets.styles import get_custom_css
from components.sidebar import render_sidebar
from components.overview_dashboard import render_overview_dashboard
from components.smart_bundles import render_smart_bundles
from components.customer_segments import render_customer_segments
from components.marketing_assistant import render_marketing_assistant

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Smart Business Segmenter",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'data_analyzed' not in st.session_state:
    st.session_state.data_analyzed = False
if 'uploaded_file_name' not in st.session_state:
    st.session_state.uploaded_file_name = None

# --- TITLE ---
st.markdown("""
<div style='text-align: center; padding: 20px 0;'>
    <h1 style='font-size: 3em; margin-bottom: 0;'>Business Segmenter</h1>
</div>
""", unsafe_allow_html=True)

# --- LOAD OR GENERATE DATA (before sidebar to enable smart mode) ---
@st.cache_data
def load_data(uploaded_file):
    """Load data from file or generate demo data with validation"""
    if uploaded_file is None:
        df = generate_demo_data(n_transactions=600, n_customers=60, n_days=45)
        return df, True, None
    else:
        try:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file)
            
            # Validate required columns - ALL columns are now required
            required_columns = ['Date', 'UserID', 'ProductID', 'Amount', 'TransactionID']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                error_msg = f"Missing required columns: {', '.join(missing_columns)}"
                return None, False, error_msg
            
            # Validate data is not empty
            if len(df) == 0:
                return None, False, "CSV file is empty. Please upload a file with transaction data."
            
            # Convert date column
            try:
                df['Date'] = pd.to_datetime(df['Date'])
            except Exception as e:
                return None, False, f"Invalid date format in 'Date' column. Please use YYYY-MM-DD format. Error: {str(e)}"
            
            # Validate Amount column contains numeric values
            try:
                df['Amount'] = pd.to_numeric(df['Amount'])
            except Exception as e:
                return None, False, f"Invalid amount values in 'Amount' column. Please ensure all amounts are numbers. Error: {str(e)}"
            
            return df, False, None
            
        except pd.errors.EmptyDataError:
            return None, False, "CSV file is empty or corrupted."
        except pd.errors.ParserError as e:
            return None, False, f"Error parsing CSV file. Please check the file format. Error: {str(e)}"
        except Exception as e:
            return None, False, f"Error loading file: {str(e)}"

# Pre-load data to check if we have an uploaded file
if st.session_state.uploaded_file_name: # Check if a file name was previously stored
    # There's an uploaded file, load it from session state
    temp_df, temp_is_demo, temp_error = load_data(st.session_state.get('temp_uploaded_file'))
else:
    # Load demo data for smart mode calculation
    temp_df, temp_is_demo, temp_error = load_data(None)

# --- SIDEBAR (now with data for smart mode) ---
uploaded_file, min_support, min_confidence, n_clusters = render_sidebar(temp_df)

# Store uploaded file in session state for reload
if uploaded_file:
    st.session_state.temp_uploaded_file = uploaded_file
    st.session_state.uploaded_file_name = uploaded_file.name # Store name for persistence check
else:
    # If file is cleared, clear session state
    st.session_state.temp_uploaded_file = None
    st.session_state.uploaded_file_name = None

# Now load the actual data with the uploaded file
df, is_demo, error_msg = load_data(uploaded_file)

# Handle errors from CSV upload
if error_msg:
    st.error(f"**Error Loading CSV File**")
    st.error(error_msg)
    st.info("""
    **Required CSV Format:**
    
    Your CSV file must contain ALL these columns:
    - **Date** - Transaction date (YYYY-MM-DD format)
    - **UserID** - Customer identifier
    - **ProductID** - Product name or ID
    - **Amount** - Transaction amount (numeric)
    - **TransactionID** - Unique transaction identifier
    
    **Example:**
    ```
    Date,UserID,ProductID,Amount,TransactionID
    2024-01-15,CUST001,PROD123,299.99,TXN001
    2024-01-15,CUST001,PROD456,149.99,TXN001
    2024-01-16,CUST002,PROD123,299.99,TXN002
    ```
    """)
    st.stop()

# Display data info banner or analyze prompt
# Auto-analyze demo data, but require button click for uploaded data
if not st.session_state.data_analyzed:
    if is_demo:
        # Automatically show demo data insights without requiring button click
        st.session_state.data_analyzed = True
    else:
        # For uploaded data, require the analyze button click
        st.success(f"**Data Loaded Successfully** - {len(df):,} transactions from {df['UserID'].nunique()} customers. Click 'Analyze Data' to proceed!")
        st.stop()

# --- MAIN ANALYSIS (Only show when analyzed) ---
# If we reach here, data_analyzed is True
# Navigation
st.markdown("<br>", unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Overview Dashboard",
    "Smart Bundles",
    "Customer Segments",
    "Marketing Assistant"
])

# ============================================
# TAB 1: OVERVIEW DASHBOARD
# ============================================
with tab1:
    render_overview_dashboard(df)

# ============================================
# TAB 2: SMART BUNDLES
# ============================================
with tab2:
    render_smart_bundles(df, min_support, min_confidence)

# ============================================
# TAB 3: CUSTOMER SEGMENTS
# ============================================
with tab3:
    customer_metrics, segment_profiles, segment_insights = render_customer_segments(df, n_clusters)

# ============================================
# TAB 4: MARKETING ASSISTANT
# ============================================
with tab4:
    render_marketing_assistant(df, customer_metrics)
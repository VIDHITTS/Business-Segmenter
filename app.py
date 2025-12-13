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
    """Load data from file or generate demo data"""
    if uploaded_file is None:
        df = generate_demo_data(n_transactions=600, n_customers=60, n_days=45)
        return df, True
    else:
        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file)
        
        # Auto-detect and create missing columns
        if 'TransactionID' not in df.columns:
            df['TransactionID'] = df.groupby(['Date', 'UserID']).ngroup() + 1
        
        if 'Amount' not in df.columns:
            df['Amount'] = np.random.randint(20, 500, size=len(df))
        
        df['Date'] = pd.to_datetime(df['Date'])
        return df, False

# Pre-load data to check if we have an uploaded file
if st.session_state.uploaded_file_name: # Check if a file name was previously stored
    # There's an uploaded file, load it from session state
    temp_df, temp_is_demo = load_data(st.session_state.get('temp_uploaded_file'))
else:
    # Load demo data for smart mode calculation
    temp_df, temp_is_demo = load_data(None)

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
df, is_demo = load_data(uploaded_file)

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

"""Sidebar component for data upload and settings"""
import streamlit as st
import pandas as pd


def calculate_smart_parameters(df):
    """
    Automatically calculate optimal parameters based on data characteristics
    
    Args:
        df: Transaction DataFrame
    
    Returns:
        tuple: (min_support, min_confidence, n_clusters)
    """
    # Get data characteristics
    n_transactions = df['TransactionID'].nunique()
    n_customers = df['UserID'].nunique()
    n_products = df['ProductID'].nunique()
    
    # Calculate average basket size
    avg_items_per_transaction = df.groupby('TransactionID').size().mean()
    
    # Calculate data sparsity (how diverse the purchases are)
    total_possible_combinations = n_transactions * n_products
    actual_transactions = len(df)
    sparsity = actual_transactions / total_possible_combinations if total_possible_combinations > 0 else 0
    
    # Smart support calculation based on transaction count AND sparsity
    if n_transactions < 50:
        min_support = 0.15  # 15% for very small datasets
        support_reason = "Small dataset (<50 txn)"
    elif n_transactions < 200:
        min_support = 0.08  # 8% for small datasets
        support_reason = "Small dataset (<200 txn)"
    elif n_transactions < 500:
        min_support = 0.04  # 4% for medium datasets
        support_reason = "Medium dataset (<500 txn)"
    else:
        # For larger datasets, adjust based on sparsity
        if sparsity < 0.01:  # Very sparse data
            min_support = 0.02
            support_reason = "High product diversity"
        else:
            min_support = 0.03
            support_reason = "Standard dataset size"
    
    # Smart confidence based on average basket size
    if avg_items_per_transaction < 2:
        min_confidence = 0.50  # Lower confidence for small baskets
        conf_reason = "Small avg basket size"
    elif avg_items_per_transaction < 4:
        min_confidence = 0.60  # Standard confidence
        conf_reason = "Avg basket size"
    else:
        min_confidence = 0.70  # Higher confidence for large baskets
        conf_reason = "Large avg basket size"
    
    # Smart cluster calculation using Elbow method heuristic
    if n_customers < 20:
        n_clusters = 2
        cluster_reason = "Small customer base"
    elif n_customers < 50:
        n_clusters = 3
        cluster_reason = "Growing customer base"
    elif n_customers < 150:
        n_clusters = 4
        cluster_reason = "Medium customer base"
    else:
        n_clusters = 5
        cluster_reason = "Large customer base"
    
    return min_support, min_confidence, n_clusters, support_reason, conf_reason, cluster_reason


def render_sidebar(df=None):
    """
    Render sidebar with data upload and analysis settings
    
    Args:
        df: Optional DataFrame for smart parameter calculation
    
    Returns:
        tuple: (uploaded_file, min_support, min_confidence, n_clusters)
    """
    with st.sidebar:
        st.markdown("### Data Upload")
        st.markdown("Upload your CSV file with:")
        st.markdown("• **Date** - Transaction date")
        st.markdown("• **UserID** - Customer identifier")
        st.markdown("• **ProductID** - Product name/ID")
        
        uploaded_file = st.file_uploader(
            "Drop your CSV file here",
            type=["csv"],
            help="Upload transaction data for analysis"
        )
        
        # Check if file changed
        if uploaded_file is not None:
            if st.session_state.uploaded_file_name != uploaded_file.name:
                st.session_state.data_analyzed = False
                st.session_state.uploaded_file_name = uploaded_file.name
        
        st.markdown("---")
        
        # Settings
        st.markdown("### Analysis Settings")
        
        # Smart Auto mode toggle
        use_smart_mode = st.toggle(
            "Smart Auto Mode",
            value=True,
            help="Automatically select best parameters for your data. Turn off for manual control."
        )
        
        if use_smart_mode:
            if df is not None:
                # Calculate smart parameters once
                min_support, min_confidence, n_clusters, s_reason, c_reason, k_reason = calculate_smart_parameters(df)
                
                # Display the calculated parameters
                st.success("**Smart Parameters Selected:**")
                
                st.markdown(f"""<div style="font-size: 0.9em; color: #4a5568;">
<strong>Bundle Support: {int(min_support * 100)}%</strong><br>
<span style="color: #718096; font-size: 0.9em;">ℹ️ <em>{s_reason}</em></span><br><br>

<strong>Confidence: {int(min_confidence * 100)}%</strong><br>
<span style="color: #718096; font-size: 0.9em;">ℹ️ <em>{c_reason}</em></span><br><br>

<strong>Segments: {n_clusters} groups</strong><br>
<span style="color: #718096; font-size: 0.9em;">ℹ️ <em>{k_reason}</em></span>
</div>""", unsafe_allow_html=True)
                
            else:
                # No data yet
                st.warning("Load data to enable Smart Auto mode")
                min_support = 0.05
                min_confidence = 0.60
                n_clusters = 3
        else:
            # Manual mode - show sliders
            min_support = st.slider(
                "Bundle Support %",
                min_value=1,
                max_value=20,
                value=5,
                help="Minimum percentage of transactions where products appear together to be considered a bundle"
            ) / 100
            
            min_confidence = st.slider(
                "Bundle Confidence %",
                min_value=30,
                max_value=100,
                value=60,
                help="Likelihood that customers who buy the first product will also buy the second product"
            ) / 100
            
            n_clusters = st.slider(
                "Customer Segments",
                min_value=2,
                max_value=5,
                value=3,
                help="Number of customer segments to create"
            )
        
        st.markdown("---")
        
        # Analyze Button
        if st.button("Analyze Data", type="primary", use_container_width=True):
            st.session_state.data_analyzed = True
            st.rerun()
        
        st.markdown("---")
        
        # Quick Stats
        st.markdown("### Quick Info")
        if uploaded_file:
            st.success("Custom data loaded")
        else:
            st.info("Using demo data")
    
    return uploaded_file, min_support, min_confidence, n_clusters


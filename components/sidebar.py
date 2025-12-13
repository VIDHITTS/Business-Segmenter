"""Sidebar component for data upload and settings"""
import streamlit as st


def render_sidebar():
    """
    Render sidebar with data upload and analysis settings
    
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

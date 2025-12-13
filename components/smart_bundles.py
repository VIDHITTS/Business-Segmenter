"""Smart Bundles component for market basket analysis"""
import streamlit as st
import plotly.express as px
from utils.market_basket import prepare_basket_data, find_product_bundles, calculate_bundle_revenue_potential


def render_smart_bundles(df, min_support, min_confidence):
    """
    Render smart bundles analysis tab
    
    Args:
        df: Transaction DataFrame
        min_support: Minimum support threshold
        min_confidence: Minimum confidence threshold
    """
    st.markdown('<div class="animated">', unsafe_allow_html=True)
    st.markdown("### Product Bundle Analysis")
    st.markdown("Discover which products are frequently purchased together using **Apriori Algorithm**")
    
    with st.spinner("Analyzing product combinations..."):
        basket_sets = prepare_basket_data(df)
        frequent_itemsets, rules = find_product_bundles(basket_sets, min_support, min_confidence)
    
    if not rules.empty:
        st.success(f"Found **{len(rules)}** product bundle opportunities!")
        
        # Revenue Potential
        st.markdown("### Revenue Opportunity Analysis")
        revenue_potential = calculate_bundle_revenue_potential(df, rules)
        
        if not revenue_potential.empty:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_potential = revenue_potential['potential_revenue'].sum()
                st.metric(
            label="Potential Additional Revenue",
            value=f"₹{total_potential:,.2f}",
            delta=f"From {len(rules)} bundles"
        )
            with col2:
                avg_potential = revenue_potential['potential_revenue'].mean()
                st.metric("Avg per Bundle", f"₹{avg_potential:,.0f}")
            
            with col3:
                top_bundle_revenue = revenue_potential.iloc[0]['potential_revenue']
                st.metric("Top Bundle Potential", f"₹{top_bundle_revenue:,.0f}")
            
            st.markdown("<br>", unsafe_allow_html=True)
        
        # Top Bundles Display
        st.markdown("### Recommended Product Bundles")
        
        for idx, row in rules.head(8).iterrows():
            col1, col2 = st.columns([3, 1])
            
            # Get potential revenue from the revenue_potential dataframe if available
            if idx < len(revenue_potential):
                potential = revenue_potential.iloc[idx]['potential_revenue']
            else:
                potential = 0.0
            
            with col1:
                st.markdown(f"""
                <div class="bundle-card">
                    <h4>{idx + 1}. {row['antecedents_str']} + {row['consequents_str']}</h4>
                    <span class="bundle-label">₹{potential:,.2f} Revenue</span>
                    <p style="margin: 10px 0 5px 0; color: #4a5568;">
                        <strong>When customers buy:</strong> {row['antecedents_str']}<br>
                        <strong>They also buy:</strong> {row['consequents_str']} <span class="badge badge-success">{row['confidence_pct']}% of the time</span>
                    </p>
                    <div style="margin-top: 15px;">
                        <span class="badge badge-info">Support: {row['support_pct']}%</span>
                        <span class="badge badge-info">Lift: {row['lift_score']}x</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Progress bar for confidence
                st.markdown(f"""
                <div style="margin-top: 25px;">
                    <p style="font-size: 0.9em; color: #718096; margin-bottom: 5px;">Confidence</p>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {row['confidence_pct']}%;">
                            {row['confidence_pct']}%
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Detailed Table
        with st.expander("View All Bundle Details"):
            display_df = rules[['antecedents_str', 'consequents_str', 'confidence_pct', 'lift_score', 'support_pct']].copy()
            display_df.columns = ['Product(s) A', 'Product(s) B', 'Confidence %', 'Lift', 'Support %']
            st.dataframe(display_df, use_container_width=True, height=400)
        
        # Visualization
        st.markdown("### Bundle Confidence Visualization")
        
        top_bundles = rules.head(10).copy()
        top_bundles['Bundle'] = top_bundles['antecedents_str'] + ' → ' + top_bundles['consequents_str']
        
        fig = px.bar(top_bundles, y='Bundle', x='confidence_pct',
                    orientation='h',
                    color='lift_score',
                    color_continuous_scale='Viridis',
                    labels={'confidence_pct': 'Confidence %', 'Bundle': '', 'lift_score': 'Lift Score'},
                    title='Top 10 Product Bundles by Confidence')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter, sans-serif'),
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.warning(f"No bundles found with the current thresholds. Try adjusting the settings in the sidebar.")
        st.info("**Tip:** Lower the Support % or Confidence % to discover more patterns.")
    
    st.markdown('</div>', unsafe_allow_html=True)

"""Customer Segments component for segmentation analysis"""
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.segmentation import calculate_customer_metrics, segment_customers, get_segment_insights


def render_customer_segments(df, n_clusters):
    """
    Render customer segmentation analysis tab
    
    Args:
        df: Transaction DataFrame
        n_clusters: Number of customer segments
    
    Returns:
        tuple: (customer_metrics, segment_profiles, segment_insights)
    """
    st.markdown('<div class="animated">', unsafe_allow_html=True)
    st.markdown("### Customer Segmentation Analysis")
    st.markdown("Understand your customers through **K-Means clustering** and **RFM analysis**")
    
    with st.spinner("Analyzing customer behavior..."):
        customer_metrics = calculate_customer_metrics(df)
        customer_metrics, segment_profiles = segment_customers(customer_metrics, n_clusters)
        segment_insights = get_segment_insights(customer_metrics, df)
    
    st.success(f"Customers segmented into **{n_clusters}** distinct groups!")
    
    # Segment Overview
    st.markdown("### Segment Overview")
    
    cols = st.columns(n_clusters)
    
    for idx, (segment_name, insights) in enumerate(segment_insights.items()):
        with cols[idx]:
            st.markdown(f"""
            <div class="segment-card">
                <div class="segment-title">{segment_name}</div>
                <div class="stat-item">
                    <div class="stat-label">Customers</div>
                    <div class="stat-value">{insights['size']}</div>
                </div>
                <div class="stat-item" style="margin-top: 10px;">
                    <div class="stat-label">Total Revenue</div>
                    <div class="stat-value">₹{insights['total_revenue']:,.0f}</div>
                </div>
                <div class="stat-item" style="margin-top: 10px;">
                    <div class="stat-label">Avg Spend</div>
                    <div class="stat-value">₹{insights['avg_spend_per_customer']:,.0f}</div>
                </div>
                <div class="stat-item" style="margin-top: 10px;">
                    <div class="stat-label">Contribution</div>
                    <div class="stat-value">{insights['revenue_contribution']:.1f}%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Segment Distribution")
        
        segment_sizes = customer_metrics['SegmentName'].value_counts()
        fig = px.pie(values=segment_sizes.values, names=segment_sizes.index,
                    title='Customer Distribution by Segment',
                    color_discrete_sequence=px.colors.sequential.Purples_r)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter, sans-serif')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Revenue Contribution")
        
        revenue_by_segment = []
        for segment_name, insights in segment_insights.items():
            revenue_by_segment.append({
                'Segment': segment_name,
                'Revenue': insights['total_revenue']
            })
        revenue_df = pd.DataFrame(revenue_by_segment)
        
        fig2 = px.bar(revenue_df, x='Segment', y='Revenue',
                     title='Total Revenue by Segment',
                     color='Revenue',
                     color_continuous_scale='Blues')
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter, sans-serif'),
            showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # 3D Scatter
    st.markdown("### Customer Segments in 3D Space")
    
    fig3d = px.scatter_3d(customer_metrics,
                         x='Recency', y='Frequency', z='TotalSpend',
                         color='SegmentName',
                         title='Customer Segmentation (3D Visualization)',
                         labels={
                             'TotalSpend': 'Total Spend (₹)',
                             'Frequency': 'Purchase Frequency',
                             'Recency': 'Recency (Days Ago)'
                         },
                         hover_data=['UserID'],
                         color_discrete_sequence=px.colors.qualitative.Set3)
    fig3d.update_layout(
        scene=dict(
            xaxis=dict(title='Recency', backgroundcolor="rgba(0,0,0,0)", gridcolor='#BDDDFC', showbackground=True, tickfont=dict(color='#384959'), title_font=dict(color='#384959')),
            yaxis=dict(title='Frequency', backgroundcolor="rgba(0,0,0,0)", gridcolor='#BDDDFC', showbackground=True, tickfont=dict(color='#384959'), title_font=dict(color='#384959')),
            zaxis=dict(title='Monetary', backgroundcolor="rgba(0,0,0,0)", gridcolor='#BDDDFC', showbackground=True, tickfont=dict(color='#384959'), title_font=dict(color='#384959')),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        font=dict(color='#384959')
    )
    st.plotly_chart(fig3d, use_container_width=True)
    
    # Segment Details
    st.markdown("### Detailed Segment Insights")
    
    for segment_name, insights in segment_insights.items():
        with st.expander(f"{segment_name} - Detailed Analysis"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Key Metrics")
                st.metric("Number of Customers", f"{insights['size']}")
                st.metric("Total Revenue Generated", f"₹{insights['total_revenue']:,.2f}")
                st.metric("Average Spend per Customer", f"₹{insights['avg_spend_per_customer']:,.2f}")
                st.metric("Purchase Frequency", f"{insights['avg_frequency']:.1f} transactions")
            
            with col2:
                st.markdown("#### Top Products")
                for product, count in list(insights['top_products'].items())[:5]:
                    st.markdown(f"**{product}**: {count} purchases")
                
                st.markdown(f"**Avg Items per Transaction**: {insights['avg_items_per_transaction']:.1f}")
                st.markdown(f"**Revenue Contribution**: {insights['revenue_contribution']:.1f}%")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return customer_metrics, segment_profiles, segment_insights

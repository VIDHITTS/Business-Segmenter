"""Overview Dashboard component"""
import streamlit as st
import plotly.express as px


def render_overview_dashboard(df):
    """
    Render overview dashboard with key metrics and charts
    
    Args:
        df: Transaction DataFrame
    """
    st.markdown('<div class="animated">', unsafe_allow_html=True)
    
    # Key Metrics Row
    st.markdown("### Key Performance Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_transactions = df['TransactionID'].nunique()
    total_customers = df['UserID'].nunique()
    total_products = df['ProductID'].nunique()
    total_revenue = df['Amount'].sum()
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <p>Total Transactions</p>
            <h3>{total_transactions:,}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #88BDF2 0%, #6A89A7 100%);">
            <p>Unique Customers</p>
            <h3>{total_customers:,}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #6A89A7 0%, #384959 100%);">
            <p>Product Catalog</p>
            <h3>{total_products:,}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="revenue-card">
            <p>Total Revenue</p>
            <h3>₹{total_revenue:,.0f}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Additional Insights
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Revenue Insights")
        
        avg_transaction_value = df.groupby('TransactionID')['Amount'].sum().mean()
        avg_items_per_transaction = df.groupby('TransactionID').size().mean()
        avg_customer_value = df.groupby('UserID')['Amount'].sum().mean()
        
        st.metric("Average Transaction Value", f"₹{avg_transaction_value:.2f}")
        st.metric("Avg Items per Transaction", f"{int(round(avg_items_per_transaction))}")
        st.metric("Avg Customer Lifetime Value", f"₹{avg_customer_value:.2f}")
    
    with col2:
        st.markdown("### Time-based Insights")
        
        date_range = (df['Date'].max() - df['Date'].min()).days
        daily_avg_transactions = total_transactions / max(date_range, 1)
        daily_avg_revenue = total_revenue / max(date_range, 1)
        
        st.metric("Data Range (Days)", f"{date_range}")
        st.metric("Avg Daily Transactions", f"{int(round(daily_avg_transactions))}")
        st.metric("Avg Daily Revenue", f"₹{daily_avg_revenue:.2f}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Transaction Timeline")
        
        daily_transactions = df.groupby(df['Date'].dt.date).agg({
            'TransactionID': 'nunique',
            'Amount': 'sum'
        }).reset_index()
        daily_transactions.columns = ['Date', 'Transactions', 'Revenue']
        
        fig2 = px.line(
            daily_transactions,
            x='Date',
            y='Transactions',
            title='Daily Transaction Volume',
            markers=True
        )
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter, sans-serif', color='#384959'),
            xaxis=dict(showgrid=False, color='#384959', tickfont=dict(color='#384959')),
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', color='#384959', tickfont=dict(color='#384959')),
            hovermode="x unified"
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        st.markdown("### Top Performing Products")
        
        top_products = df.groupby('ProductID').agg({
            'TransactionID': 'nunique',
            'Amount': 'sum'
        }).reset_index()
        top_products.columns = ['Product', 'Times Sold', 'Total Revenue']
        top_products = top_products.sort_values('Total Revenue', ascending=False).head(10)
        
        fig3 = px.bar(
            top_products.head(10).sort_values('Total Revenue', ascending=True),
            x='Total Revenue',
            y='Product',
            orientation='h',
            title='Top 10 Products by Revenue (₹)',
            color='Total Revenue',
            color_continuous_scale=['#BDDDFC', '#88BDF2', '#6A89A7', '#384959']
        )
        fig3.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter, sans-serif', color='#384959'),
            xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', color='#384959', tickfont=dict(color='#384959')),
            yaxis=dict(showgrid=False, color='#384959', tickfont=dict(color='#384959')),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    
    # Raw Data
    with st.expander("View Raw Transaction Data"):
        st.dataframe(df.head(100), use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

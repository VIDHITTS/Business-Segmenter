"""Marketing Assistant component for campaign generation"""
import streamlit as st
import numpy as np


def render_marketing_assistant(df, customer_metrics):
    """
    Render marketing assistant tab for campaign generation
    
    Args:
        df: Transaction DataFrame
        customer_metrics: Customer metrics DataFrame with segments
    """
    st.markdown('<div class="animated">', unsafe_allow_html=True)
    st.markdown("### AI-Powered Marketing Campaign Generator")
    st.markdown("Create personalized marketing campaigns based on customer segments and purchase behavior")
    
    # Campaign Configuration
    col1, col2 = st.columns(2)
    
    with col1:
        segment_options = customer_metrics['SegmentName'].unique().tolist()
        selected_segment = st.selectbox(
            "Target Segment",
            options=segment_options,
            index=0,
            help="Choose which customer segment to target"
        )
    
    with col2:
        campaign_options = ["Product Recommendation", "Exclusive Discount", "VIP Upgrade", "Re-engagement", "New Product Launch"]
        campaign_type = st.selectbox(
            "Campaign Type",
            options=campaign_options,
            index=0,
            help="Select the type of marketing campaign"
        )
    
    # Get segment data
    segment_customers = customer_metrics[customer_metrics['SegmentName'] == selected_segment]
    segment_user_ids = segment_customers['UserID'].tolist()
    segment_data = df[df['UserID'].isin(segment_user_ids)]
    segment_products = segment_data['ProductID'].value_counts().head(5)
    
    # Display segment info
    st.markdown(f"""
    <div class="insight-card">
        <h4>Target Segment Profile</h4>
        <p><strong>Segment:</strong> {selected_segment}</p>
        <p><strong>Total Customers:</strong> {len(segment_customers):,}</p>
        <p><strong>Average Spend:</strong> ₹{segment_customers['TotalSpend'].mean():,.2f}</p>
        <p><strong>Average Frequency:</strong> {segment_customers['Frequency'].mean():.1f} transactions</p>
        <p><strong>Popular Products:</strong> {', '.join(segment_products.index.tolist()[:3])}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Generate Email Button
    if st.button("Generate Marketing Email", type="primary", use_container_width=True):
        with st.spinner("Crafting your personalized email..."):
            # Generate email content
            avg_spend = segment_customers['TotalSpend'].mean()
            top_product = segment_products.index[0] if len(segment_products) > 0 else "our products"
            
            # Customize email based on segment and campaign type
            if "VIP" in selected_segment or "High" in selected_segment:
                greeting = "Dear Valued Customer"
                offer = "exclusive 20% VIP discount"
                cta = "CLAIM YOUR VIP OFFER"
            elif "Loyal" in selected_segment:
                greeting = "Hello Loyal Friend"
                offer = "special 15% loyalty reward"
                cta = "REDEEM YOUR REWARD"
            elif "Growing" in selected_segment or "New" in selected_segment:
                greeting = "Hi there"
                offer = "welcoming 10% discount"
                cta = "START SHOPPING"
            else:
                greeting = "Hello"
                offer = "special 10% discount"
                cta = "SHOP NOW"
            
            email_draft = f"""
### Generated Email Campaign

---

**Subject Line Options:**

1. {greeting}! Your {offer} is waiting
2. Exclusive offer on {top_product} just for you
3. We've reserved something special for you

---

**Email Body:**

{greeting},

We noticed you're one of our valued customers in our **{selected_segment}** tier!

Based on your purchase history, especially your interest in **{top_product}**, we've handpicked some recommendations that we think you'll love.

**Your Exclusive Offer:**

Get **{offer}** on your next purchase! This includes:

{chr(10).join([f'• **{prod}** - One of your favorites!' for prod in segment_products.index.tolist()[:3]])}

**Why This Offer is Perfect for You:**

- You've spent an average of **₹{avg_spend:.2f}** with us
- These products complement your recent purchases
- Limited time offer - valid for the next **48 hours**

**[{cta}]**

Don't miss out on this exclusive opportunity!

---

**Best regards,**  
The Smart Retail Team

*P.S. This offer is exclusively for our {selected_segment} members. You're in good company with {len(segment_customers)} other valued customers!*

---

**Campaign Performance Predictions:**

- **Expected Open Rate:** {np.random.randint(25, 45)}%
- **Expected Click Rate:** {np.random.randint(8, 18)}%
- **Estimated Conversions:** {int(len(segment_customers) * np.random.uniform(0.05, 0.15))} customers
- **Potential Revenue:** ₹{len(segment_customers) * avg_spend * np.random.uniform(0.05, 0.15):,.2f}
            """
            
            st.markdown(email_draft)
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.download_button(
                    label="Download Email",
                    data=email_draft,
                    file_name=f"campaign_{selected_segment.replace(' ', '_')}.txt",
                    mime="text/plain"
                )
            
            with col2:
                if st.button("Generate Another"):
                    st.rerun()
            
            with col3:
                st.button("Export Segment List")
    
    # Show segment customers
    with st.expander(f"View All Customers in {selected_segment}"):
        display_cols = ['UserID', 'TotalSpend', 'Frequency', 'UniqueProducts', 'Recency', 'CLV']
        segment_display = segment_customers[display_cols].sort_values('TotalSpend', ascending=False)
        st.dataframe(segment_display, use_container_width=True, height=400)
    
    st.markdown('</div>', unsafe_allow_html=True)

"""Customer segmentation using K-Means clustering"""
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def calculate_customer_metrics(df):
    """
    Calculate RFM and other customer metrics
    
    Args:
        df: DataFrame with columns Date, UserID, Amount, TransactionID, ProductID
    
    Returns:
        DataFrame with customer metrics
    """
    # Calculate recency, frequency, monetary
    current_date = df['Date'].max()
    
    customer_metrics = df.groupby('UserID').agg({
        'Date': lambda x: (current_date - x.max()).days,  # Recency
        'TransactionID': 'nunique',  # Frequency
        'Amount': ['sum', 'mean'],  # Monetary
        'ProductID': 'nunique'  # Variety
    }).reset_index()
    
    customer_metrics.columns = ['UserID', 'Recency', 'Frequency', 'TotalSpend', 'AvgOrderValue', 'UniqueProducts']
    
    # Calculate Customer Lifetime Value (simple version)
    customer_metrics['CLV'] = customer_metrics['TotalSpend'] * (customer_metrics['Frequency'] / customer_metrics['Recency'].replace(0, 1))
    
    return customer_metrics

def segment_customers(customer_metrics, n_clusters=3):
    """
    Perform K-Means clustering on customer metrics
    
    Args:
        customer_metrics: DataFrame with customer metrics
        n_clusters: Number of clusters
    
    Returns:
        DataFrame with segment assignments and labels
    """
    # Select features for clustering
    features = customer_metrics[['Recency', 'Frequency', 'TotalSpend', 'UniqueProducts']].values
    
    # Scale features
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    # Perform K-Means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    customer_metrics['Segment'] = kmeans.fit_predict(features_scaled)
    
    # Label segments based on characteristics
    segment_profiles = customer_metrics.groupby('Segment').agg({
        'TotalSpend': 'mean',
        'Frequency': 'mean',
        'Recency': 'mean',
        'UniqueProducts': 'mean'
    })
    
    # Sort by total spend and assign labels
    segment_order = segment_profiles.sort_values('TotalSpend', ascending=False).index
    
    # Create segment labels based on actual number of clusters
    label_options = [
        'VIP Customers',
        'Loyal Customers',
        'Growing Customers',
        'At-Risk Customers',
        'New Customers'
    ]
    
    segment_labels = {}
    for i, segment_id in enumerate(segment_order):
        if i < len(label_options):
            segment_labels[segment_id] = label_options[i]
        else:
            segment_labels[segment_id] = f'Segment {segment_id}'
    
    customer_metrics['SegmentName'] = customer_metrics['Segment'].map(segment_labels)
    
    return customer_metrics, segment_profiles

def get_segment_insights(customer_metrics, df):
    """
    Generate detailed insights for each segment
    
    Args:
        customer_metrics: DataFrame with segment assignments
        df: Original transaction DataFrame
    
    Returns:
        Dictionary with segment insights
    """
    insights = {}
    
    for segment_name in customer_metrics['SegmentName'].unique():
        segment_users = customer_metrics[customer_metrics['SegmentName'] == segment_name]['UserID'].tolist()
        segment_data = df[df['UserID'].isin(segment_users)]
        
        # Calculate insights
        insights[segment_name] = {
            'size': len(segment_users),
            'total_revenue': segment_data['Amount'].sum(),
            'avg_spend_per_customer': segment_data.groupby('UserID')['Amount'].sum().mean(),
            'avg_frequency': segment_data.groupby('UserID')['TransactionID'].nunique().mean(),
            'top_products': segment_data['ProductID'].value_counts().head(5).to_dict(),
            'avg_items_per_transaction': len(segment_data) / segment_data['TransactionID'].nunique(),
            'revenue_contribution': (segment_data['Amount'].sum() / df['Amount'].sum()) * 100
        }
    
    return insights

"""Generate realistic demo transaction data"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_demo_data(n_transactions=500, n_customers=50, n_days=30):
    """
    Generate realistic demo transaction data with patterns
    
    Args:
        n_transactions: Number of transactions to generate
        n_customers: Number of unique customers
        n_days: Number of days of historical data
    
    Returns:
        DataFrame with columns: Date, UserID, ProductID, TransactionID, Amount
    """
    np.random.seed(42)
    
    dates = pd.date_range(end=datetime.now(), periods=n_days, freq='D')
    user_ids = [f"USER{i:03d}" for i in range(1, n_customers + 1)]
    
    # Product catalog with realistic pricing
    products = {
        'Gaming Mouse': 79,
        'Mousepad': 29,
        'Laptop': 1299,
        'HDMI Cable': 19,
        'USB-C Hub': 49,
        'Monitor': 399,
        '4K Webcam': 149,
        'Mechanical Keyboard': 169,
        'Headphones': 199,
        'External SSD': 129,
        'Laptop Stand': 59,
        'Cable Organizer': 15,
        'Wireless Charger': 39,
        'Phone Case': 25,
        'Screen Protector': 12,
        'Bluetooth Speaker': 89,
        'Desk Lamp': 45,
        'USB Cable': 9,
        'Webcam Cover': 7,
        'Microphone': 179
    }
    
    # Create customer segments with different behaviors
    high_spenders = user_ids[:10]  # Top 20% are high spenders
    medium_spenders = user_ids[10:30]  # 40% are medium spenders
    regular_customers = user_ids[30:]  # Rest are regular
    
    transactions = []
    transaction_id = 1
    
    for _ in range(n_transactions):
        # Choose customer segment
        rand = np.random.random()
        if rand < 0.3:
            user = np.random.choice(high_spenders)
            purchase_prob = 0.7  # Higher purchase frequency
        elif rand < 0.6:
            user = np.random.choice(medium_spenders)
            purchase_prob = 0.5
        else:
            user = np.random.choice(regular_customers)
            purchase_prob = 0.3
        
        date = np.random.choice(dates)
        
        # Create product bundles with realistic patterns
        bundle_rand = np.random.random()
        
        if bundle_rand < 0.25:
            # Gaming bundle
            items = ['Gaming Mouse', 'Mousepad']
            if np.random.random() < 0.4:
                items.append('Mechanical Keyboard')
        elif bundle_rand < 0.45:
            # Work from home bundle
            items = ['Laptop', 'HDMI Cable', 'USB-C Hub']
            if np.random.random() < 0.3:
                items.append('Laptop Stand')
        elif bundle_rand < 0.60:
            # Streaming setup
            items = ['Monitor', '4K Webcam']
            if np.random.random() < 0.35:
                items.append('Microphone')
        elif bundle_rand < 0.75:
            # Mobile accessories
            items = ['Phone Case', 'Screen Protector']
            if np.random.random() < 0.3:
                items.append('Wireless Charger')
        else:
            # Single item purchase
            items = [np.random.choice(list(products.keys()))]
        
        # Add items to transaction
        for item in items:
            transactions.append({
                'Date': date,
                'UserID': user,
                'ProductID': item,
                'TransactionID': transaction_id,
                'Amount': products[item] + np.random.randint(-5, 15)  # Add slight price variation
            })
        
        transaction_id += 1
    
    df = pd.DataFrame(transactions)
    
    # Sort by date
    df = df.sort_values('Date').reset_index(drop=True)
    
    return df

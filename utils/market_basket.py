"""Market basket analysis using Apriori algorithm"""
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

def prepare_basket_data(df):
    """
    Prepare transaction data for Apriori algorithm
    
    Args:
        df: DataFrame with columns TransactionID, ProductID
    
    Returns:
        One-hot encoded basket DataFrame
    """
    basket = df.groupby(['TransactionID', 'ProductID'])['ProductID'].count().unstack().reset_index().fillna(0).set_index('TransactionID')
    
    # Convert to binary (bought/not bought)
    basket_sets = basket.map(lambda x: 1 if x >= 1 else 0)
    
    return basket_sets

def find_product_bundles(basket_sets, min_support=0.05, min_confidence=0.3):
    """
    Find frequent itemsets and association rules
    
    Args:
        basket_sets: One-hot encoded basket DataFrame
        min_support: Minimum support threshold
        min_confidence: Minimum confidence threshold
    
    Returns:
        Tuple of (frequent_itemsets, rules DataFrame)
    """
    # Find frequent itemsets
    frequent_itemsets = apriori(basket_sets, min_support=min_support, use_colnames=True)
    
    if frequent_itemsets.empty or len(frequent_itemsets) < 2:
        return frequent_itemsets, pd.DataFrame()
    
    # Generate association rules
    try:
        rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
        
        if not rules.empty:
            # Format rules for display
            rules['antecedents_str'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
            rules['consequents_str'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))
            rules['confidence_pct'] = (rules['confidence'] * 100).round(1)
            rules['lift_score'] = rules['lift'].round(2)
            rules['support_pct'] = (rules['support'] * 100).round(2)
            
            # Sort by confidence
            rules = rules.sort_values('confidence', ascending=False)
        
        return frequent_itemsets, rules
    
    except Exception as e:
        print(f"Error generating rules: {e}")
        return frequent_itemsets, pd.DataFrame()

def get_product_recommendations(df, product_name, top_n=5):
    """
    Get top N products that are frequently bought with a given product
    
    Args:
        df: Transaction DataFrame
        product_name: Product to find recommendations for
        top_n: Number of recommendations
    
    Returns:
        List of recommended products
    """
    # Find transactions containing the product
    transactions_with_product = df[df['ProductID'] == product_name]['TransactionID'].unique()
    
    # Find other products in those transactions
    other_products = df[
        (df['TransactionID'].isin(transactions_with_product)) & 
        (df['ProductID'] != product_name)
    ]['ProductID'].value_counts().head(top_n)
    
    return other_products.to_dict()

def calculate_bundle_revenue_potential(df, rules):
    """
    Calculate potential revenue impact of promoting bundles
    
    Args:
        df: Transaction DataFrame with Amount column
        rules: Association rules DataFrame
    
    Returns:
        DataFrame with revenue potential for each rule
    """
    if rules.empty:
        return pd.DataFrame()
    
    revenue_potential = []
    
    for idx, rule in rules.iterrows():
        antecedent = list(rule['antecedents'])[0] if len(rule['antecedents']) == 1 else None
        consequent = list(rule['consequents'])[0] if len(rule['consequents']) == 1 else None
        
        if antecedent and consequent:
            # Get average price of consequent
            avg_price = df[df['ProductID'] == consequent]['Amount'].mean()
            
            # Get number of transactions with antecedent but not consequent
            ant_transactions = set(df[df['ProductID'] == antecedent]['TransactionID'])
            cons_transactions = set(df[df['ProductID'] == consequent]['TransactionID'])
            potential_customers = len(ant_transactions - cons_transactions)
            
            # Potential revenue = potential customers * confidence * avg_price
            potential_revenue = potential_customers * rule['confidence'] * avg_price
            
            revenue_potential.append({
                'bundle': f"{antecedent} + {consequent}",
                'potential_customers': potential_customers,
                'expected_conversion': int(potential_customers * rule['confidence']),
                'avg_item_price': avg_price,
                'potential_revenue': potential_revenue,
                'confidence': rule['confidence_pct']
            })
    
    return pd.DataFrame(revenue_potential).sort_values('potential_revenue', ascending=False)

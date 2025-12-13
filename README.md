# Business Segmenter

A comprehensive business analytics tool for customer segmentation, market basket analysis, and AI-powered marketing campaigns.

## Features

- **Overview Dashboard** - Key metrics, revenue trends, and top products
- **Smart Bundles** - Product association discovery using Apriori algorithm
- **Customer Segments** - K-Means clustering with RFM analysis
- **Marketing Assistant** - AI-powered personalized campaign generation

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/VIDHITTS/Business-Segmenter.git
cd Business-Segmenter

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Data Format

### Required Columns

Your CSV file must contain these columns:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| **Date** | datetime | Transaction date (YYYY-MM-DD) | 2024-01-15 |
| **UserID** | string | Customer identifier | CUST001 |
| **ProductID** | string | Product name or ID | Gaming Mouse |

### Optional Columns

These columns will be auto-generated if missing:

| Column | Type | Description |
|--------|------|-------------|
| TransactionID | string | Unique transaction identifier |
| Amount | float | Transaction amount |

### Example CSV

```csv
Date,UserID,ProductID,Amount,TransactionID
2024-01-15,CUST001,Gaming Mouse,299.99,TXN001
2024-01-15,CUST001,Mousepad,49.99,TXN001
2024-01-16,CUST002,Laptop,1299.99,TXN002
2024-01-16,CUST002,HDMI Cable,19.99,TXN002
2024-01-17,CUST001,Keyboard,149.99,TXN003
2024-01-18,CUST003,Gaming Mouse,299.99,TXN004
2024-01-18,CUST003,Mousepad,49.99,TXN004
2024-01-18,CUST003,Keyboard,149.99,TXN004
```

## Usage

### 1. Upload Data
- Drag and drop your CSV file in the sidebar
- Or use the built-in demo data to explore features

### 2. Smart Auto Mode (Recommended)
- Toggle "Smart Auto Mode" ON (default)
- Automatically calculates optimal parameters based on your data
- See explanations for each parameter choice

### 3. Manual Settings (Optional)
- Turn off Smart Auto Mode for manual control
- Adjust Bundle Support (1-20%)
- Adjust Confidence (30-100%)
- Set number of Customer Segments (2-5)

### 4. Click "Analyze Data"
- Required for uploaded CSV files
- Demo data auto-loads immediately

### 5. Explore Insights
- **Overview** - Metrics, trends, and top products
- **Smart Bundles** - Product recommendations and revenue opportunities
- **Customer Segments** - Segment profiles and 3D visualization
- **Marketing** - Generate personalized email campaigns

## Project Structure

```
business-segmenter/
├── app.py                    # Main application entry point
├── requirements.txt          # Python dependencies
├── components/              # UI components
│   ├── sidebar.py           # Sidebar with Smart Auto Mode
│   ├── overview_dashboard.py
│   ├── smart_bundles.py
│   ├── customer_segments.py
│   └── marketing_assistant.py
├── utils/                   # Business logic
│   ├── data_generator.py   # Demo data generation
│   ├── segmentation.py     # K-Means clustering
│   └── market_basket.py    # Apriori algorithm
└── assets/                  # Styling
    └── styles.py
```

## Key Technologies

- **Streamlit** - Web framework
- **Pandas & NumPy** - Data processing
- **Scikit-learn** - Machine learning (K-Means)
- **MLxtend** - Market basket analysis (Apriori)
- **Plotly** - Interactive visualizations

## Error Handling

The app includes robust CSV validation:

✅ Validates required columns  
✅ Checks for empty files  
✅ Validates date formats  
✅ Catches parser errors  
✅ Shows helpful error messages with examples  

No more crashes from invalid data!

## Troubleshooting

### App won't start?
```bash
# Ensure dependencies are installed
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Port already in use?
```bash
streamlit run app.py --server.port 8502
```

### CSV upload errors?
Check that your CSV has the required columns: `Date`, `UserID`, `ProductID`

## License

MIT License - Free for personal and commercial use

---

**Built with Streamlit, Scikit-learn, and MLxtend**

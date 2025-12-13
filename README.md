# 🛍️ Smart Business Segmenter

A comprehensive business analytics tool that combines customer segmentation, market basket analysis, and AI-powered marketing campaign generation.

## ✨ Features

### 1. 📊 Overview Dashboard
- Real-time key performance metrics
- Transaction timeline and revenue trends
- Top performing products analysis
- Interactive visualizations with Plotly

### 2. 🎁 Smart Bundles (Apriori Algorithm)
- Discover frequently bought together products
- Revenue opportunity analysis for each bundle
- Confidence, support, and lift metrics
- Visual bundle recommendations with progress bars

### 3. 👥 Customer Segmentation (K-Means Clustering)
- Automatic customer segmentation using RFM analysis
- 3D visualization of customer segments
- Detailed segment insights and profiles
- Customer Lifetime Value (CLV) calculation

### 4. ✉️ AI Marketing Assistant
- Generate personalized marketing emails
- Segment-based campaign recommendations
- Performance prediction metrics
- Export segment lists and campaigns

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Virtual environment (venv)

### Installation

1. **Activate your virtual environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Open in browser:**
   The app will automatically open at `http://localhost:8501`

## 📁 Project Structure

```
business-segmenter/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (API keys)
├── .gitignore            # Git ignore rules
│
├── utils/                # Utility modules
│   ├── data_generator.py    # Demo data generation
│   ├── segmentation.py      # K-Means clustering & RFM
│   ├── market_basket.py     # Apriori algorithm
│   └── __init__.py
│
├── assets/               # Static assets
│   └── styles.py           # Custom CSS styling
│
├── components/           # Reusable UI components (future)
├── pages/               # Multi-page support (future)
└── data/                # Data storage
```

## 📊 Data Format

Upload a CSV file with the following columns:

| Column | Type | Description |
|--------|------|-------------|
| Date | datetime | Transaction date |
| UserID | string | Customer identifier |
| ProductID | string | Product name or ID |

**Optional columns:**
- `Amount` - Transaction amount (auto-generated if missing)
- `TransactionID` - Unique transaction ID (auto-generated if missing)

### Example Data:
```csv
Date,UserID,ProductID
2025-01-15,USER001,Gaming Mouse
2025-01-15,USER001,Mousepad
2025-01-16,USER002,Laptop
2025-01-16,USER002,HDMI Cable
```

## 🎯 How It Works

### 1. Data Upload
- Drag and drop your CSV file
- Or use the generated demo data to explore features
- Data is automatically validated and processed

### 2. Smart Bundles
- Apriori algorithm identifies product associations
- Adjust support and confidence thresholds in sidebar
- View revenue potential for each bundle
- Get actionable recommendations

### 3. Customer Segments
- K-Means clustering groups similar customers
- RFM (Recency, Frequency, Monetary) analysis
- Adjust number of segments (2-5) in sidebar
- Explore segment characteristics in 3D

### 4. Marketing Campaigns
- Select target segment
- Choose campaign type
- Generate personalized emails instantly
- Download and export for use

## ⚙️ Configuration

### API Keys (Optional)

For AI-powered email generation with OpenAI:

The API key is already configured in `.env` file. If you need to update it:

```bash
# Edit .env file
OPENAI_API_KEY=your-api-key-here
```

### Adjustable Parameters

**In Sidebar:**
- Bundle Support % (1-20%)
- Bundle Confidence % (30-100%)
- Number of Customer Segments (2-5)

## 🎨 Key Technologies

- **Streamlit** - Interactive web application
- **Pandas & NumPy** - Data processing
- **Scikit-learn** - K-Means clustering
- **MLxtend** - Apriori algorithm
- **Plotly** - Interactive visualizations
- **LangChain & OpenAI** - AI email generation (optional)

## 📈 Use Cases

1. **E-commerce Stores**
   - Optimize product bundles
   - Target high-value customers
   - Increase cross-selling

2. **Retail Analytics**
   - Understand customer behavior
   - Identify shopping patterns
   - Improve inventory planning

3. **Marketing Teams**
   - Segment-based campaigns
   - Personalized messaging
   - ROI optimization

## 🔒 Security

- API keys stored in `.env` file (not committed to git)
- `.gitignore` configured for sensitive data
- No data stored permanently (session-based)

## 🐛 Troubleshooting

### App won't start?
```bash
# Make sure you're in the right directory
cd "/Users/vidhitt.s/Desktop/business segmenter"

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
pip install -r requirements.txt --upgrade

# Run the app
streamlit run app.py
```

### Import errors?
```bash
# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Port already in use?
```bash
# Use a different port
streamlit run app.py --server.port 8502
```

## 🚀 Advanced Features (Coming Soon)

- [ ] Multi-page application
- [ ] Historical trend analysis
- [ ] A/B testing recommendations
- [ ] Automated email scheduling
- [ ] PDF report generation
- [ ] Database integration
- [ ] User authentication

## 📝 License

This project is for educational and commercial use.

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the example data format
3. Ensure all dependencies are installed

---

**Built with ❤️ using Streamlit, Scikit-learn, and MLxtend**

*Smart Business Segmenter © 2025*

"""Custom CSS styling for the application"""

def get_custom_css():
    """Return custom CSS for enhanced UI"""
    return """
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
        /* Global Styles */
        .main {
            font-family: 'Inter', sans-serif;
            background-color: white;
            color: #384959;
        }
        
        /* Header Styles */
        h1 {
            color: #384959;
            font-weight: 700;
            padding: 20px 0;
        }
        
        h2 {
            color: #384959;
            border-bottom: 3px solid #6A89A7;
            padding-bottom: 10px;
            margin-top: 30px;
        }
        
        h3 {
            color: #384959;
            font-weight: 600;
        }
        
        p, li, label {
            color: #384959;
        }
        
        /* Custom Cards */
        .metric-card {
            background: linear-gradient(135deg, #6A89A7 0%, #384959 100%);
            padding: 25px;
            border-radius: 15px;
            color: white;
            text-align: center;
            box-shadow: 0 10px 25px rgba(106, 137, 167, 0.3);
            transition: transform 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(106, 137, 167, 0.4);
        }
        
        .metric-card h3 {
            color: white !important;
            font-size: 2.5em;
            margin: 10px 0;
            font-weight: 700;
        }
        
        .metric-card p {
            color: #BDDDFC !important;
            font-size: 0.95em;
            margin: 0;
            opacity: 0.9;
        }
        
        /* Bundle Cards */
        .bundle-card {
            background: #BDDDFC;
            padding: 20px;
            border-radius: 12px;
            border-left: 5px solid #384959;
            margin: 15px 0;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
        }
        
        .bundle-card:hover {
            transform: translateX(5px);
            box-shadow: 0 6px 20px rgba(56, 73, 89, 0.15);
            border-left-color: #6A89A7;
            background: #dbeafe;
        }
        
        .bundle-card h4 {
            color: #384959 !important;
            margin-top: 0;
            font-weight: 600;
        }
        
        .bundle-label {
            display: inline-block;
            background: #384959;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: 600;
            margin-right: 10px;
            font-size: 0.9em;
        }
        
        /* Segment Cards */
        .segment-card {
            background: white;
            padding: 25px;
            border-radius: 15px;
            border: 2px solid #BDDDFC;
            margin: 15px 0;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
        }
        
        .segment-card:hover {
            border-color: #6A89A7;
            box-shadow: 0 8px 25px rgba(106, 137, 167, 0.15);
            transform: translateY(-3px);
        }
        
        .segment-title {
            font-size: 1.4em;
            font-weight: 700;
            color: #384959;
            margin-bottom: 15px;
        }
        
        .segment-stats {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-top: 15px;
        }
        
        .stat-item {
            background: #F0F7FF;
            padding: 12px;
            border-radius: 8px;
            border-left: 3px solid #88BDF2;
        }
        
        .stat-label {
            font-size: 0.85em;
            color: #6A89A7;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .stat-value {
            font-size: 1.5em;
            font-weight: 700;
            color: #384959;
            margin-top: 5px;
        }
        
        /* Insight Cards */
        .insight-card {
            background: #FFF9F0;
            padding: 20px;
            border-radius: 12px;
            border-left: 5px solid #6A89A7;
            margin: 15px 0;
            box-shadow: 0 4px 12px rgba(106, 137, 167, 0.1);
        }
        
        .insight-card h4 {
            color: #384959;
            margin-top: 0;
        }
        
        /* Revenue Card */
        .revenue-card {
            background: linear-gradient(135deg, #88BDF2 0%, #6A89A7 100%);
            padding: 25px;
            border-radius: 15px;
            color: white;
            box-shadow: 0 8px 20px rgba(136, 189, 242, 0.3);
        }
        
        .revenue-card h3 {
            color: white !important;
            font-size: 2em;
            margin: 10px 0;
        }

        .revenue-card p {
            color: white !important;
            opacity: 0.9;
        }
        
        /* Upload Section */
        .upload-section {
            background: #F0F7FF;
            padding: 40px;
            border-radius: 15px;
            border: 2px dashed #88BDF2;
            text-align: center;
            margin: 20px 0;
        }
        
        /* Badges */
        .badge {
            display: inline-block;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            margin: 5px;
        }
        
        .badge-success {
            background: #BDDDFC;
            color: #384959;
        }
        
        .badge-warning {
            background: #fff3cd;
            color: #856404;
        }
        
        .badge-info {
            background: #88BDF2;
            color: #fff;
        }
        
        .badge-danger {
            background: #f8d7da;
            color: #721c24;
        }
        
        /* Progress Bars */
        .progress-bar {
            background: #e2e8f0;
            border-radius: 10px;
            overflow: hidden;
            height: 25px;
            margin: 10px 0;
        }
        
        .progress-fill {
            background: linear-gradient(90deg, #88BDF2 0%, #6A89A7 100%);
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
            font-size: 0.85em;
            transition: width 0.5s ease;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: white;
            padding: 10px 0;
            border-radius: 10px;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            background: white;
            border-radius: 8px;
            padding: 0 24px;
            font-weight: 600;
            color: #6A89A7 !important;
            border: 1px solid #BDDDFC;
            transition: all 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: #BDDDFC;
            color: #384959 !important;
        }
        
        .stTabs [aria-selected="true"],
        .stTabs [aria-selected="true"] *,
        .stTabs [aria-selected="true"] button,
        .stTabs [aria-selected="true"] div,
        .stTabs [aria-selected="true"] p,
        .stTabs [aria-selected="true"] span {
            background: #384959 !important;
            background-color: #384959 !important;
            color: #FFFFFF !important;
            border: none !important;
        }
        
        /* Buttons - ALL STATES */
        .stButton>button,
        .stButton>button:hover,
        .stButton>button:active,
        .stButton>button:focus,
        button[kind="primary"],
        button[kind="primary"]:hover,
        button[kind="primary"]:active,
        button[kind="primary"]:focus {
            background-color: #384959 !important;
            background: #384959 !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 10px;
            padding: 12px 30px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(56, 73, 89, 0.3);
        }
        
        /* Ensure button text is always white */
        .stButton>button *,
        .stButton>button span,
        .stButton>button div,
        .stButton>button p,
        button[kind="primary"] *,
        button[kind="primary"] span,
        button[kind="primary"] div,
        button[kind="primary"] p {
            color: #FFFFFF !important;
        }
        
        .stButton>button:hover,
        button[kind="primary"]:hover {
            transform: translateY(-2px) !important;
            background-color: #2d3748 !important;
            background: #2d3748 !important;
            box-shadow: 0 6px 20px rgba(56, 73, 89, 0.5) !important;
            color: #FFFFFF !important;
        }
        
        .stButton>button:active,
        .stButton>button:focus,
        button[kind="primary"]:active,
        button[kind="primary"]:focus {
            background-color: #2d3748 !important;
            background: #2d3748 !important;
            color: #FFFFFF !important;
            outline: none !important;
        }
        
        /* Download button specific */
        .stDownloadButton>button,
        .stDownloadButton>button:hover,
        .stDownloadButton>button:active,
        .stDownloadButton>button:focus {
            background-color: #384959 !important;
            background: #384959 !important;
            color: #FFFFFF !important;
        }
        
        /* Data Tables */
        .dataframe {
            border: none !important;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #F0F7FF;
            border-right: 1px solid #BDDDFC;
        }
        
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
             color: #384959;
        }
        
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
             color: #384959;
        }
        
        /* Success/Info Messages */
        .stSuccess {
            background: #BDDDFC;
            color: #384959;
            border-left: 5px solid #6A89A7;
        }
        
        .stInfo {
            background: #e7f5ff;
            color: #384959;
            border-left: 5px solid #88BDF2;
        }
        
        .stWarning {
            background: #fff3cd;
            color: #856404;
            border-left: 5px solid #ffeeba;
        }
        
        /* Animation */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .animated {
            animation: fadeIn 0.6s ease-out;
        }

        /* Chart text fix */
        .js-plotly-plot .plotly .xaxislayer-above text, 
        .js-plotly-plot .plotly .yaxislayer-above text {
            fill: #384959 !important;
            font-size: 12px !important;
        }
    </style>
    """
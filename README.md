# InsightFlow

InsightFlow is an intelligent business analytics and insights platform built with Streamlit. It leverages AI-powered sentiment analysis, anomaly detection, and recommendations to help businesses understand their performance metrics, identify trends, and take actionable steps.

## Features

- **Business Overview Dashboard**: Real-time KPI monitoring and performance metrics
- **AI-Powered Sentiment Analysis**: Analyzes customer reviews to identify satisfaction trends and issues
- **Anomaly Detection**: Detects unusual patterns in revenue and key metrics using machine learning
- **Intelligent Recommendations**: AI-generated action items and strategic recommendations
- **Confidence Metrics**: Displays confidence levels for predictions and insights
- **Evidence-Based Analysis**: Links insights to underlying data and drivers
- **Feedback System**: Collects user feedback on insight quality and relevance
- **Multi-Industry Support**: Pre-seeded data for automotive, fashion, grocery, and SaaS sectors
- **Interactive Visualizations**: Powered by Plotly for rich, responsive charts

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: MySQL
- **AI/ML**: Google GenAI, TextBlob, scikit-learn, statsmodels
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly Express

## Requirements

- Python 3.8+
- MySQL 5.7+
- Dependencies listed in `requirements.txt`

## Installation

1. **Clone or setup the project**:
   ```bash
   cd InsightFlow
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   # or
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Create a `.env` file in the project root with:
   ```
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_USER=your_username
   MYSQL_PASSWORD=your_password
   MYSQL_DATABASE=insightflow
   GOOGLE_API_KEY=your_google_genai_key
   ```

5. **Initialize the database**:
   ```bash
   python run_seed.py
   ```
   This will set up the database schema and seed it with sample data.

## Running the Application

Start the Streamlit application:
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Project Structure

```
InsightFlow/
├── app.py                    # Main application entry point
├── config.py                 # Database configuration
├── requirements.txt          # Python dependencies
├── run_seed.py              # Database seeding script
├── ai/                      # AI and NLP modules
│   ├── sentiment.py         # Review sentiment analysis
│   ├── recommendations.py   # AI-powered recommendations
│   └── storyteller.py       # Narrative generation
├── analytics/               # Data analytics modules
│   ├── anomaly.py           # Anomaly detection
│   ├── confidence.py        # Confidence scoring
│   ├── contribution.py      # Driver contribution analysis
│   ├── evidence.py          # Evidence tracking
│   ├── feedback.py          # Feedback processing
│   └── forecast.py          # Trend forecasting
├── components/              # UI components
│   ├── action_cards.py      # Action recommendation cards
│   ├── bento_layout.py      # Layout framework
│   ├── confidence_panel.py  # Confidence visualizations
│   ├── kpi_cards.py         # KPI display cards
│   ├── evidence_panel.py    # Evidence ranking
│   ├── styles.py            # CSS and styling
│   └── layout.py            # Layout helpers
├── pages/                   # Multi-page application
│   ├── 1_Insights.py        # Main insights page
│   ├── 2_Actions.py         # Action items page
│   ├── 3_Feedback.py        # Feedback collection
│   └── 9_Engine_Room.py     # Advanced analytics
├── database/                # Database schema and seeds
│   ├── schema.sql           # Database schema
│   ├── seed_automotive.py   # Automotive data seed
│   ├── seed_fashion.py      # Fashion data seed
│   ├── seed_grocery.py      # Grocery data seed
│   └── seed_saas.py         # SaaS data seed
└── utils/                   # Utility functions
    ├── bootstrap.py         # App initialization
    ├── data_loader.py       # Data loading utilities
    ├── kpi_engine.py        # KPI calculation engine
    ├── telemetry.py         # Usage tracking
    └── security.py          # Security utilities
```

## Application Pages

### 1. **Insights** (1_Insights.py)
The main overview dashboard showing:
- Current business metrics and KPIs
- Revenue trends and changes
- Customer sentiment summary
- Anomalies in key metrics
- AI-generated narrative insights

### 2. **Actions** (2_Actions.py)
Actionable recommendations page:
- Prioritized action items
- Impact estimates
- Implementation guidance
- Related evidence and metrics

### 3. **Feedback** (3_Feedback.py)
Feedback collection for continuous improvement:
- Rate insight relevance
- Report data quality issues
- Provide additional context
- Track feedback history

### 4. **Engine Room** (9_Engine_Room.py)
Advanced analytics and debugging:
- Raw data exploration
- Processing breakdown
- Model diagnostics
- Performance metrics

## Database Setup

The application uses MySQL with predefined schemas. Several seed scripts provide sample data for different industries:

- `seed_automotive.py` - Automotive industry sample data
- `seed_fashion.py` - Fashion retail sample data
- `seed_grocery.py` - Grocery retail sample data
- `seed_saas.py` - SaaS industry sample data

Run all seeds with:
```bash
python run_seed.py
```

Or run individual seeds:
```bash
python database/seed_automotive.py
```

## Key Modules

### AI Module
- **sentiment.py**: Analyzes customer reviews for sentiment (Positive/Negative/Neutral)
- **recommendations.py**: Generates AI-powered action recommendations
- **storyteller.py**: Creates narrative summaries of business insights

### Analytics Module
- **anomaly.py**: Detects unusual patterns using Isolation Forest
- **confidence.py**: Calculates confidence scores for predictions
- **contribution.py**: Analyzes which factors contribute to KPI changes
- **forecast.py**: Generates trend forecasts

### Components Module
Reusable UI components for consistent styling and layout:
- Alert cards, KPI displays, confidence gauges
- Evidence panels, action cards
- Responsive bento-box layout system

### Utils Module
- **kpi_engine.py**: Core KPI calculation logic
- **data_loader.py**: Database query and data loading
- **bootstrap.py**: Application initialization and context setup
- **telemetry.py**: User interaction tracking

## Configuration

Edit `config.py` to change database connection parameters. Use environment variables for sensitive credentials.

For Streamlit-specific configuration, see `.streamlit/config.toml` (if present).

## Contributing

1. Ensure code follows the existing structure
2. Test new analytics modules with sample data
3. Update relevant seed scripts if adding new data schemas
4. Document new components and utilities


## Support

For issues or questions, please check the Engine Room page for diagnostics or consult the application logs.

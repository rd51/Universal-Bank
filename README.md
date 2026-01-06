# Universal Bank BI Dashboard 🏦

## Overview
Interactive Streamlit dashboard for retail banking analytics focusing on:
- **Personal Loan cross-sell optimization**
- **Customer segmentation** using Latent Class Analysis (Gaussian Mixture Models)
- **Association Rule Mining** (Apriori algorithm)
- **Advanced BI KPIs and insights**

## Dataset
- **File:** `UniversalBank with description 2.0.csv`
- **Records:** 5,000+ customers
- **Dimensions:** 14 features (demographics, account info, loan status)

## Tech Stack
- **Python** - Core language
- **Streamlit** - Web framework
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Scikit-learn** - Machine learning (GaussianMixture)
- **Mlxtend** - Association rules mining (Apriori)

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip or conda

### Local Installation
```bash
git clone https://github.com/rd51/Universal-Bank.git
cd Universal-Bank
pip install -r requirements.txt
streamlit run app.py
```

## How to Run
1. Ensure `UniversalBank with description 2.0.csv` is in the project root
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`
4. Open browser at `http://localhost:8501`

## Key Features

### 1. Advanced Customer Segmentation
- **Latent Class Analysis** using Gaussian Mixture Models
- 4 distinct customer segments identified
- Based on: Income, Credit Card Spending, Age, Education, Product Usage

### 2. Product Association Insights
- **Apriori Algorithm** to find frequent itemsets
- **Association Rules** with lift metrics
- Discover cross-sell opportunities
- Minimum support threshold: 10%

### 3. Feature Engineering
- **Income Band:** Low, Medium, High
- **Age Group:** Young, Mid, Senior
- **Total Products:** Count of accounts held
- **Digital Flag:** Online + Credit Card usage

### 4. Interactive Filters
- Filter by Income Band
- Filter by Latent Class (Customer Segment)
- Real-time KPI updates

### 5. Business KPIs
- Total Customers in segment
- Loan Conversion Rate %
- Average Income
- Digital Adoption %

### 6. Segment Analysis
- Loan conversion rates by segment
- Association rules ranked by lift
- Top 10 product combinations

## Deploy on Streamlit Cloud
1. Fork repository to your GitHub
2. Go to https://share.streamlit.io
3. Create new app:
   - Repository: `rd51/Universal-Bank`
   - Branch: `main`
   - Main file: `app.py`
4. Click Deploy

## File Structure
```
Universal-Bank/
├── app.py                              # Main Streamlit application
├── requirements.txt                    # Python dependencies
├── README.md                           # Documentation
├── .gitignore                          # Git ignore rules
├── UniversalBank with description 2.0.csv  # Dataset
└── .streamlit/
    └── config.toml                     # Streamlit configuration
```

## How It Works

### Data Pipeline
1. Load CSV dataset
2. Feature engineering (Income bands, Age groups)
3. Latent Class Analysis (4 clusters via GMM)
4. Association rules mining
5. Interactive visualization & filtering

### Machine Learning Models
- **Gaussian Mixture Model (GMM):** Customer segmentation into 4 latent classes
- **Apriori Algorithm:** Find frequent product combinations
- **Association Rules:** Calculate lift for cross-sell recommendations

## Contributing
Pull requests welcome! Please follow existing code style.

## License
MIT License

## Contact & Support
For issues or questions, open a GitHub issue or contact the maintainer.

## Key Metrics Explained
- **Lift:** Ratio of observed to expected frequency. Values > 1 indicate positive association
- **Latent Class:** Segment identified by GMM clustering algorithm
- **Digital Adoption:** Percentage of customers using online banking or credit cards
- **Loan Conversion:** Percentage of customers with active personal loans

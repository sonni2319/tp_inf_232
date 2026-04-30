# 📊 TP INF 232 — Data Analysis Platform

A modern, interactive data analysis web app built with **Python + Streamlit + Plotly**.

## Features
- ✏️ Manual data entry with editable grid
- 📥 Excel file import with sheet selection & cleaning
- 📐 Descriptive statistics (mean, median, mode, variance, IQR, skewness & more)
- 📈 Linear regression with R² score
- 📊 6 chart types: Histogram, Box Plot, Line, Bar, Pie, Scatter+Regression, Heatmap
- 💡 Auto-insights and smart chart suggestions
- 📤 Export results to styled Excel workbook

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/tp-inf-232.git
cd tp-inf-232

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

## Project Structure

```
tp-inf-232/
├── app.py                  # Main entry point
├── requirements.txt
├── modules/
│   ├── data_input.py       # Manual data entry
│   ├── data_import.py      # Excel import
│   ├── analysis.py         # Statistics engine
│   ├── visualization.py    # Plotly charts
│   └── export.py           # Excel export
└── utils/
    └── helpers.py          # CSS injection & utilities
```

## Deploy on Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → select your repo → set `app.py` as the main file
4. Click **Deploy** 🚀

## Tech Stack
- Python 3.10+
- Streamlit
- Pandas / NumPy
- Plotly 5.22
- xlsxwriter / openpyxl

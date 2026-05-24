# Delhi Metro Network & Ridership Insights Analysis

## Overview

The Delhi Metro Network & Ridership Insights project is a complete end-to-end transportation analytics project developed using Python, SQL, Power BI, and Streamlit. The project analyzes 150,000+ Delhi Metro trip records from 2022–2024 to uncover ridership trends, revenue insights, passenger behavior, seasonal patterns, forecasting, and anomaly detection.

---

## Key Highlights

- 150,000+ metro trip records analyzed
- 30 lakh+ passengers studied
- ₹31.5 crore total revenue analyzed
- 24 metro stations covered
- 28,000+ missing values cleaned
- 24-month passenger forecasting implemented
- Interactive Power BI dashboard created
- Streamlit web application deployed

---

## Technologies Used

### Programming Languages
- Python
- SQL

### Libraries
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Statsmodels
- Scikit-learn

### Tools & Platforms
- Power BI
- Streamlit
- MySQL Workbench
- Jupyter Notebook
- GitHub

---

# Project Modules

## Module 1 — Data Cleaning & Feature Engineering

- Handled 28,257 missing values
- Converted Date column using `pd.to_datetime()`
- Engineered 7 analytical features including:
  - Total Revenue
  - Year
  - Month
  - Day of Week
  - Passenger Segment

---

## Module 2 — Exploratory Data Analysis

Key Findings:
- Rajiv Chowk emerged as the highest traffic station
- Tourist Card generated 39.47% of total revenue
- Fare-Revenue correlation was 0.90
- Distance-Fare correlation was 0.00

---

## Module 3 — Temporal Pattern Analysis

- Ridership remained stable between 73,000–88,000 monthly passengers
- February consistently showed lowest ridership
- August 2024 recorded highest ridership
- Saturday emerged as busiest day of the week
- Off-peak travel exceeded peak-hour traffic

---

## Module 4 — Forecasting & Anomaly Detection

### Forecasting
- Implemented ARIMA and SARIMA models
- SARIMA outperformed ARIMA using RMSE comparison
- Generated 24-month ridership forecast

### Anomaly Detection
- Applied Z-score statistical anomaly detection
- Identified 57 anomalous days
- Highest anomaly recorded on 10 August 2024

---

## Module 5 — Dashboard & Deployment

### Power BI Dashboard
Features:
- KPI cards
- Monthly trend analysis
- Seasonal heatmaps
- Station traffic analysis
- Interactive filters and slicers

### Streamlit Web App
Features:
- Dynamic forecasting horizon
- Adjustable anomaly threshold
- Real-time forecasting
- Downloadable CSV reports

---

# SQL Analysis

Performed SQL analysis using MySQL Workbench:
- Summary statistics
- Revenue by ticket type
- Top 10 station rankings
- Monthly ridership trends
- Peak vs Off-Peak comparison

---

# Dashboard Preview

## Power BI Dashboard
![Dashboard](images/1. dashboard (Overview Page).png)

## Forecasting Output
![Forecast](images/Future_forecast.png)

## Heatmap
![Heatmap](images/seasonal_ridership_heatmap.png)

## Streamlit Application
![Streamlit](images/1. Overview Page.png)

---

# Project Structure

```text
Delhi_Metro_Project/
│
├── data/
├── notebooks/
├── dashboard/
├── sql_queries/
├── streamlit_app/
├── images/
├── README.md
├── requirements.txt
├── app.py
└── metro_analysis.ipynb

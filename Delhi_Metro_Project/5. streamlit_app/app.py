# ─────────────────────────────────────────────
# DELHI METRO RIDERSHIP INSIGHTS — STREAMLIT APP
# ─────────────────────────────────────────────

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings
warnings.filterwarnings('ignore')

# ── PAGE CONFIGURATION ──────────────────────────────────────
# This sets the browser tab title, icon and layout
st.set_page_config(
    page_title = "Delhi Metro Ridership Insights",
    page_icon  = "🚇",
    layout     = "wide"
)

# ── LOAD AND CACHE DATA ──────────────────────────────────────
# @st.cache_data tells Streamlit to load the data only once
# and remember it — so the app doesn't reload data every time
# you click something. Makes the app much faster.
@st.cache_data
def load_data():
    df = pd.read_csv('delhi_metro_updated.csv')
    df['Date']         = pd.to_datetime(df['Date'])
    df['From_Station'] = df['From_Station'].str.strip().str.title()
    df['To_Station']   = df['To_Station'].str.strip().str.title()
    df['Ticket_Type']  = df['Ticket_Type'].fillna('Unknown')
    df['Remarks']      = df['Remarks'].fillna('Normal')
    df['Passengers']   = df['Passengers'].fillna(df['Passengers'].median())
    df['Total_Revenue']= df['Fare'] * df['Passengers']
    df['Year']         = df['Date'].dt.year
    df['Month']        = df['Date'].dt.month
    df['Day_of_Week']  = df['Date'].dt.day_name()
    df['Quarter']      = df['Date'].dt.quarter
    df['Month_Year']   = df['Date'].dt.to_period('M').astype(str)
    return df

df = load_data()

# ── SIDEBAR NAVIGATION ───────────────────────────────────────
# st.sidebar creates the left panel
# st.sidebar.radio creates clickable page options
st.sidebar.image(
    "Delhi_Metro_full_logo.svg.png",
    width = 120
)
st.sidebar.title("🚇 Delhi Metro")
st.sidebar.markdown("**Ridership Insights Dashboard**")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate to",
    ["🏠 Home",
     "📊 EDA",
     "🕐 Temporal Analysis",
     "📈 Forecasting",
     "🔍 Anomaly Detection"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Filters**")

# ── GLOBAL FILTERS IN SIDEBAR ────────────────────────────────
# These filters affect charts across pages
# st.sidebar.multiselect creates checkboxes for multiple selection
selected_years = st.sidebar.multiselect(
    "Select Year(s)",
    options = sorted(df['Year'].unique()),
    default = sorted(df['Year'].unique())
)

selected_tickets = st.sidebar.multiselect(
    "Select Ticket Type(s)",
    options = df['Ticket_Type'].unique().tolist(),
    default = df['Ticket_Type'].unique().tolist()
)

# Apply filters — this creates a filtered version of the data
# based on whatever the user selected in the sidebar
filtered_df = df[
    (df['Year'].isin(selected_years)) &
    (df['Ticket_Type'].isin(selected_tickets))
]

st.sidebar.markdown("---")
st.sidebar.caption("BCA (DS & AI) Final Year Project")
st.sidebar.caption("Kirti Srivastava | BBD University")


# ════════════════════════════════════════════════════════════
# PAGE 1 — HOME
# ════════════════════════════════════════════════════════════
if page == "🏠 Home":

    # st.title creates a large heading
    st.title("🚇 Delhi Metro Network & Ridership Insights")
    st.markdown("**BCA (DS & AI) Final Year Project | BBD University, Lucknow**")
    st.markdown("---")

    # Project description
    st.markdown("""
    This dashboard presents a comprehensive analysis of **1,50,000 Delhi Metro 
    trip records** spanning from **January 2022 to December 2024**.  
    The analysis covers exploratory data analysis, temporal pattern analysis, 
    time series forecasting using ARIMA & SARIMA models, and anomaly detection.
    """)

    st.markdown("---")
    st.subheader("📌 Key Performance Indicators")

    # st.columns(4) creates 4 equal columns side by side
    # This is how we make the KPI card row
    col1, col2, col3, col4 = st.columns(4)

    # st.metric creates a clean KPI card with a label and value
    with col1:
        st.metric("Total Trips",
                  f"{len(filtered_df):,}")
    with col2:
        st.metric("Total Passengers",
                  f"{filtered_df['Passengers'].sum():,.0f}")
    with col3:
        st.metric("Total Revenue",
                  f"₹{filtered_df['Total_Revenue'].sum():,.0f}")
    with col4:
        st.metric("Average Fare",
                  f"₹{filtered_df['Fare'].mean():.2f}")

    st.markdown("---")

    # Second row of KPIs
    col5, col6, col7, col8 = st.columns(4)

    with col5:
        st.metric("Unique Stations",
                  f"{filtered_df['From_Station'].nunique()}")
    with col6:
        st.metric("Avg Distance",
                  f"{filtered_df['Distance_km'].mean():.2f} km")
    with col7:
        st.metric("Avg Passengers/Trip",
                  f"{filtered_df['Passengers'].mean():.1f}")
    with col8:
        st.metric("Revenue/Passenger",
                  f"₹{filtered_df['Total_Revenue'].sum() / filtered_df['Passengers'].sum():.2f}")

    st.markdown("---")
    st.subheader("📋 Dataset Preview")

    # st.dataframe shows an interactive scrollable table
    st.dataframe(filtered_df.head(10), use_container_width=True)

    st.markdown("---")
    st.subheader("🗂️ Project Modules")

    # st.columns(3) creates 3 equal columns for module cards
    m1, m2, m3 = st.columns(3)

    with m1:
        # st.info creates a blue information box
        st.info("**Module 1 — Data Cleaning**\n\n"
                "Handled missing values, standardised station names, "
                "engineered new features including Total Revenue, "
                "Year, Month, Day of Week and Passenger Segments.")
    with m2:
        st.info("**Module 2 — EDA**\n\n"
                "Analysed distributions, station traffic, ticket type "
                "performance and correlations across all key "
                "numerical variables.")
    with m3:
        st.info("**Module 3 — Temporal Analysis**\n\n"
                "Studied monthly trends, weekday vs weekend patterns, "
                "seasonal heatmaps and quarterly revenue trends "
                "across 2022–2024.")

    m4, m5, _ = st.columns(3)

    with m4:
        st.success("**Module 4 — Forecasting**\n\n"
                   "Implemented ARIMA and SARIMA models on monthly "
                   "passenger data. Best model selected by lowest RMSE. "
                   "Forecasted next 24 months with confidence intervals.")
    with m5:
        st.success("**Module 5 — Dashboard & KPIs**\n\n"
                   "Compiled all findings into a summary dashboard with "
                   "12 visualisations, KPI reporting and final "
                   "recommendations for metro management.")


# ════════════════════════════════════════════════════════════
# PAGE 2 — EDA
# ════════════════════════════════════════════════════════════
elif page == "📊 EDA":

    st.title("📊 Exploratory Data Analysis")
    st.markdown("---")

    # ── Station Traffic ──────────────────────────────────────
    st.subheader("🚉 Top Departure Stations by Passengers")

    # st.slider creates a draggable slider for the user
    # Here we let user choose how many top stations to show
    top_n = st.slider("Select number of top stations", 5, 20, 10)

    top_stations = (filtered_df.groupby('From_Station')['Passengers']
                    .sum()
                    .sort_values(ascending=False)
                    .head(top_n)
                    .reset_index())

    # px.bar creates an interactive Plotly bar chart
    fig = px.bar(top_stations,
                 x='Passengers', y='From_Station',
                 orientation='h',
                 color='Passengers',
                 color_continuous_scale='Blues',
                 title=f'Top {top_n} Departure Stations by Total Passengers',
                 labels={'From_Station': 'Station',
                         'Passengers': 'Total Passengers'})
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})

    # st.plotly_chart displays the interactive plotly chart
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Ticket Type Analysis ─────────────────────────────────
    st.subheader("🎫 Ticket Type Analysis")

    # st.columns(2) creates 2 side by side charts
    col1, col2 = st.columns(2)

    ticket = filtered_df.groupby('Ticket_Type').agg(
        Trips         = ('TripID',        'count'),
        Total_Revenue = ('Total_Revenue', 'sum'),
        Avg_Fare      = ('Fare',          'mean')
    ).reset_index()

    with col1:
        fig1 = px.pie(ticket,
                      values='Trips',
                      names='Ticket_Type',
                      title='Trips by Ticket Type',
                      hole=0.4)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.bar(ticket,
                      x='Ticket_Type',
                      y='Total_Revenue',
                      color='Ticket_Type',
                      title='Revenue by Ticket Type (₹)',
                      labels={'Total_Revenue': 'Total Revenue (₹)'})
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # ── Correlation Heatmap ──────────────────────────────────
    st.subheader("🔗 Correlation Heatmap")

    corr_cols  = ['Distance_km', 'Fare',
                  'Cost_per_passenger', 'Passengers', 'Total_Revenue']
    corr_matrix = filtered_df[corr_cols].corr()

    # We use matplotlib here inside streamlit using st.pyplot
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f',
                cmap='coolwarm', linewidths=0.5,
                ax=ax, vmin=-1, vmax=1)
    ax.set_title('Correlation Matrix of Numerical Variables')

    # st.pyplot displays a matplotlib figure
    st.pyplot(fig)

    st.markdown("---")

    # ── Distribution ─────────────────────────────────────────
    st.subheader("📐 Variable Distributions")

    # st.selectbox creates a dropdown menu
    col_to_plot = st.selectbox(
        "Select variable to visualise",
        ['Fare', 'Distance_km', 'Passengers', 'Total_Revenue']
    )

    fig = px.histogram(filtered_df,
                       x=col_to_plot,
                       nbins=40,
                       marginal='box',
                       title=f'Distribution of {col_to_plot}',
                       color_discrete_sequence=['steelblue'])
    st.plotly_chart(fig, use_container_width=True)


# ════════════════════════════════════════════════════════════
# PAGE 3 — TEMPORAL ANALYSIS
# ════════════════════════════════════════════════════════════
elif page == "🕐 Temporal Analysis":

    st.title("🕐 Temporal Pattern Analysis")
    st.markdown("---")

    # ── Monthly Trend ────────────────────────────────────────
    st.subheader("📅 Monthly Passenger Trend")

    monthly = (filtered_df.groupby('Month_Year')
               .agg(Passengers    = ('Passengers',    'sum'),
                    Total_Revenue = ('Total_Revenue', 'sum'),
                    Trips         = ('TripID',        'count'))
               .reset_index())

    # st.radio creates small button options
    metric = st.radio("Select metric",
                      ['Passengers', 'Total_Revenue', 'Trips'],
                      horizontal=True)

    fig = px.line(monthly,
                  x='Month_Year', y=metric,
                  markers=True,
                  title=f'Monthly {metric} Trend (2022–2024)',
                  labels={'Month_Year': 'Month-Year',
                          metric: metric})
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Day of Week ──────────────────────────────────────────
    st.subheader("📆 Passengers by Day of Week")

    dow_order = ['Monday','Tuesday','Wednesday',
                 'Thursday','Friday','Saturday','Sunday']
    dow = (filtered_df.groupby('Day_of_Week')['Passengers']
           .sum().reindex(dow_order).reset_index())
    dow['Type'] = dow['Day_of_Week'].apply(
        lambda x: 'Weekend' if x in ['Saturday','Sunday'] else 'Weekday')

    fig = px.bar(dow,
                 x='Day_of_Week', y='Passengers',
                 color='Type',
                 color_discrete_map={'Weekday':'#4C72B0',
                                     'Weekend':'#C44E52'},
                 title='Total Passengers by Day of Week')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Seasonal Heatmap ─────────────────────────────────────
    st.subheader("🌡️ Seasonal Ridership Heatmap")

    pivot = (filtered_df.groupby(['Year','Month'])['Passengers']
             .sum().unstack('Month'))
    pivot.columns = ['Jan','Feb','Mar','Apr','May','Jun',
                     'Jul','Aug','Sep','Oct','Nov','Dec']

    fig, ax = plt.subplots(figsize=(14, 4))
    sns.heatmap(pivot, annot=True, fmt='.0f',
                cmap='YlOrRd', linewidths=0.5, ax=ax)
    ax.set_title('Seasonal Ridership Heatmap (Year × Month)')
    st.pyplot(fig)

    st.markdown("---")

    # ── Peak vs Off-Peak ─────────────────────────────────────
    st.subheader("⏰ Ridership by Remarks Category")

    remarks = (filtered_df.groupby('Remarks')
               .agg(Passengers = ('Passengers', 'sum'),
                    Avg_Fare   = ('Fare',        'mean'))
               .reset_index()
               .sort_values('Passengers', ascending=False))

    fig = px.bar(remarks,
                 x='Remarks', y='Passengers',
                 color='Remarks',
                 title='Total Passengers by Remarks Category')
    st.plotly_chart(fig, use_container_width=True)


# ════════════════════════════════════════════════════════════
# PAGE 4 — FORECASTING
# ════════════════════════════════════════════════════════════
elif page == "📈 Forecasting":

    st.title("📈 Time Series Forecasting")
    st.markdown("---")

    # Prepare monthly passenger time series
    monthly_passengers = (df.set_index('Date')['Passengers']
                          .resample('ME').sum())

    # ── Model Selection ──────────────────────────────────────
    st.subheader("⚙️ Model Configuration")

    col1, col2 = st.columns(2)

    with col1:
        # st.selectbox lets user pick which model to run
        model_choice = st.selectbox(
            "Select Forecasting Model",
            ["ARIMA", "SARIMA"]
        )

    with col2:
        # st.slider lets user choose how many months to forecast
        forecast_months = st.slider(
            "Forecast Horizon (months)", 6, 36, 24)

    st.markdown("---")

    # ── Run Model ────────────────────────────────────────────
    # st.spinner shows a loading animation while model runs
    with st.spinner(f"Training {model_choice} model... please wait"):

        split_idx = int(len(monthly_passengers) * 0.8)
        train     = monthly_passengers[:split_idx]
        test      = monthly_passengers[split_idx:]

        if model_choice == "ARIMA":
            model     = ARIMA(train, order=(1,1,1))
            model_fit = model.fit()
            test_forecast = model_fit.forecast(steps=len(test))

            full_model     = ARIMA(monthly_passengers, order=(1,1,1))
            full_model_fit = full_model.fit()
            future_forecast = full_model_fit.forecast(
                steps=forecast_months)
            future_dates = future_forecast.index
            model_order  = "(1,1,1)"

        else:  # SARIMA
            model     = SARIMAX(train,
                                order=(1,1,1),
                                seasonal_order=(1,1,1,12))
            model_fit = model.fit(disp=False)
            test_forecast = model_fit.forecast(steps=len(test))

            full_model     = SARIMAX(monthly_passengers,
                                     order=(1,1,1),
                                     seasonal_order=(1,1,1,12))
            full_model_fit = full_model.fit(disp=False)
            future_fc      = full_model_fit.get_forecast(
                steps=forecast_months)
            future_forecast = future_fc.predicted_mean
            conf_int        = future_fc.conf_int()
            future_dates    = future_forecast.index
            model_order     = "(1,1,1)x(1,1,1,12)"

    # ── Model Metrics ────────────────────────────────────────
    from sklearn.metrics import mean_squared_error, mean_absolute_error
    rmse = np.sqrt(mean_squared_error(test, test_forecast))
    mae  = mean_absolute_error(test, test_forecast)

    st.subheader("📊 Model Performance")
    c1, c2, c3 = st.columns(3)
    c1.metric("Model",    f"{model_choice}{model_order}")
    c2.metric("RMSE",     f"{rmse:,.0f} passengers")
    c3.metric("MAE",      f"{mae:,.0f} passengers")

    st.markdown("---")

    # ── Train/Test Plot ──────────────────────────────────────
    st.subheader("🔍 Train / Test Evaluation")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=train.index, y=train,
        name='Training Data', line=dict(color='#4C72B0', width=2)))
    fig.add_trace(go.Scatter(
        x=test.index, y=test,
        name='Actual (Test)', line=dict(color='#55A868', width=2)))
    fig.add_trace(go.Scatter(
        x=test.index, y=test_forecast,
        name=f'{model_choice} Forecast',
        line=dict(color='#C44E52', width=2, dash='dash')))
    fig.update_layout(
        title=f'{model_choice} — Train/Test Evaluation',
        xaxis_title='Date', yaxis_title='Monthly Passengers',
        hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Future Forecast Plot ─────────────────────────────────
    st.subheader(f"🔮 {forecast_months}-Month Future Forecast")

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=monthly_passengers.index, y=monthly_passengers,
        name='Historical', line=dict(color='#4C72B0', width=2)))

    # Vertical line at forecast start
    # Vertical line at forecast start
    forecast_start = monthly_passengers.index[-1]

    fig2.add_vline(
        x=forecast_start,
        line_dash="dot",
        line_color="grey"   
    )

    fig2.add_annotation(
        x=forecast_start,
        y=monthly_passengers.max(),
        text="Forecast Start",
        showarrow=True,
        arrowhead=1,
        ax=40,
        ay=-40
    )

    fig2.add_trace(go.Scatter(
        x=future_dates, y=future_forecast,
        name='Forecast', line=dict(color='#C44E52', width=2,
                                   dash='dash')))

    # Add confidence interval shading for SARIMA
    if model_choice == "SARIMA":
        fig2.add_trace(go.Scatter(
            x=list(future_dates) + list(future_dates[::-1]),
            y=list(conf_int.iloc[:,1]) + list(conf_int.iloc[:,0][::-1]),
            fill='toself',
            fillcolor='rgba(255,0,0,0.15)',
            line=dict(color='rgba(255,255,255,0)'),
            name='95% Confidence Interval'))

    fig2.update_layout(
        title=f'{model_choice} — {forecast_months} Month Future Forecast',
        xaxis_title='Date', yaxis_title='Monthly Passengers',
        hovermode='x unified')
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # ── Forecast Table ───────────────────────────────────────
    st.subheader("📋 Forecast Values Table")

    forecast_df = pd.DataFrame({
        'Month'                : future_dates.strftime('%Y-%m'),
        'Forecasted_Passengers': future_forecast.round(0).astype(int)
    })

    # st.dataframe with use_container_width fills full page width
    st.dataframe(forecast_df, use_container_width=True)

    # st.download_button lets user download a CSV
    csv = forecast_df.to_csv(index=False)
    st.download_button(
        label     = "⬇️ Download Forecast as CSV",
        data      = csv,
        file_name = f'{model_choice}_forecast.csv',
        mime      = 'text/csv'
    )


# ════════════════════════════════════════════════════════════
# PAGE 5 — ANOMALY DETECTION
# ════════════════════════════════════════════════════════════
elif page == "🔍 Anomaly Detection":

    st.title("🔍 Anomaly Detection in Daily Ridership")
    st.markdown("---")

    # Calculate daily passengers
    daily_pass = (df.groupby('Date')['Passengers']
                  .sum().reset_index())
    daily_pass.columns = ['Date', 'Daily_Passengers']

    mean_p = daily_pass['Daily_Passengers'].mean()
    std_p  = daily_pass['Daily_Passengers'].std()

    # ── Threshold Slider ─────────────────────────────────────
    st.subheader("⚙️ Configure Detection Threshold")

    # Let user change the Z-score threshold interactively
    threshold = st.slider(
        "Z-Score Threshold (higher = fewer anomalies detected)",
        min_value = 1.5,
        max_value = 3.5,
        value     = 2.0,
        step      = 0.1
    )

    daily_pass['Z_Score'] = ((daily_pass['Daily_Passengers'] - mean_p)
                              / std_p)
    daily_pass['Anomaly'] = daily_pass['Z_Score'].abs() > threshold
    anomalies             = daily_pass[daily_pass['Anomaly']]

    # ── KPI Row ──────────────────────────────────────────────
    a1, a2, a3, a4 = st.columns(4)
    a1.metric("Total Days Analysed",   f"{len(daily_pass):,}")
    a2.metric("Anomalous Days",        f"{len(anomalies)}")
    a3.metric("Upper Boundary (+Zσ)",
              f"{mean_p + threshold*std_p:,.0f}")
    a4.metric("Lower Boundary (-Zσ)",
              f"{mean_p - threshold*std_p:,.0f}")

    st.markdown("---")

    # ── Anomaly Chart ────────────────────────────────────────
    st.subheader("📉 Daily Passenger Count with Anomalies")

    fig = go.Figure()

    # Normal daily line
    fig.add_trace(go.Scatter(
        x=daily_pass['Date'], y=daily_pass['Daily_Passengers'],
        name='Daily Passengers',
        line=dict(color='#4C72B0', width=1)))

    # Red dots for anomalies
    fig.add_trace(go.Scatter(
        x=anomalies['Date'], y=anomalies['Daily_Passengers'],
        mode='markers', name='Anomaly',
        marker=dict(color='red', size=8, symbol='circle')))

    # Upper boundary line
    fig.add_hline(y=mean_p + threshold*std_p,
                  line_dash="dash", line_color="orange",
                  annotation_text=f"+{threshold}σ boundary")

    # Lower boundary line
    fig.add_hline(y=mean_p - threshold*std_p,
                  line_dash="dash", line_color="orange",
                  annotation_text=f"-{threshold}σ boundary")

    fig.update_layout(
        title='Anomaly Detection in Daily Passenger Counts',
        xaxis_title='Date',
        yaxis_title='Daily Passengers',
        hovermode='x unified')

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Anomaly Table ────────────────────────────────────────
    st.subheader("📋 List of Anomalous Days")

    # Color code the Z-score column
    # Positive Z = unusually HIGH, Negative Z = unusually LOW
    anomalies_display = anomalies.copy()
    anomalies_display['Type'] = anomalies_display['Z_Score'].apply(
        lambda z: '🔴 Unusually High' if z > 0 else '🔵 Unusually Low')
    anomalies_display = anomalies_display.sort_values(
        'Z_Score', key=abs, ascending=False)
    anomalies_display['Z_Score'] = anomalies_display['Z_Score'].round(2)

    st.dataframe(anomalies_display, use_container_width=True)

    # Download button for anomalies
    csv = anomalies_display.to_csv(index=False)
    st.download_button(
        label     = "⬇️ Download Anomaly Report as CSV",
        data      = csv,
        file_name = "anomaly_report.csv",
        mime      = 'text/csv'
    )
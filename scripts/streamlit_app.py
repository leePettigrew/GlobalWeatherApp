import streamlit as st
import pandas as pd
import plotly.express as px
import time
import numpy as np

# Set the page configuration
st.set_page_config(
    page_title="🌍 Global Weather Dashboard",
    layout="wide",
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    </style>
    """, unsafe_allow_html=True)

# Title with emoji
st.title("🌍 Global Weather Dashboard")

# Sidebar for navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["Data Dashboard", "Live Data Updates"])

# Load the cleaned data
@st.cache_data
def load_data():
    df = pd.read_csv('data/clean/global_weather_cleaned.csv')
    return df

df = load_data()

# Data Dashboard Section
if selection == "Data Dashboard":
    st.header("📊 Data Dashboard")

    # Sidebar Filters
    st.sidebar.subheader("Filters")
    country_list = df['country'].unique().tolist()
    country_list.sort()
    country_list.insert(0, 'All')
    selected_country = st.sidebar.selectbox("Select Country", country_list)
    date_input = st.sidebar.text_input("Date (YYYY-MM-DD)")

    # Apply filters
    if selected_country != 'All':
        df_filtered = df[df['country'] == selected_country]
    else:
        df_filtered = df.copy()

    if date_input:
        df_filtered = df_filtered[df_filtered['last_updated'].str.contains(date_input)]

    # Display data
    st.write("### Filtered Data")
    st.dataframe(df_filtered)

    # Visualization
    if not df_filtered.empty:
        st.write("### Visualizations")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🌡️ Temperature Distribution")
            fig = px.histogram(
                df_filtered,
                x='temperature_celsius',
                nbins=50,
                title='Temperature Distribution',
                color_discrete_sequence=['#FF4B4B']
            )
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.subheader("💧 Humidity Distribution")
            fig = px.histogram(
                df_filtered,
                x='humidity',
                nbins=50,
                title='Humidity Distribution',
                color_discrete_sequence=['#1f77b4']
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

# Live Data Updates Section
elif selection == "Live Data Updates":
    st.header("📡 Live Data Updates")

    # Placeholder for the live plot
    placeholder = st.empty()
    df_live = pd.DataFrame(columns=['last_updated', 'temperature_celsius', 'country'])

    # Simulate data for top 5 countries
    top_countries = df['country'].value_counts().head(5).index.tolist()
    df_simulated = df[df['country'].isin(top_countries)].reset_index(drop=True)

    # Simulate live data updates
    for _ in range(60):  # Simulate 60 data points
        # Randomly select a country
        country = df_simulated.sample(1).iloc[0]
        # Generate data with random fluctuation
        data = {
            'last_updated': pd.Timestamp.now(),
            'temperature_celsius': country['temperature_celsius'] + np.random.normal(0, 0.5),
            'country': country['country']
        }
        df_live = pd.concat([df_live, pd.DataFrame([data])], ignore_index=True)

        # Convert 'last_updated' to datetime
        df_live['last_updated'] = pd.to_datetime(df_live['last_updated'])

        # Update live plot
        with placeholder.container():
            if not df_live.empty:
                fig = px.line(
                    df_live,
                    x='last_updated',
                    y='temperature_celsius',
                    color='country',
                    title='Live Temperature Updates',
                    markers=True
                )
                fig.update_layout(
                    xaxis_title='Time',
                    yaxis_title='Temperature (°C)',
                    legend_title='Country'
                )
                st.plotly_chart(fig, use_container_width=True)
        time.sleep(1)

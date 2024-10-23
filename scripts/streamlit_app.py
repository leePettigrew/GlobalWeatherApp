import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import time
import json

# Set the page configuration
st.set_page_config(
    page_title="Global Weather Dashboard",
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

# Data Dashboard Section
if selection == "Data Dashboard":
    st.header("📊 Data Dashboard")

    # Sidebar Filters
    st.sidebar.subheader("Filters")
    # Assuming you have a list of unique countries
    @st.cache_data
    def get_country_list():
        response = requests.get('http://localhost:5000/data')
        data = response.json()
        df_countries = pd.DataFrame(data)
        country_list = df_countries['country'].unique().tolist()
        country_list.sort()
        country_list.insert(0, 'All')
        return country_list

    country_list = get_country_list()
    selected_country = st.sidebar.selectbox("Select Country", country_list)
    date_input = st.sidebar.text_input("Date (YYYY-MM-DD)")

    # Fetch data from the Flask API
    @st.cache_data
    def load_data(country, date):
        params = {}
        if country and country != 'All':
            params['country'] = country
        if date:
            params['date'] = date
        response = requests.get('http://localhost:5000/data', params=params)
        data = response.json()
        return pd.DataFrame(data)

    df_filtered = load_data(selected_country, date_input)

    # Display data
    st.write("### Filtered Data")
    st.dataframe(df_filtered)

    # Visualization
    if not df_filtered.empty:
        st.write("### Visualizations")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🌡️ Temperature Distribution")
            fig = px.histogram(df_filtered, x='temperature_celsius', nbins=50, title='Temperature Distribution', color_discrete_sequence=['#FF4B4B'])
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.subheader("💧 Humidity Distribution")
            fig = px.histogram(df_filtered, x='humidity', nbins=50, title='Humidity Distribution', color_discrete_sequence=['#1f77b4'])
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

# Live Data Updates Section
elif selection == "Live Data Updates":
    st.header("📡 Live Data Updates")

    # Placeholder for the live plot
    placeholder = st.empty()

    # Initialize an empty DataFrame
    df_live = pd.DataFrame(columns=['last_updated', 'temperature_celsius'])

    # Stream data from the Flask API
    with st.spinner("Connecting to live data stream..."):
        response = requests.get('http://localhost:5000/stream', stream=True)
        if response.encoding is None:
            response.encoding = 'utf-8'

        # Process streaming data
        for line in response.iter_lines(decode_unicode=True):
            if line and line.startswith("data:"):
                json_data = line.replace("data:", "")
                data = json.loads(json_data)

                # Use pd.concat instead of append
                df_live = pd.concat([df_live, pd.DataFrame([data])], ignore_index=True)

                # Convert 'last_updated' to datetime if necessary
                if 'last_updated' in df_live.columns:
                    df_live['last_updated'] = pd.to_datetime(df_live['last_updated'])

                # Update live plot
                with placeholder.container():
                    if not df_live.empty:
                        fig = px.line(df_live, x='last_updated', y='temperature_celsius', title='Live Temperature Updates', markers=True)
                        fig.update_layout(xaxis_title='Time', yaxis_title='Temperature (°C)')
                        st.plotly_chart(fig, use_container_width=True)
                time.sleep(1)

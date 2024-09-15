import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
from fredapi import Fred

# Set up FRED API
fred_key = '2e57a7876c4e69707e4fd2786defc7e3'
fred = Fred(api_key=fred_key)

# Streamlit app
st.title('Unemployment Rates by State')

# Load data
@st.cache_data
def load_data():
    unemp_df = fred.search('unemployment rate state', filter=('frequency','Monthly'))
    unemp_df = unemp_df.query('seasonal_adjustment == "Seasonally Adjusted" and units == "Percent"')
    unemp_df = unemp_df.loc[unemp_df['title'].str.contains('Unemployment Rate')]
    
    uemp_results = pd.DataFrame()
    for index, row in unemp_df.iterrows():
        series = fred.get_series(row['id'])
        uemp_results[row['id']] = series
    
    # Remove columns with more than 4 characters (assuming these are not state codes)
    cols_to_drop = [col for col in uemp_results.columns if len(col) > 4]
    uemp_results = uemp_results.drop(columns=cols_to_drop)
    
    uemp_states = uemp_results.copy()
    uemp_states = uemp_states.dropna()
    id_to_state = unemp_df['title'].str.replace('Unemployment Rate in ','').to_dict()
    uemp_states.columns = [id_to_state[c] for c in uemp_states.columns]
    
    return uemp_states

uemp_states = load_data()

# Create Plotly chart
fig = px.line(uemp_states)

# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)
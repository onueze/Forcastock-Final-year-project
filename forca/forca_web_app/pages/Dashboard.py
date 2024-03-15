from database import *
from user import *

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Dashboard Title
st.title('Stock Market Dashboard')

# Sidebar for user input
st.sidebar.header('User Input Parameters')

def get_input():
    start_date = st.sidebar.date_input("Start Date", pd.to_datetime('2020-01-01'))
    end_date = st.sidebar.date_input("End Date", pd.to_datetime('today'))
    stock_symbol = st.sidebar.text_input("Stock Symbol", "AAPL")
    return start_date, end_date, stock_symbol

def get_company_name(symbol):
    ticker = yf.Ticker(symbol)
    info = ticker.info
    return info.get('longName')

def get_data(symbol, start, end):
    ticker = yf.Ticker(symbol)
    df = ticker.history(period='1d', start=start, end=end)
    df.reset_index(inplace=True)
    return df

start, end, symbol = get_input()
df = get_data(symbol, start, end)
company_name = get_company_name(symbol)

# Displaying the stock information
st.header(company_name + " Stock Price\n")

# Using Plotly Express for the line chart
fig = px.line(df, x='Date', y='Close', labels={'Close': 'Closing Price'}, title=f"{company_name} Closing Price")
fig.update_xaxes(title_text='Date')
fig.update_yaxes(title_text='Closing Price (USD)')
st.plotly_chart(fig)

# Displaying metrics
st.header('Data Metrics')
st.metric(label="Closing Price", value=f"${df['Close'].iloc[-1]:.2f}")
st.metric(label="Volume", value=f"{df['Volume'].iloc[-1]}")




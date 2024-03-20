from database import *
from user import *
#from pages.StockPrediction import show_stock_prediction

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import requests

# Function to display the dashboard
def display_dashboard():

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
        
    def get_current_price(ticker):
        data = yf.Ticker(ticker).history(period='1m')
        return data['Close'].iloc[-1]
        

    # Retrieve user input
    start, end, symbol = get_input()
    df = get_data(symbol, start, end)
    company_name = get_company_name(symbol)
        
    current_price = get_current_price(symbol)

    # Displaying the stock information
    st.header(company_name + " Stock Price\n")

    # Using Plotly Express for the line chart
    fig = px.line(df, x='Date', y='Close', labels={'Close': 'Closing Price'}, title=f"{company_name} Closing Price")
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Closing Price (USD)')
    st.plotly_chart(fig)

    # Button to navigate to the stock prediction page
    if st.button("Predict Stock"):
        st.session_state['selected_ticker'] = symbol
        # Update the session state to indicate the current page or action
        st.session_state.current_page = "stock_prediction"
        # Rerun the app to reflect changes
        st.rerun()


    # Displaying metrics
    st.header('Data Metrics')
    st.metric(label="Closing Price", value=f"${df['Close'].iloc[-1]:.2f}")
    st.metric(label="Volume", value=f"{df['Volume'].iloc[-1]}")

        
    # Function to fetch news from Alpha Vantage
    def get_alpha_vantage_news(api_key, symbol):
        base_url = "https://www.alphavantage.co/query"
        params = {
            "function": "NEWS_SENTIMENT",
            "tickers": symbol,
            "apikey": api_key
        }
        response = requests.get(base_url, params=params)
        return response.json()

    # Fetch and display news based on user input symbol
    st.title(f'Stock News from Alpha Vantage for {company_name}')

    api_key = "YOUR_ALPHA_VANTAGE_API_KEY"  # API key here

    try:
        news_json = get_alpha_vantage_news(api_key, symbol)
        news_articles = news_json.get('feed', [])
        count = 0
        for article in news_articles:
            if count == 5:
                break
            st.subheader(article['title'])
            st.write(article['summary'])
            st.markdown(f"[Read more]({article['url']})", unsafe_allow_html=True)
            count += 1
    except Exception as e:
        st.error('Error fetching news from Alpha Vantage: ' + str(e))
            
            


user_id = st.session_state.get('user_id', None)
if user_id:
    display_dashboard()
    st.session_state['current_page'] = 'dashboard'
else:
    st.error('Please log in to view dashboard.')


    
    
    




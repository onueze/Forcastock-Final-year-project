from database import *
from user import *
#from pages.StockPrediction import show_stock_prediction

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

from bs4 import BeautifulSoup
import requests

# Function to display the dashboard
def display_dashboard():
    '''Display the main dashboard interface with stock market visualization.'''
    
    # Dashboard Title
    st.title('Stock Market Dashboard')

    # Sidebar for user input
    st.sidebar.header('User Input Parameters')

    def get_input():
        """
        returns user input for start date, end date, and company ticker symbol
        from sidebar input fields.
        """
        
        start_date = st.sidebar.date_input("Start Date", pd.to_datetime('2020-01-01'))
        end_date = st.sidebar.date_input("End Date", pd.to_datetime('today'))
        
        # Scrape S&P 500 tickers
        sp500_tickers = scrape_sp500_tickers()

        # options for the selectbox
        options = [f"{ticker} - {company}" for ticker, company in sp500_tickers]
        # Sort options alphabetically by company name
        options.sort()
        selected_option = st.sidebar.selectbox("Select a company:", options)
        ticker_symbol = selected_option.split(" - ")[0]
        
        return start_date, end_date, ticker_symbol
    
    @st.cache_data
    def get_company_name(symbol):
        """
        Retrieve the name of the company associated to the ticker symbol.
        """
        
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return info.get('longName')
    
    @st.cache_data
    def get_data(symbol, start, end):
        """
        Fetch historical stock price data for the ticker symbol between the start and end dates.
        """
        
        ticker = yf.Ticker(symbol)
        df = ticker.history(period='1d', start=start, end=end)
        df.reset_index(inplace=True)
        return df
    
    # The process of scraping the sp500 data was taken from the Beautiful Soup package https://realpython.com/beautiful-soup-web-scraper-python/
    @st.cache_data
    def scrape_sp500_tickers():
        """
        Scrape S&P 500 ticker symbols and company names from Wikipedia.
        """
        
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table', {'class': 'wikitable sortable'})

        # Initialize an empty list to store tickers
        tickers = []
        # Loop over each row in the table except the header row
        for row in table.findAll('tr')[1:]:
            ticker = row.findAll('td')[0].text.strip()
            company_name = row.findAll('td')[1].text.strip()
            tickers.append((ticker, company_name))
        return tickers
        

    # Retrieve user input
    start, end, symbol = get_input()
    df = get_data(symbol, start, end)
    company_name = get_company_name(symbol)
        

    # Displaying the stock information
    company_name = get_company_name(symbol)
    if company_name is None:
        st.error("Failed to fetch company name.")
        return  # Exit the function early since no fetch of the company name
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
    
    # Fetch and display news based on user input symbol
    st.title(f'Stock News from Alpha Vantage for {company_name}')

    
    # lines 99-125 (except the st. statements) The process of fetching  the news data from the ALPHA VANTAGE API was generated by ChatGPT. The specific prompts will be detailed in the final report    
    # Function to fetch news from Alpha Vantage
    def get_alpha_vantage_news(api_key, symbol):
        """
        Fetch news articles related to the ticker symbol using the Alpha Vantage API.
        """
        base_url = "https://www.alphavantage.co/query"
        params = {
            "function": "NEWS_SENTIMENT",
            "tickers": symbol,
            "apikey": api_key
        }
        response = requests.get(base_url, params=params)
        return response.json()

    api_key = "SY6VYHGY5D4SITEN"  # API key here

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


    
    
    




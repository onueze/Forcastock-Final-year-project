import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import datetime
from tensorflow.keras.initializers import Orthogonal
from tensorflow.keras.models import load_model
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

import requests
from bs4 import BeautifulSoup

# please uncomment for local testing
MODEL_PATH = '../my_lstm_model.keras'

# please uncomment for deployment
#MODEL_PATH = 'forca/my_lstm_model.keras'
SEQUENCE_LENGTH = 200

@st.cache_data
def load_dataset(ticker,start_date,end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return pd.DataFrame(data)

@st.cache_resource
def load_lstm_model():
    return load_model(MODEL_PATH)

def prepare_data(df):
    scaler = MinMaxScaler()
    scaled_close = scaler.fit_transform(df['Close'].values.reshape(-1, 1))
    X = []
    for i in range(len(scaled_close) - SEQUENCE_LENGTH):
        sequence = scaled_close[i:(i + SEQUENCE_LENGTH)]
        X.append(sequence)
    return np.array(X), scaler

def predict_future_prices(model, last_sequence, scaler, n_future_steps):
    future_predictions = []
    current_sequence = last_sequence
    for _ in range(n_future_steps):
        predicted = model.predict(current_sequence.reshape(1, SEQUENCE_LENGTH, 1))
        future_predictions.append(predicted[0][0])
        current_sequence = np.roll(current_sequence, -1)
        current_sequence[-1] = predicted
    return scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))


# Create sequences for prediction
def create_sequences(data, sequence_length):
    X, y = [], []
    for i in range(len(data) - sequence_length):
        X.append(data[i:i+sequence_length])
        y.append(data[i+sequence_length])
    return np.array(X), np.array(y)


# The process of scraping the sp500 data was taken from the Beautiful Soup package https://realpython.com/beautiful-soup-web-scraper-python/
@st.cache_data
def scrape_sp500_tickers():
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

def show_stock_prediction():
    # UI
    if 'user_authenticated' in st.session_state and st.session_state['user_authenticated']:
         
        st.title("Forcastock Stock Prediction")
        
         # Define the restricted date
        restriction_date = datetime.date(2022, 3, 1)
        
        start_date = st.date_input("Start Date", value=datetime.date(2022, 1, 1))
        end_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        
        # Scrape S&P 500 tickers
        sp500_tickers = scrape_sp500_tickers()
    
        # options for the selectbox
        options = [f"{ticker} - {company}" for ticker, company in sp500_tickers]
        # Sort options alphabetically by company name
        options.sort()
        selected_option = st.selectbox("Select a company:", options)
        ticker_symbol = selected_option.split(" - ")[0]

        if ticker_symbol:
            df = load_dataset(ticker_symbol,start_date,end_date)
            if not df.empty:
                fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
                fig.update_layout(title=f"{ticker_symbol} Candlestick Chart", xaxis_title="Date", yaxis_title="Price", template="plotly_white")
                st.plotly_chart(fig, use_container_width=True)
                
                if start_date >= restriction_date:
                    st.error("Stock prediction is not available after 01 March 2022.")
                    return

                lstm_model = load_lstm_model()
                X, scaler = prepare_data(df)
            
                n_future_steps = st.number_input("Number of days to predict:", min_value=1, value=10, max_value=100)
                last_sequence = X[-1]
                predicted_prices = predict_future_prices(lstm_model, last_sequence, scaler, n_future_steps)
            
                future_dates = pd.date_range(start=df.index.max() + pd.Timedelta(days=1), periods=n_future_steps)
                fig.add_trace(go.Scatter(x=future_dates, y=predicted_prices.flatten(), mode='lines', name='Predicted Prices', line=dict(color='red', dash='dot')))
                fig.update_layout(title=f"{ticker_symbol} Stock Price Prediction", xaxis_rangeslider_visible=False)
                st.plotly_chart(fig, use_container_width=True)

                # Displaying the predicted future price in HTML markdown
                st.markdown(f"<h4 style='color:green;'>Predicted Future Price after {n_future_steps} days: ${predicted_prices[-1][0]:.2f}</h4>", unsafe_allow_html=True)
                
                # following code is taken from the research component
                # Prepare the data for LSTM
                scaler = MinMaxScaler()
                scaled_data = scaler.fit_transform(df['Close'].values.reshape(-1, 1))
                X, y = create_sequences(scaled_data, SEQUENCE_LENGTH)

                # Split data into train and test sets
                split_index = int(len(X) * 0.8)
                X_train, X_test = X[:split_index], X[split_index:]
                y_train, y_test = y[:split_index], y[split_index:]
                
                # Define the starting index for test data based on SEQUENCE_LENGTH and split_index
                test_start_idx = split_index + SEQUENCE_LENGTH
                # Create a date index for the test set
                dates_for_test = df.index[test_start_idx:test_start_idx + len(X_test)]

                # Load LSTM model and make predictions
                lstm_model = load_lstm_model()
                predictions = lstm_model.predict(X_test)

                # Inverse transform to get actual prices
                y_test_actual = scaler.inverse_transform(y_test.reshape(-1, 1))
                predictions_actual = scaler.inverse_transform(predictions)

                # Plot the actual and predicted prices using Matplotlib
                fig, ax = plt.subplots(figsize=(12, 6))
                ax.plot(dates_for_test, y_test_actual, color='red', label='Actual Price')
                ax.plot(dates_for_test, predictions_actual, color='green', label='Predicted Price')
                ax.set_title(f'Actual vs Predicted Price for {ticker_symbol}')
                ax.set_xlabel('Date')
                ax.set_ylabel('Price')
                ax.legend()
                st.pyplot(fig)



            try:
                company_name = yf.Ticker(ticker_symbol).info['longName']
                st.write(f"**Company Name:** {company_name}")
            except KeyError:
                st.write("Company name information not available.")

            try:
                industry = yf.Ticker(ticker_symbol).info['industry']
                st.write(f"**Industry:** {industry}")
            except KeyError:
                st.write("Industry information not available.")

            try:
                market_cap = yf.Ticker(ticker_symbol).info['marketCap']
                st.write(f"**Market Cap:** ${market_cap:,}")
            except KeyError:
                st.write("Market Cap information not available.")

            try:
                dividend_rate = yf.Ticker(ticker_symbol).info.get('dividendRate', 'N/A')
                st.write(f"**Dividend Rate:** ${dividend_rate}")
            except KeyError:
                st.write("Dividend Rate information not available.")

            try:
                trailing_eps = yf.Ticker(ticker_symbol).info['trailingEps']
                st.write(f"**EPS (TTM):** ${trailing_eps}")
            except KeyError:
                st.write("EPS (TTM) information not available.")

            try:
                forward_pe = yf.Ticker(ticker_symbol).info['forwardPE']
                st.write(f"**P/E Ratio (TTM):** {forward_pe}")
            except KeyError:
                st.write("P/E Ratio (TTM) information not available.")

            try:
                fifty_two_week_high = yf.Ticker(ticker_symbol).info['fiftyTwoWeekHigh']
                st.write(f"**52 Week High:** ${fifty_two_week_high}")
            except KeyError:
                st.write("52 Week High information not available.")

            try:
                fifty_two_week_low = yf.Ticker(ticker_symbol).info['fiftyTwoWeekLow']
                st.write(f"**52 Week Low:** ${fifty_two_week_low}")
            except KeyError:
                st.write("52 Week Low information not available.")
            

user_id = st.session_state.get('user_id', None)
if user_id:
    show_stock_prediction()
    st.session_state['current_page'] = 'stock_prediction'
else:
    st.error('Please log in to view Stock prediction.')


    
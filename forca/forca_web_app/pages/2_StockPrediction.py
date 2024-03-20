import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import datetime
from tensorflow.keras.initializers import Orthogonal
from tensorflow.keras.models import load_model
import numpy as np
from sklearn.preprocessing import MinMaxScaler

MODEL_PATH = '../my_lstm_model.keras'
SEQUENCE_LENGTH = 500

@st.cache_data
def load_dataset(ticker,start_date,end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return pd.DataFrame(data)

@st.cache_resource
def load_lstm_model():
    return load_model(MODEL_PATH, custom_objects={'Orthogonal': Orthogonal(gain=1.0, seed=42)})

def prepare_data(df):
    scaler = MinMaxScaler()
    scaled_close = scaler.fit_transform(df['Close'].values.reshape(-1, 1))
    X = [scaled_close[i:(i + SEQUENCE_LENGTH)] for i in range(len(scaled_close) - SEQUENCE_LENGTH)]
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



def show_stock_prediction():
# UI
    if 'user_authenticated' in st.session_state and st.session_state['user_authenticated']:
         
        st.title("Forcastock Stock Prediction")
        start_date = st.date_input("Start Date", value=datetime.date(2022, 1, 1))
        end_date = datetime.datetime.now().strftime("%Y-%m-%d")
        ticker_symbol = st.text_input("Enter Ticker Symbol (e.g., AAPL):")

        if ticker_symbol:
            df = load_dataset(ticker_symbol,start_date,end_date)
            if not df.empty:
                fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
                fig.update_layout(title=f"{ticker_symbol} Candlestick Chart", xaxis_title="Date", yaxis_title="Price", template="plotly_white")
                st.plotly_chart(fig, use_container_width=True)

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
                
                # Button to navigate to the stock prediction page
                if st.button(f"Trade {ticker_symbol}"):
                    # Update the session state to indicate the current page or action
                    st.session_state.current_page = "demo_trading"
                    # Rerun the app to reflect changes
                    st.rerun()



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


    
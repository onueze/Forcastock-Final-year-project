import streamlit as st
import pandas as pd
import yfinance as yf
import datetime

start_date = '2022-01-01'
end_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Load dataset
@st.cache(allow_output_mutation=True)
def load_dataset(ticker):
    data = yf.download(ticker, start=start_date, end=end_date)
    return pd.DataFrame(data)

# Initialize demo account if not already done
if 'demo_account' not in st.session_state:
    st.session_state.demo_account = {
        'initial_amount': 0.0,
        'balance': 0.0,
        'holdings': {}
    }

# Function to allocate initial amount
def allocate_initial_amount():
    initial_amount = st.number_input("Enter initial amount for the demo account:", min_value=100.0, step=100.0, format="%.2f")
    if st.button("Allocate"):
        st.session_state.demo_account['initial_amount'] = initial_amount
        st.session_state.demo_account['balance'] = initial_amount
        st.success(f"Allocated ${initial_amount} to your demo account.")

# Function to trade stocks
def trade_stocks():
    ticker = st.text_input("Enter Ticker Symbol (e.g., AAPL):").upper()
    if ticker:
        lot_size = st.number_input("Enter lot size (number of shares):", min_value=1, step=1)
        if st.button("Buy"):
            buy_stock(ticker, lot_size)
        elif st.button("Sell"):
            sell_stock(ticker, lot_size)

# Buy stock
def buy_stock(ticker, lot_size):
    # Dummy price for the example; in practice, fetch the current stock price
    current_price = 100  # This should be replaced with real-time price fetching
    total_cost = current_price * lot_size
    if total_cost <= st.session_state.demo_account['balance']:
        # Update holdings and balance
        if ticker in st.session_state.demo_account['holdings']:
            st.session_state.demo_account['holdings'][ticker] += lot_size
        else:
            st.session_state.demo_account['holdings'][ticker] = lot_size
        st.session_state.demo_account['balance'] -= total_cost
        st.success(f"Bought {lot_size} shares of {ticker}.")
    else:
        st.error("Insufficient funds.")

# Sell stock
def sell_stock(ticker, lot_size):
    if ticker in st.session_state.demo_account['holdings'] and st.session_state.demo_account['holdings'][ticker] >= lot_size:
        # Dummy price for the example; in practice, fetch the current stock price
        current_price = 100  # This should be replaced with real-time price fetching
        total_value = current_price * lot_size
        st.session_state.demo_account['holdings'][ticker] -= lot_size
        st.session_state.demo_account['balance'] += total_value
        st.success(f"Sold {lot_size} shares of {ticker}.")
    else:
        st.error("Insufficient shares to sell.")

# Main page layout
st.title("Demo Trading Account")
if st.session_state.demo_account['initial_amount'] == 0.0:
    allocate_initial_amount()
else:
    trade_stocks()
    st.write(f"Account Balance: ${st.session_state.demo_account['balance']:.2f}")
    st.write("Current Holdings:")
    st.write(st.session_state.demo_account['holdings'])
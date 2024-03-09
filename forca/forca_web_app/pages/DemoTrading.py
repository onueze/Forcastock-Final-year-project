import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
#from StockPrediction import load_dataset


start_date = '2022-01-01'  
end_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Cache the function output to improve performance
@st.cache_data  
def load_dataset(ticker):
    data = yf.download(ticker, start=start_date, end=end_date)
    df = pd.DataFrame(data)
    return df

def demo_account_page():
    st.title("Demo Account Allocation")
    st.write("Allocate a certain amount of money to your demo account.")

    # Input field for users to enter the initial amount
    initial_amount = st.number_input("Enter initial amount:", min_value=0.0, step=1.0)

    # Button to confirm allocation
    if st.button("Allocate"):
        # Store the initial amount in session state or a persistent storage solution
        st.session_state.initial_amount = initial_amount
        st.success(f"Successfully allocated ${initial_amount} to your demo account.")

        # Rerun the app to navigate to the page for selecting stocks and lot sizes
        st.experimental_rerun()


def select_stocks_page():
    st.title("Select Stocks and Lot Sizes")
    st.write("Here, you can select stocks and lot sizes.")

    # Ticker input field
    ticker_input = st.text_input("Enter Ticker Symbol (e.g., AAPL):")

    if ticker_input:
        # Display stock information table
        st.subheader("Stock Information")
        display_stock_info(ticker_input)


def display_stock_info(ticker):
    # Load real-time data for the entered ticker symbol
    df = load_dataset(ticker)

    if df is not None:
        # Display stock information table
        st.write(f"**Ticker:** {ticker}")
        st.write(df)


if "initial_amount" not in st.session_state:
    demo_account_page()
else:
    select_stocks_page()

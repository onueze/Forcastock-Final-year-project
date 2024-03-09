import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import datetime

start_date = '2022-01-01'  
end_date = datetime.datetime.now().strftime("%Y-%m-%d")


# Cache the function output to improve performance
@st.cache_data  
def load_dataset(ticker):
    data = yf.download(ticker, start=start_date, end=end_date)
    df = pd.DataFrame(data)
    return df


st.title("Forcastock Stock Prediction")
ticker_symbol = st.text_input("Enter Ticker Symbol (e.g., AAPL):")

if ticker_symbol:
    # Load data
    df = load_dataset(ticker_symbol)

    if df is not None:
        # Display candlestick chart
        fig = go.Figure(data=[go.Candlestick(x=df.index,
                        open=df['Open'],
                        high=df['High'],
                        low=df['Low'],
                        close=df['Close'])])

        fig.update_layout(
            title=f"{ticker_symbol} Candlestick Chart",
            xaxis_title="Date",
            yaxis_title="Price",
            template="plotly_white" 
        )

        st.plotly_chart(fig, use_container_width=True)

        st.header("Stock Information")

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

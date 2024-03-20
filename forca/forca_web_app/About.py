import streamlit as st
#from pages.Dashboard import display_dashboard


def about_page():
    st.title("About Forcastock")

    st.write("""
    ### Welcome to Forcastock!

    Forcastock is a stock market dashboard application designed to provide real-time stock market data, analysis tools, and trading simulations. Our goal is to empower individual investors and traders with the tools and information they need to make informed decisions.

    #### Features of Forcastock:
    - **Real-Time Market Data:** Access up-to-the-minute information on stock prices, trends, and market conditions.
    - **Advanced Analysis Tools:** Utilize tools like moving averages, Bollinger Bands to analyze stock performance.
    - **Trading Simulation:** Test your trading strategies in a risk-free environment with the virtual trading platform.
    - **Stock Prediction:** Leverage our machine learning model to get predictions on stock price movements.

    Whether you're a seasoned investor or just starting, Forcastock provides a comprehensive suite of tools to help you navigate the complexities of the stock market.

    #### Disclaimer
    Forcastock is a tool for financial analysis and simulation, not a financial advisor. The information and features provided by Forcastock are for educational purposes only and should not be interpreted as investment advice. Users should conduct their own research or consult with a financial advisor before making investment decisions. Forcastock and its creator will not be liable for any financial loss or damage arising from the use of this application.
    
    
    Please engage with the Navigation Bar and
    
    #### ENJOY FORCASTOCK!!!
    """)


user_id = st.session_state.get('user_id', None)
if user_id:
    about_page()
else:
    st.error('Please log in to view this page.')

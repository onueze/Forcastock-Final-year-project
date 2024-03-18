import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import datetime
from database import connect_to_database


def load_dataset(ticker, start_date='2022-01-01', end_date=datetime.datetime.now().strftime("%Y-%m-%d")):
    data = yf.download(ticker, start=start_date, end=end_date)
    return pd.DataFrame(data)


def get_current_price(ticker):
    data = yf.Ticker(ticker).history(period='1d')
    return data['Close'].iloc[-1]

def update_transaction(user_id, ticker, lot_size, transaction_type, current_price):
    conn = connect_to_database()
    print('not yet SUCCESS')
    if conn is not None:
        try:
            with conn.cursor() as cur:
                print('connection SUCCESS')
                cur.execute("SELECT demo_id FROM demo_accounts WHERE user_id = %s;", (user_id,))
                demo_id = cur.fetchone()[0]
                cur.execute("""
                    INSERT INTO transactions (transaction_type, stock_symbol, quantity, price, demo_id)
                    VALUES (%s, %s, %s, %s, %s);
                """, (transaction_type, ticker, lot_size, current_price, demo_id))
                print('INSERT SUCCESS')
                if transaction_type == "BUY":
                    cur.execute("UPDATE demo_accounts SET allocated_amount = allocated_amount - %s WHERE demo_id = %s;", (current_price * lot_size, demo_id))
                else:
                    cur.execute("UPDATE demo_accounts SET allocated_amount = allocated_amount + %s WHERE demo_id = %s;", (current_price * lot_size, demo_id))
                conn.commit()
                print('BUY SUCCESS')
                return True, f"Transaction successful: {transaction_type} {lot_size} shares of {ticker} at ${current_price:.2f} each."
        except Exception as e:
            return False, "Database operation failed."
        finally:
            conn.close()
    else:
        return False, "Failed to connect to the database."

def buy_stock(ticker, lot_size):
    current_price = get_current_price(ticker)
    user_id = st.session_state.user_id
    success, message = update_transaction(user_id, ticker, lot_size, "BUY", current_price)
    if success:
        st.success(message)
    else:
        st.error(message)

def sell_stock(ticker, lot_size):
    current_price = get_current_price(ticker)
    user_id = st.session_state.user_id
    success, message = update_transaction(user_id, ticker, lot_size, "SELL", current_price)
    if success:
        st.success(message)
    else:
        st.error(message)

def calculate_moving_averages(data, windows=[20, 50]):
    for window in windows:
        data[f'MA{window}'] = data['Close'].rolling(window=window).mean()
    return data

def calculate_bollinger_bands(data, window=20, num_of_std=2):
    data['MA20'] = data['Close'].rolling(window=window).mean()
    data['STD20'] = data['Close'].rolling(window=window).std()
    data['UpperBB'] = data['MA20'] + (data['STD20'] * num_of_std)
    data['LowerBB'] = data['MA20'] - (data['STD20'] * num_of_std)
    return data

def trade_stocks():
    st.subheader("Trade Stocks")
    ticker = st.text_input("Enter Ticker Symbol (e.g., AAPL):").upper()
    if ticker:
        try:
            current_price = get_current_price(ticker)
            st.write(f"Current Price of {ticker}: ${current_price:.2f}")
        except Exception:
            st.error("Failed to fetch current price. Please check the ticker and try again.")
            return

        lot_size = st.number_input("Enter lot size (number of shares):", min_value=1, step=1)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Buy"):
                buy_stock(ticker, lot_size)
        with col2:
            if st.button("Sell"):
                sell_stock(ticker, lot_size)

        data = load_dataset(ticker)
        if not data.empty:
            analysis_options = st.multiselect('Select Analysis Options', ['Moving Averages', 'Bollinger Bands'])
            fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'])])

            if 'Moving Averages' in analysis_options:
                data = calculate_moving_averages(data)
                for window in [20, 50]:
                    fig.add_trace(go.Scatter(x=data.index, y=data[f'MA{window}'], mode='lines', name=f'MA{window}'))

            if 'Bollinger Bands' in analysis_options:
                data = calculate_bollinger_bands(data)
                fig.add_trace(go.Scatter(x=data.index, y=data['UpperBB'], mode='lines', name='Upper Bollinger Band', line=dict(color='rgba(250, 0, 0, 0.75)')))
                fig.add_trace(go.Scatter(x=data.index, y=data['LowerBB'], mode='lines', name='Lower Bollinger Band', line=dict(color='rgba(0, 0, 250, 0.75)')))

            fig.update_layout(title=f"{ticker} Analysis", xaxis_title="Date", yaxis_title="Price", template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
            

import streamlit as st

def display_open_trades(user_id):
    conn = connect_to_database()
    if conn is not None:
        try:
            with conn.cursor() as cur:
                # Fetch all open trades for the user
                cur.execute("""
                    SELECT transaction_id, transaction_type, stock_symbol, quantity, price, timestamp
                    FROM transactions
                    WHERE demo_id = (
                        SELECT demo_id FROM demo_accounts WHERE user_id = %s
                    ) AND status = 'OPEN';
                """, (user_id,))

                # Fetch rows
                trades = cur.fetchall()

                if trades:
                    # Convert the trades to a DataFrame for display
                    df = pd.DataFrame(trades, columns=['Transaction ID', 'Type', 'Symbol', 'Quantity', 'Price', 'Timestamp'])
                    st.subheader("Open Trades")
                    st.table(df)
                else:
                    st.write("No open trades found.")

        except Exception as e:
            st.error("Failed to fetch open trades: " + str(e))
        finally:
            conn.close()
    else:
        st.error("Failed to connect to the database.")

            

def check_or_create_demo_account(user_id):
    conn = connect_to_database()
    if conn is not None:
        try:
            with conn.cursor() as cur:
                # Check if the user already has a demo account
                cur.execute("SELECT demo_id, allocated_amount FROM demo_accounts WHERE user_id = %s;", (user_id,))
                account_info = cur.fetchone()

                if account_info:
                    return True, account_info[0], account_info[1]  # Has account, return demo_id and balance
                else:
                    # No account found, create a new one with a default amount (handled below)
                    return False, None, 0
        except Exception as e:
            print(f"Error checking or creating demo account: {e}")
            return False, None, 0
        finally:
            conn.close()
    else:
        print("Failed to connect to the database.")
        return False, None, 0
    
def allocate_initial_amount(user_id):
    initial_amount = st.number_input("Enter initial amount for the demo account:", min_value=100.0, step=100.0, format="%.2f")
    if st.button("Allocate"):
        conn = connect_to_database()
        if conn is not None:
            try:
                with conn.cursor() as cur:
                    # Insert new demo account with allocated amount
                    cur.execute("INSERT INTO demo_accounts (allocated_amount, user_id) VALUES (%s, %s) RETURNING demo_id;", (initial_amount, user_id))
                    demo_id = cur.fetchone()[0]
                    conn.commit()
                    st.success(f"Allocated ${initial_amount} to your demo account with ID {demo_id}.")
                    return demo_id
            except Exception as e:
                st.error(f"Failed to allocate initial amount. Error: {e}")
                return None
            finally:
                conn.close()
        else:
            st.error("Failed to connect to the database for allocation.")
            return None

def show_demo_trading():
    st.title("Demo Trading Account")
    
    if 'user_id' not in st.session_state:
        st.warning("Please log in to continue.")  
        return

    user_id = st.session_state['user_id']

    has_account, demo_id, balance = check_or_create_demo_account(user_id)
    
    if not has_account:
        st.subheader("Allocate Initial Amount to Demo Account")
        demo_id = allocate_initial_amount(user_id)
        if demo_id:
            st.session_state['demo_id'] = demo_id
            st.experimental_rerun()

    if has_account or demo_id:
        # Tabs for different trading views
        tab1, tab2 = st.tabs(["Trade", "Open Trades"])

        with tab1:
            trade_stocks()

        with tab2:
            display_open_trades(user_id)


        st.write(f"Account Balance: ${balance:.2f}")
        st.write("Current Holdings: Placeholder") 

# Check if the dashboard page should be displayed
if "current_page" in st.session_state:
    if st.session_state.current_page == 'demo_trading':
        show_demo_trading()
    elif st.session_state.current_page == '':
        pass
else:
    # this means that the page was selected from the navigation bar
    pass
    
    
    

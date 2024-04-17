import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import datetime
from database import connect_to_database
import time

import requests
from bs4 import BeautifulSoup


# Margin percentage for both buy and sell positions
MARGIN_PERCENTAGE = 10  

# The process of scraping the sp500 data was taken from the Beautiful Soup package https://realpython.com/beautiful-soup-web-scraper-python/
@st.cache_data
def scrape_sp500_tickers():
    """
    Scrape S&P 500 ticker symbols and company names from Wikipedia.
     
    :return: List of tuples containing ticker symbols and company names.
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

@st.cache_data
def load_dataset(ticker, start_date='2022-01-01', end_date=datetime.datetime.now().strftime("%Y-%m-%d")):
    """
    Download and return stock price data for a given ticker, start date, and end date.
    
    :param ticker: Ticker symbol of the stock.
    :param start_date: Start date for the data retrieval.
    :param end_date: End date for the data retrieval.
    :return: DataFrame containing stock price data.
    """
    data = yf.download(ticker, start=start_date, end=end_date)
    return pd.DataFrame(data)

@st.cache_data
def get_current_price(ticker):
    """
    Retrieve the current closing price of a stock.
    
    :param ticker: Stock ticker symbol.
    :return: Latest closing price of the stock.
    """
    data = yf.Ticker(ticker).history(period='1m')
    return data['Close'].iloc[-1]

def update_transaction(user_id, ticker, lot_size, transaction_type, current_price):
    """
    Update the transaction records in the database for a given user and stock.
    
    :param user_id: User ID.
    :param ticker: Stock ticker symbol.
    :param lot_size: Number of shares to buy/sell for a transaction.
    :param transaction_type: Type of transaction (BUY or SELL).
    :param current_price: Current price of the stock.
    :return: Tuple showing success/failure and a message describing the outcome.
    """
    conn = connect_to_database()
    if conn is not None:
        try:
            with conn.cursor() as cur:
                # demo account ID associated with the user
                cur.execute("SELECT demo_id FROM demo_accounts WHERE user_id = %s;", (user_id,))
                demo_id = cur.fetchone()[0]

                # Insert the new transaction into the transactions table
                cur.execute("""
                    INSERT INTO transactions (transaction_type, stock_symbol, quantity, price, demo_id)
                    VALUES (%s, %s, %s, %s, %s);
                """, (transaction_type, ticker, lot_size, current_price, demo_id))

                conn.commit()
                return True, f"Transaction successful: {transaction_type} {lot_size} shares of {ticker} at ${current_price:.2f} each."
        except Exception as e:
            return False, f"Database operation failed: {str(e)}"
        finally:
            conn.close()
    else:
        return False, "Failed to connect to the database."

def buy_stock(ticker, lot_size):
    """
    Execute a BUY transaction for a given ticker and lot size.
    :param ticker: Stock ticker symbol.
    :param lot_size: Number of shares to purchase.
    """
    
    
    current_price = get_current_price(ticker)
    user_id = st.session_state.user_id
    total_purchase_price = current_price * lot_size
    margin_required = total_purchase_price * MARGIN_PERCENTAGE / 100

    # Check if the user has enough balance to cover the margin
    has_account, demo_id, balance = check_or_create_demo_account(user_id)
    if not has_account:
        st.error("Demo account does not exist or could not be created.")
        return

    if balance < margin_required:

        placeholder = st.empty()
        # Show a message
        placeholder.error(f"Insufficient balance to cover the margin required for this purchase. Margin required: ${margin_required}")
        # Wait for 2 seconds
        time.sleep(2)
        # Clear the message
        placeholder.empty()
        return

    # Proceed with the transaction since the balance is sufficient to cover the margin
    success, message = update_transaction(user_id, ticker, lot_size, "BUY", current_price)
    if success:
        # Deduct the margin required for the buy position from the account balance
        update_account_balance(user_id, -margin_required)
        
        placeholder = st.empty()
        # Show a message
        placeholder.success(message)
        # Wait for 3 seconds
        time.sleep(3)
        # Clear the message
        placeholder.empty()
    else:
        st.error(message)

def sell_stock(ticker, lot_size):
    """
    Execute a SELL transaction for a given ticker and lot size.
    
    :param ticker: Stock ticker symbol.
    :param lot_size: Number of shares to purchase.
    """
    
    current_price = get_current_price(ticker)
    user_id = st.session_state.user_id
    total_purchase_price = current_price * lot_size
    margin_required = total_purchase_price * MARGIN_PERCENTAGE / 100

    # Check if the user has enough balance to cover the margin
    has_account, demo_id, balance = check_or_create_demo_account(user_id)
    if not has_account:
        st.error("Demo account does not exist or could not be created.")
        return

    if balance < margin_required:
        placeholder = st.empty()
        # Show a message
        placeholder.error(f"Insufficient balance to cover the margin required for this purchase. Margin required: ${margin_required}")
        # Wait for 2 seconds
        time.sleep(2)
        # Clear the message
        placeholder.empty()
        return

    success, message = update_transaction(user_id, ticker, lot_size, "SELL", current_price)
    if success:
        # margin required for the sell position to the account balance
        update_account_balance(user_id, -margin_required)
        
        placeholder = st.empty()
        # Show a message
        placeholder.success(message)
        # Wait for 3 seconds
        time.sleep(3)
        # Clear the message
        placeholder.empty()
    else:
        st.error(message)
        
def update_account_balance(user_id, amount):
    """
    Update the balance of a user's demo account.
    
    :param user_id: User ID.
    :param amount: Amount to update in the user's account balance.
    """
    conn = connect_to_database()
    if conn is not None:
        try:
            # Updates the amount allocated to the demo account
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE demo_accounts
                    SET allocated_amount = allocated_amount + %s
                    WHERE user_id = %s;
                """, (amount, user_id))
                conn.commit()
        except Exception as e:
            print(f"Failed to update account balance: {str(e)}")
        finally:
            conn.close()

def calculate_moving_averages(data, windows=[20, 50]):
    """
    Calculate moving averages for the Close price over specified window sizes.
    
    :param data: DataFrame containing stock price data.
    :param windows: window sizes for Moving Average.
    :return: DataFrame with additional columns for each moving average.
    """
    for window in windows:
        # Calculate and add moving average to the DataFrame for each specified window size
        data[f'MA{window}'] = data['Close'].rolling(window=window).mean()
    return data

def calculate_bollinger_bands(data, window=20, num_of_std=2):
    """
    Calculate Bollinger Bands for the'Close price data.
    
    :param data: DataFrame containing stock price data.
    :param window: moving average window for Bollinger band.
    :param num_of_std: Number of standard deviations to use for the upper and lower bands.
    :return: DataFrame with additional columns for Bollinger Bands.
    """
    
    # Calculate the moving average for the specified window
    data['MA20'] = data['Close'].rolling(window=window).mean()
    # Calculate the standard deviation for the same window
    data['STD20'] = data['Close'].rolling(window=window).std()
     # Calculate the upper Bollinger Band
    data['UpperBB'] = data['MA20'] + (data['STD20'] * num_of_std)
    # Calculate the lower Bollinger Band
    data['LowerBB'] = data['MA20'] - (data['STD20'] * num_of_std)
    return data

def trade_stocks():
    """
    Display the stock trading page for buying or selling stocks.
    """
    
    st.subheader("Trade Stocks")
    
    # Scrape S&P 500 tickers
    sp500_tickers = scrape_sp500_tickers()
    
    # options for the selectbox
    options = [f"{ticker} - {company}" for ticker, company in sp500_tickers]
    # Sort options alphabetically by company name
    options.sort()
    selected_option = st.selectbox("Select a company:", options)
    ticker = selected_option.split(" - ")[0]
    
    if ticker:
        try:
            # fetch and display the current price of the selected ticker
            current_price = get_current_price(ticker)
            st.write(f"Current Price of {ticker}: ${current_price:.2f}")
        except Exception:
            st.error("Failed to fetch current price. Please check the ticker and try again.")
            return
        
        # # User input for the number of shares to trade
        lot_size = st.number_input("Enter lot size (number of shares):", min_value=1, step=1)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Buy"):
                buy_stock(ticker, lot_size)
                st.rerun()
        with col2:
            if st.button("Sell"):
                sell_stock(ticker, lot_size)
                st.rerun()
                
        # User input for start date of the stock data to fetch and display
        start_date = st.date_input("Start Date", value=datetime.date.today() - datetime.timedelta(days=365))
        data = load_dataset(ticker, start_date=start_date)
        if not data.empty:
            analysis_options = st.multiselect('Select Analysis Options', ['Moving Averages', 'Bollinger Bands'])
            fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'])])
            
            # Add moving average lines to the plot if selected
            if 'Moving Averages' in analysis_options:
                data = calculate_moving_averages(data)
                for window in [20, 50]:
                    fig.add_trace(go.Scatter(x=data.index, y=data[f'MA{window}'], mode='lines', name=f'MA{window}'))
                    
             # Add Bollinger Bands to the plot if selected
            if 'Bollinger Bands' in analysis_options:
                data = calculate_bollinger_bands(data)
                fig.add_trace(go.Scatter(x=data.index, y=data['UpperBB'], mode='lines', name='Upper Bollinger Band', line=dict(color='rgba(250, 0, 0, 0.75)')))
                fig.add_trace(go.Scatter(x=data.index, y=data['LowerBB'], mode='lines', name='Lower Bollinger Band', line=dict(color='rgba(0, 0, 250, 0.75)')))

            fig.update_layout(title=f"{ticker} Analysis", xaxis_title="Date", yaxis_title="Price", template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
            

def display_open_trades(user_id):
    """
    Display open trades for a user.
    
    :param user_id: User ID.
    """
    conn = connect_to_database()
    if conn is not None:
        try:
            
            # fetches all of the transactions allocated to the users created demo account
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT transaction_id, transaction_type, stock_symbol, quantity, price, timestamp
                    FROM transactions
                    WHERE demo_id = (
                        SELECT demo_id FROM demo_accounts WHERE user_id = %s
                    ) AND status = 'OPEN';
                """, (user_id,))

                trades = cur.fetchall()

                if trades:
                    
                    # Initalizes the Dataframe to store open trades
                    df = pd.DataFrame(trades, columns=['Transaction ID', 'Type', 'Symbol', 'Quantity', 'Price', 'Timestamp'])
                    st.subheader("Open Trades")
                    
                    # defines the columns of the open trades frame
                    cols = st.columns([3, 3, 3, 3, 3, 3, 3, 3, 3])
                    headers = ['Transaction ID', 'Type', 'Symbol', 'Quantity', 'Price', 'Timestamp', 'Gain/Loss %', 'Gain/Loss $', 'Action']
                    for col, header in zip(cols, headers):
                        col.write(header)
                        
                        
                    for index, row in df.iterrows():
                        cols = st.columns([3, 3, 3, 3, 3, 3, 3, 3, 3])
                        cols[0].write(row['Transaction ID'])
                        cols[1].write(row['Type'])
                        cols[2].write(row['Symbol'])
                        cols[3].write(row['Quantity'])
                        cols[4].write(f"${row['Price']:.2f}")
                        cols[5].write(row['Timestamp'].strftime('%Y-%m-%d %H:%M:%S'))

                        current_price = get_current_price(row['Symbol'])
                        price = float(row['Price'])
                        quantity = row['Quantity']
                        
                        # calculate gain/loss value 
                        if row['Type'] == 'BUY':
                            dollar_gain_loss = (current_price - price) * quantity  
                        else:
                            dollar_gain_loss = (price - current_price) * quantity
                        
                        gain_loss_percentage = (dollar_gain_loss / (price * quantity)) * 100
                        
                        if gain_loss_percentage >= 0:
                            color = 'green'
                            
                        else:
                            color = 'red'
                        
                        # HTML Markdown to display gain in green or loss in red
                        cols[6].markdown(f"<span style='color:{color};'>{gain_loss_percentage:+.2f}%</span>", unsafe_allow_html=True)
                        cols[7].markdown(f"<span style='color:{color};'>${dollar_gain_loss:+.2f}</span>", unsafe_allow_html=True)

                        if cols[8].button("Close Position", key=row['Transaction ID']):
                            close_trade(user_id, row['Transaction ID'])
                            st.rerun()

                else:
                    st.write("No open trades found.")

        except Exception as e:
            st.error(f"Failed to fetch open trades: {e}")
        finally:
            conn.close()
    else:
        st.error("Failed to connect to the database.")

        

    
        
def close_trade(user_id, transaction_id):
    """
    Close an open trade for a user by reversing the transaction type and updating the account balance.
    
    :param user_id: User ID.
    :param transaction_id: ID of the transaction to close.
    """
    conn = connect_to_database()
    if conn is not None:
        try:
            with conn.cursor() as cur:
                # Fetch the original transaction details
                cur.execute("""
                    SELECT stock_symbol, quantity, price, transaction_type
                    FROM transactions
                    WHERE transaction_id = %s;
                """, (transaction_id,))
                transaction = cur.fetchone()

                if transaction:
                    stock_symbol, quantity, price, transaction_type = transaction
                    current_price = get_current_price(stock_symbol)

                    # Ensure all numbers are floats for calculation
                    transaction_price = float(price)
                    quantity = float(quantity)
                    current_price = float(current_price)

                    margin_used = transaction_price * quantity * MARGIN_PERCENTAGE / 100

                    # Determine profit or loss
                    if transaction_type == 'BUY':
                        profit_loss = (current_price - transaction_price) * quantity
                        net_balance_change = profit_loss + margin_used  # Return margin and add profit or deduct loss
                    else:  # SELL
                        profit_loss = (transaction_price - current_price) * quantity
                        net_balance_change = profit_loss + margin_used  # Return margin and add profit or deduct loss

                    # Reverse the transaction type for closing the trade
                    reverse_type = 'BUY' if transaction_type == 'SELL' else 'SELL'

                    # Insert the closing transaction
                    cur.execute("""
                        INSERT INTO transactions (transaction_type, stock_symbol, quantity, price, demo_id, status)
                        VALUES (%s, %s, %s, %s, (
                            SELECT demo_id FROM demo_accounts WHERE user_id = %s
                        ), 'CLOSED');
                    """, (reverse_type, stock_symbol, quantity, current_price, user_id))

                    # Update the original transaction to mark it as closed
                    cur.execute("""
                        UPDATE transactions
                        SET status = 'CLOSED'
                        WHERE transaction_id = %s;
                    """, (transaction_id,))
                    
                    # Update the account balance
                    update_account_balance(user_id, net_balance_change)

                    conn.commit()
                    
                    placeholder = st.empty()

                    # Show a message
                    placeholder.success(f"Trade closed successfully. Transaction type: {reverse_type}, Quantity: {quantity}, Price: ${current_price:.2f}, Profit/Loss: ${profit_loss:.2f}")

                    # Wait for 5 seconds
                    time.sleep(5)

                    # Clear the message
                    placeholder.empty()

                else:
                    st.error("Original transaction not found.")
        except Exception as e:
            st.error(f"Failed to close trade: {e}")
        finally:
            conn.close()
    else:
        st.error("Failed to connect to the database.")
        
        
def calculate_current_holdings(user_id):
    """
    Calculate the total current holdings value for a user account based on open transactions.
    
    :param user_id: User's ID.
    """
    conn = connect_to_database()
    if conn:
        try:
            # Initialize total holdings value
            total_holdings_value = 0.0  
            with conn.cursor() as cur:
                # Fetch all open transactions for the user
                cur.execute("""
                SELECT stock_symbol, transaction_type, quantity, price
                FROM transactions
                WHERE demo_id = (SELECT demo_id FROM demo_accounts WHERE user_id = %s) AND status = 'OPEN';
                """, (user_id,))
                
                
                for row in cur.fetchall():
                    symbol, transaction_type, quantity, transaction_price = row
                    current_price = get_current_price(symbol)
                    
                    
                    transaction_price = float(transaction_price)
                    
                    if transaction_type == 'BUY':
                        # Calculate the change in value since the transaction
                        value_change = (current_price - transaction_price) * quantity
                    else:  # transaction_type == 'SELL'
                        # Calculate the change in value since the transaction, reverse for sell
                        value_change = (transaction_price - current_price) * quantity

                    total_holdings_value += value_change
            
            # Display the total current holdings value, can be negative or positive
            st.write(f"Total Current Holdings Value: ${total_holdings_value:.2f}")
            
        except Exception as e:
            st.error(f"Failed to calculate current holdings: {e}")
        finally:
            conn.close()
    else:
        st.error("Failed to connect to the database.")



            
def check_or_create_demo_account(user_id):
    """
    Check if a user has an existing demo account or create one if it does not exist.
    
    :param user_id: User's ID.
    :return: Tuple indicating if an account exists, the account ID, and the balance.
    """
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
    """
    Allocate an initial amount to a user's new demo account.
    
    :param user_id: User ID.
    :return: ID of the newly created demo account or None if creation failed.
    """
    
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
    """
    Display the demo trading interface for a logged-in user.
    """
    
    st.title("Demo Trading Account")
    
    if 'user_id' not in st.session_state:
        st.warning("Please log in to continue.")  
        return

    user_id = st.session_state['user_id']
    
    # checks if the user has an existing demo account
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
        calculate_current_holdings(user_id)

# checking for available user_id in the current session
user_id = st.session_state.get('user_id', None)
if user_id:
    show_demo_trading()
    st.session_state['current_page'] = 'demo_trading'
else:
    st.error('Please log in to view Demo trading.')


    
    

import pandas as pd
import datetime
import calendar
from database import connect_to_database
import streamlit as st

def fetch_trade_days(user_id, year, month):
    conn = connect_to_database()
    trade_days = []
    if conn is not None:
        try:
            with conn.cursor() as cur:
                # Adjust the query to join with the demo_accounts table
                sql_query = """
                SELECT DISTINCT DATE(t.timestamp)
                FROM transactions t
                JOIN demo_accounts d ON t.demo_id = d.demo_id
                WHERE EXTRACT(MONTH FROM t.timestamp) = %s
                  AND EXTRACT(YEAR FROM t.timestamp) = %s
                  AND d.user_id = %s;
                """
                cur.execute(sql_query, (month, year, user_id))
                result = cur.fetchall()
                trade_days = [day[0].day for day in result]  
        except Exception as e:
            st.error(f"Database query failed: {e}")
        finally:
            conn.close()
    return trade_days


def display_calendar(user_id):
    # Current year and month
    now = datetime.datetime.now()
    year, month = now.year, now.month

    trade_days = fetch_trade_days(user_id, year, month)
    
    # calendar for the current month
    cal = calendar.monthcalendar(year, month)
    cal_df = pd.DataFrame(cal, columns=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    
    # Replace trade days with flames
    cal_df = cal_df.applymap(lambda day: '🔥' if day in trade_days else day if day != 0 else '')
    
    # Display the current month as a header
    month_name = calendar.month_name[month]
    st.header(f"Streak Calendar for {month_name} {year}")  # Display the current month and year as a header
    st.table(cal_df)
    
    
    

# Usage example
user_id = st.session_state.get('user_id', None)
if user_id:
    display_calendar(user_id)
else:
    st.error('Please log in to view the trading calendar.')
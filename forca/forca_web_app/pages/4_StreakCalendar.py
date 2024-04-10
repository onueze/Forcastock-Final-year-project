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
                # Adjusted the query to join with the demo_accounts table
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


def display_calendar(user_id, current_day=None):
    # Current year and month
    now = datetime.datetime.now()
    year, month = now.year, now.month

    # If current_day is not provided, use the current day from datetime
    if current_day is None:
        current_day = now.day

    trade_days = fetch_trade_days(user_id, year, month)
    
    # calendar for the current month
    cal = calendar.monthcalendar(year, month)
    cal_df = pd.DataFrame(cal, columns=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    
    # trade days with flames, and mark the current day with an calendar emoji
    def mark_days(day):
        if day == current_day and day in trade_days:
            return f'📆🔥 {day}'
        
        elif day == current_day:
            return f'📆 {day}'
        
        if day in trade_days:
            return f'🔥 {day}'
        
        return day if day != 0 else ''

    cal_df = cal_df.applymap(mark_days)
    
    # Display the current month as a header
    month_name = calendar.month_name[month]
    st.header(f"Streak Calendar for {month_name} {year}")
    st.table(cal_df)

    
    
    

# Usage example
user_id = st.session_state.get('user_id', None)
if user_id:
    display_calendar(user_id)
else:
    st.error('Please log in to view the trading calendar.')
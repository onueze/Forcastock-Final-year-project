import plotly.graph_objects as go
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
                # Query to select trade dates within the specified month and year for the given user
                sql_query = """
                SELECT DISTINCT DATE(timestamp)
                FROM transactions
                WHERE EXTRACT(MONTH FROM timestamp) = %s AND EXTRACT(YEAR FROM timestamp) = %s AND user_id = %s;
                """
                cur.execute(sql_query, (month, year, user_id))
                result = cur.fetchall()
                trade_days = [datetime.date(year, month, day[0].day) for day in result]
        except Exception as e:
            print(f"Database query failed: {e}")
        finally:
            conn.close()
    return trade_days

def create_calendar(user_id, year, month):
    trade_days = fetch_trade_days(user_id, year, month)

    # Continue with calendar creation as before
    cal = calendar.monthcalendar(year, month)
    day_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    fig = go.Figure()

    for week in cal:
        for idx, day in enumerate(week):
            if day != 0:
                color = 'lightgreen' if datetime.date(year, month, day) in trade_days else 'white'
                fig.add_trace(go.Scatter(
                    x=[idx], y=[-cal.index(week)],
                    text=[str(day)],
                    mode='text',
                    textfont=dict(color='black', size=20),
                    marker=dict(color=color, size=20),
                    showlegend=False
                ))

    # Add grid and day labels as before
    # ...

    fig.update_layout(
        title=f'Calendar: {year}-{month}',
        height=300,
        width=600,
        plot_bgcolor='grey',
        margin=dict(l=0, r=0, t=30, b=0),
    )

    return fig

# Example usage
user_id = st.session_state.get('user_id', None)
if user_id:
    fig = create_calendar(user_id, 2023, 9)
    st.plotly_chart(fig)
else:
    st.error('Please log in to view the trading calendar.')

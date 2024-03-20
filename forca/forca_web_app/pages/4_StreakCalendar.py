import streamlit as st


user_id = st.session_state.get('user_id', None)
if user_id:
    pass
else:
    st.error('Please log in to view Stock prediction.')
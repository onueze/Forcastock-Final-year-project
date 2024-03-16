import streamlit as st
from streamlit_option_menu import option_menu
from app import app
from database import create_all_tables

def main():
    print('executing')
    st.set_page_config(page_title='Forcastock', page_icon=':chart:', layout='wide')
    
    # Create database tables
    create_all_tables()

    # Run the Streamlit app
    print('not ran')
    app()
    print('ran')


if __name__ == '__main__':
    main()

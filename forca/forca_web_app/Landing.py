import streamlit as st
from app import app
from database import create_all_tables

def main():
    
    # Create database tables
    create_all_tables()
    
    # Run the Streamlit app
    app()


if __name__ == '__main__':
    main()



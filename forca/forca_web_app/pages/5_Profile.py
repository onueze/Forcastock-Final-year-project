import streamlit as st
from database import connect_to_database
import pandas as pd

def logout_user():
    # Logic to log out the user
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
    
    
def display_profile_info():

    # Retrieve the user's information from session state or database
    user_info = st.session_state['user_id']  # Implement this function

    # Display the user profile information
    st.subheader('Account Details')
    st.text(f"User ID: {st.session_state['user_id']}")
    st.text(f"Email: {st.session_state['user_email']}")


def view_all_transactions(user_id):
    # Fetch and display all transactions from the database
    conn = connect_to_database()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT * FROM transactions
                    WHERE demo_id = (
                        SELECT demo_id FROM demo_accounts WHERE user_id = %s
                    );
                """, (user_id,))
                transactions = cur.fetchall()
                if transactions:
                    df = pd.DataFrame(transactions, columns=['Transaction ID', 'Type', 'Symbol', 'Quantity', 'Price', 'Timestamp', 'DemoID', 'Status'])
                    st.write(df)
                else:
                    st.write("No transactions found.")
        except Exception as e:
            st.error("Failed to fetch transactions: " + str(e))
        finally:
            conn.close()
    else:
        st.error("Failed to connect to the database.")

def delete_demo_account(user_id):
    
    if st.button('Delete Demo Account'):
        conn = connect_to_database()
        if conn:
            try:
                with conn.cursor() as cur:
                    # fetch the demo_id to delete related transactions
                    cur.execute("SELECT demo_id FROM demo_accounts WHERE user_id = %s;", (user_id,))
                    demo_id = cur.fetchone()
                    if demo_id:
                        # Delete transactions related to this demo account
                        cur.execute("DELETE FROM transactions WHERE demo_id = %s;", (demo_id[0],))

                        # delete the demo account itself
                        cur.execute("DELETE FROM demo_accounts WHERE user_id = %s;", (user_id,))
                        conn.commit()
                        st.success("Demo account and related transactions deleted successfully.")
                    else:
                        st.error("No demo account found for the given user.")
            except Exception as e:
                conn.rollback()  # Important to rollback in case of error
                st.error("Failed to delete demo account: " + str(e))
            finally:
                conn.close()
        else:
            st.error("Failed to connect to the database.")
            
            
def delete_user_account(user_id):
    # Logic to delete a user account
    if st.button('Delete User Account'):
        conn = connect_to_database()
        if conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
                    conn.commit()
                    st.success("User account deleted successfully.")
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                        st.rerun()
            except Exception as e:
                st.error("Failed to delete user account: " + str(e))
            finally:
                conn.close()
        else:
            st.error("Failed to connect to the database.")
            
            

def profile_page(user_id):
    st.title('Profile')

    tab1, tab2, tab3, tab4 = st.tabs(['Profile Information', 'Transactions History', 'Demo Account Management', 'Account Settings'])

    with tab1:
        st.header('Profile Information')
        display_profile_info()

    with tab2:
        st.header('Transactions History')
        view_all_transactions(user_id)

    with tab3:
        st.header('Demo Account Management')
        delete_demo_account(user_id)

    with tab4:
        st.header('Account Settings')
        delete_user_account(user_id)
        if st.button('Log Out'):
            logout_user()


user_id = st.session_state.get('user_id', None)
if user_id:
    profile_page(user_id)
else:
    st.error('Please log in to view Profile.')

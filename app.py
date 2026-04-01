import streamlit as st
import pandas as pd
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Finance Tracker", page_icon="💰")

# --- CUSTOM CSS FOR MOBILE ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- APP HEADER ---
st.title("💸 Personal Finance Tracker")
st.write("Welcome! This app helps you track your balance with a touch of personality.")

# --- SESSION STATE FOR HISTORY ---
if 'history' not in st.session_state:
    st.session_state.history = []

# --- INPUT SECTION ---
with st.container():
    st.subheader("Add Transaction")
    desc = st.text_input("Description (e.g., Grocery, Salary)", placeholder="What was this for?")
    amount = st.number_input("Amount", min_value=0.0, step=1.0)
    category = st.selectbox("Type", ["Income", "Expense"])

    if st.button("Submit Transaction"):
        if amount > 0 and desc:
            new_data = {
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Description": desc,
                "Amount": amount if category == "Income" else -amount,
                "Type": category
            }
            st.session_state.history.append(new_data)
            
            # The "Hehe Boy" / "Faah" Logic
            if category == "Income":
                st.balloons()
                st.success(f"Hehe boy! Added {amount} to your balance.")
            else:
                st.snow()
                st.error(f"Faah! Spent {amount}. Budgeting time!")
        else:
            st.warning("Please enter a description and amount.")

# --- DASHBOARD ---
st.divider()
if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    total_balance = df['Amount'].sum()
    
    col1, col2 = st.columns(2)
    col1.metric("Current Balance", f"${total_balance:,.2f}")
    col2.metric("Total Items", len(df))

    st.subheader("Transaction History")
    # Show the table (looks great on Android/iOS)
    st.dataframe(df, use_container_width=True)
    
    if st.button("Clear History"):
        st.session_state.history = []
        st.rerun()
else:
    st.info("No transactions yet. Start by adding one above!")

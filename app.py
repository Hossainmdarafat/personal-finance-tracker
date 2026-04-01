import streamlit as st
import pandas as pd
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Finance Tracker", page_icon="💰")

# --- SOUND LOGIC ---
# Using public URLs for the sounds so they work anywhere without uploading files
HEHE_BOY = "https://www.myinstants.com/media/sounds/hehe-boy.mp3"
FAAH = "https://www.myinstants.com/media/sounds/ah-fuck-i-cant-believe-youve-done-this.mp3" # A classic 'faah' style sound

def play_audio(url):
    st.audio(url, format="audio/mp3", autoplay=True)

# --- APP HEADER ---
st.title("💸 Personal Finance Tracker")
st.write("Track your balance and enjoy the vibes!")

if 'history' not in st.session_state:
    st.session_state.history = []

# --- INPUT SECTION ---
with st.container():
    st.subheader("Add Transaction")
    desc = st.text_input("Description", placeholder="What was this for?")
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
            
            if category == "Income":
                st.balloons()
                st.success("Hehe boy! Added!")
                play_audio(HEHE_BOY)
            else:
                st.snow()
                st.error("Faah! Spent it!")
                play_audio(FAAH)
        else:
            st.warning("Please enter a description and amount.")

# --- DASHBOARD ---
st.divider()
if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    total_balance = df['Amount'].sum()
    st.metric("Current Balance", f"${total_balance:,.2f}")
    st.dataframe(df, use_container_width=True)
    
    if st.button("Clear History"):
        st.session_state.history = []
        st.rerun()

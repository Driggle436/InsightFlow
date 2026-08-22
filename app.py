import streamlit as st

from config import get_connection


st.title("InsightFlow AI")

try:
    connection = get_connection()

    st.success("Connected to MySQL successfully!")

    cursor = connection.cursor()
    cursor.execute("SELECT DATABASE();")

    database = cursor.fetchone()[0]

    st.write(f"Connected database: `{database}`")

    cursor.close()
    connection.close()

except Exception as e:
    st.error(f"MySQL connection failed: {e}")
# app.py - Streamlit starter for MCP Server demo (Stage 1)
import streamlit as st

st.set_page_config(page_title="MCP Demo Streamlit", page_icon="🚀", layout="centered")

st.title("MCP Server Demo — Stage 1")
st.markdown("This is a simple Streamlit app used as the demo repo baseline. We'll extend this app in later stages.")

st.sidebar.header("Demo controls (local)")
branch = st.sidebar.text_input("Branch name to create (local)", value="feature-1")
make_change = st.sidebar.button("Make a minor local change")

st.header("Hello, world")
st.write("This app will be extended across stages to demonstrate PRs, reviews, security scans, and automation via the GitHub MCP Server.")

if make_change:
    st.info("Made a small local change. Commit & push using the Source Control panel.")
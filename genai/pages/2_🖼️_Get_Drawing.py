import streamlit as st
import requests
st.set_page_config(page_title="XmasMagicPic", page_icon="🎨", layout="centered", initial_sidebar_state="collapsed")

st.title("Xmas Magic Pic")
st.subheader("Transform Your Photos into Holiday Magic")

uploaded_file = st.file_uploader("Upload your image", type=['png', 'jpeg', 'jpg'])

if uploaded_file is not None:
    response = requests.get("https://dog.ceo/api/breeds/image/random", verify=False).json()
    if response['status'] == 'success':
        st.image(response['message'], width=100)
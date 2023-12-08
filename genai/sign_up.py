import streamlit as st
import boto3
import hashlib
import hmac
import base64
from st_pages import hide_pages

st.set_page_config(page_title="Pixar Star", page_icon="⭐", layout="centered", initial_sidebar_state="collapsed")
hide_pages(["Payment", "Create"])

# Initialize the Cognito client
client = boto3.client('cognito-idp', region_name=st.secrets.region_name)

# Initialization state variables
if 'email' not in st.session_state:
    st.session_state['email'] = ''
if 'secret_hash' not in st.session_state:
    st.session_state['secret_hash'] = ''
if 'confirm_code' not in st.session_state:
    st.session_state['confirm_code'] = ''

# Create a Streamlit sign-up form
st.title("Sign Up")
email = st.text_input("Email").lower()
password = st.text_input("Password", type="password")
confirm_password = st.text_input("Confirm Password", type="password")
submit_button = st.button("Sign Up")

# Calculate SECRET_HASH
message = email + st.secrets.APP_CLIENT_ID
key = st.secrets.APP_CLIENT_SECRET.encode('utf-8')
msg = message.encode('utf-8')
secret_hash = base64.b64encode(hmac.new(key, msg, digestmod=hashlib.sha256).digest()).decode()
st.session_state['secret_hash'] = secret_hash
st.session_state['email'] = email

if submit_button:
    if password != confirm_password:
        st.error("Passwords do not match")
    else:
        try:
            response = client.sign_up(
                ClientId=st.secrets.APP_CLIENT_ID,
                Username=st.session_state['email'],
                Password=password,
                SecretHash=secret_hash,
            )
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                st.info("Please check your email for the confirmation code.")
        except Exception as e:
            st.error("An error occurred during sign-up.")
            st.error(str(e))

confirm_code = st.text_input("Confirmation Code")
confirm_button = st.button("Confirm")
st.session_state['confirm_code'] = confirm_code
if confirm_button:
    # st.write("Confirm Button clicked!")
    # st.write(st.session_state['confirm_code'])
    # st.write(st.session_state['email'])
    try:
        response = client.confirm_sign_up(
            ClientId=st.secrets.APP_CLIENT_ID,
            Username=st.session_state['email'],
            ConfirmationCode=st.session_state['confirm_code'],
            SecretHash=st.session_state['secret_hash']
        )
        # st.info(response)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            # st.success("User confirmed successfully! Sign in")
            st.markdown(f"""User confirmed successfully!
            <a href="{st.secrets.APP_URI}" target = "_self"> 
            Sign in </a>""", unsafe_allow_html=True)
    except Exception as e:
        st.error("An error occurred during confirmation.")
        st.error(str(e))
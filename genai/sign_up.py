import streamlit as st
import boto3
import hashlib
import hmac
import base64

st.set_page_config(page_title="Pixar Star", page_icon="⭐", layout="centered", initial_sidebar_state="collapsed")
# show_pages_from_config()

# Set your Cognito pool id, app client id, and region
POOL_ID = "eu-west-1_WdFlA4Rm6"
APP_CLIENT_ID = "7l2hl2qjicg992bl39gt7lfdk1"
APP_CLIENT_SECRET = "3lbq6m9j87uqn68t7elj4urbo75m1gjp70qu2i2gcdoe3hpu888"
REGION_NAME = "eu-west-1"

# Initialize the Cognito client
client = boto3.client('cognito-idp', region_name=REGION_NAME)

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
message = email + APP_CLIENT_ID
key = APP_CLIENT_SECRET.encode('utf-8')
msg = message.encode('utf-8')
SECRET_HASH = base64.b64encode(hmac.new(key, msg, digestmod=hashlib.sha256).digest()).decode()
st.session_state['secret_hash'] = SECRET_HASH

if submit_button:
    if password != confirm_password:
        st.error("Passwords do not match")
    else:
        st.session_state['email'] = email
        try:
            response = client.sign_up(
                ClientId=APP_CLIENT_ID,
                Username=st.session_state['email'],
                Password=password,
                SecretHash=SECRET_HASH,
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
    st.write("Confirm Button clicked!")
    st.write(st.session_state['confirm_code'])
    st.write(st.session_state['email'])
    try:
        response = client.confirm_sign_up(
            ClientId=APP_CLIENT_ID,
            Username=st.session_state['email'],
            ConfirmationCode=st.session_state['confirm_code'],
            SecretHash=st.session_state['secret_hash']
        )
        st.info(response)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            st.success("User confirmed successfully!")
    except Exception as e:
        st.error("An error occurred during confirmation.")
        st.error(str(e))
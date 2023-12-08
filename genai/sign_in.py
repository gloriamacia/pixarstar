import streamlit as st
import boto3
import hashlib
import hmac
import base64
from st_pages import Page, show_pages, hide_pages


st.set_page_config(page_title="Pixar Star", page_icon="⭐", layout="centered", initial_sidebar_state="collapsed")
# show_pages_from_config()
show_pages(
        [
            Page("sign_in.py", "Sign in", "🔓"),
            Page("sign_up.py", "Sign Up", "🙋🏽‍♀️"),
            Page("payment.py", "Payment", "💰"),
            Page("create.py", "Create", "🎨"),
            
        ]
    )
hide_pages(["Payment", "Sign Up"])

# Initialize the Cognito client
client = boto3.client('cognito-idp', region_name=st.secrets.region_name)

# Create a Streamlit sign-up form
st.title("Sign In")
email = st.text_input("Email").lower()
password = st.text_input("Password", type="password")
submit_button = st.button("Sign In")
st.markdown("""Not a member?
    <a href="http://localhost:8501/Sign%20Up" target = "_self"> 
        Sign Up
    </a>
""", unsafe_allow_html=True)

# Calculate SECRET_HASH
message = email + st.secrets.APP_CLIENT_ID
key = st.secrets.APP_CLIENT_SECRET.encode('utf-8')
msg = message.encode('utf-8')
secret_hash = base64.b64encode(hmac.new(key, msg, digestmod=hashlib.sha256).digest()).decode()

if submit_button:
    try:
        response = client.initiate_auth(
            ClientId=st.secrets.APP_CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password,
                'SECRET_HASH': secret_hash
            }
        )
        st.success("User authenticated successfully! Start creating in the left menu.")
        # Extract the access token and refresh token from the response
        access_token = response['AuthenticationResult']['AccessToken']
        refresh_token = response['AuthenticationResult']['RefreshToken']
        st.session_state['token'] = access_token
    except client.exceptions.NotAuthorizedException:
        st.error("Incorrect user or password. Do you need to sign up?")
    except Exception as e:
        st.error("An error occurred during authentication.")
        st.error(str(e))
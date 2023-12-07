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

# Set your Cognito pool id, app client id, and region
POOL_ID = "eu-west-1_WdFlA4Rm6"
APP_CLIENT_ID = "7l2hl2qjicg992bl39gt7lfdk1"
APP_CLIENT_SECRET = "3lbq6m9j87uqn68t7elj4urbo75m1gjp70qu2i2gcdoe3hpu888"
REGION_NAME = "eu-west-1"

# Initialize the Cognito client
client = boto3.client('cognito-idp', region_name=REGION_NAME)

# Create a Streamlit sign-up form
st.title("Sign In")
email = st.text_input("Email").lower()
password = st.text_input("Password", type="password")
confirm_password = st.text_input("Confirm Password", type="password")
submit_button = st.button("Sign In")
st.markdown("""Not a member?
    <a href="http://localhost:8501/Sign%20Up" target = "_self"> 
        Sign Up
    </a>
""", unsafe_allow_html=True)

# Calculate SECRET_HASH
message = email + APP_CLIENT_ID
key = APP_CLIENT_SECRET.encode('utf-8')
msg = message.encode('utf-8')
SECRET_HASH = base64.b64encode(hmac.new(key, msg, digestmod=hashlib.sha256).digest()).decode()

if submit_button:
    if password != confirm_password:
        st.error("Passwords do not match")
    else:
        try:
            response = client.initiate_auth(
                ClientId=APP_CLIENT_ID,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': email,
                    'PASSWORD': password,
                    'SECRET_HASH': SECRET_HASH
                }
            )
            st.success("User authenticated successfully! Start creating in the left menu.")
            #st.success("User authenticated successfully! Start [creating](http://localhost:8501/Draw)")
            # Extract the access token and refresh token from the response
            access_token = response['AuthenticationResult']['AccessToken']
            refresh_token = response['AuthenticationResult']['RefreshToken']
            st.session_state['token'] = access_token
        #     # Do something with the access token and refresh token
        except client.exceptions.NotAuthorizedException:
            st.error("User not found in the database. Please [sign up](http://localhost:8501/Sign%20Up)")
        except Exception as e:
            st.error("An error occurred during authentication.")
            st.error(str(e))
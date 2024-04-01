import streamlit as st
import io
import warnings

from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from streamlit_image_comparison import image_comparison
from st_pages import hide_pages
import os
import stripe

# Navitation Configuration
st.set_page_config(page_title="Pixar Star", page_icon="🎬", layout="centered", initial_sidebar_state="collapsed")
hide_pages(["Sign Up", "Sign In"])

# Secrets & States
api_host = os.getenv("API_HOST", "https://api.stability.ai")
api_key = st.secrets.stability_key
stripe.api_key = st.secrets.stripe_restricted_key 

def customer_exists(email):
    try:
        # Retrieve the customer object from Stripe using email
        customers = stripe.Customer.list(email=email)
        return customers
    except stripe.error.InvalidRequestError as e:
        # Handle any potential errors
        print(f"Error: {e}")
        return False

def list_subscriptions_by_customer(customer_id):
    try:
        # List all subscriptions filtered by customer ID
        subscriptions = stripe.Subscription.list(customer=customer_id)
        
        return subscriptions
    except stripe.error.InvalidRequestError as e:
        # Handle any potential errors
        print(f"Error: {e}")
        return None

# Initialization state variables
if 'cognito_token' not in st.session_state:
    st.markdown(f"""To use the app, first
            <a href="{st.secrets.APP_URI}" target = "_self"> 
            sign in </a>""", unsafe_allow_html=True)
else:
    customer_email = st.session_state['email']
    # Set up our connection to the API.
    stability_api = client.StabilityInference(
        key=st.secrets["stability_key"], # API Key reference.
        verbose=True, # Print debug messages.
        engine="stable-diffusion-xl-1024-v1-0", # Set the engine to use for generation.
        # Check out the following link for a list of available engines: https://platform.stability.ai/docs/features/api-parameters#engine
    )

    st.title("Pixar Star 🎬")
    st.subheader("Transform Your Pet into a Pixar movie character")

    animal = st.text_input('What animal is your pet?')
    image = st.file_uploader("Upload your image", type=['png', 'jpeg', 'jpg'])
    prompt=f"{animal} in Disney style, Pixar animation, character design, adorable cute {animal} in Pixar style, beautiful eyes, 8k resolution, Disney Pixar movie poster, 3D render, high resolution, 4k, sharp borders, no blur"

    if image:
    # Check if the customer is in the database and has an active subscription 
        response = customer_exists(customer_email)
        if response['data']:
            customer_id = response['data'][0]['id']
            subscriptions = list_subscriptions_by_customer(customer_id)
            for subscription in subscriptions.auto_paging_iter():
                if subscription.status == 'active':
                    st.success("You are a paying customer. Your pixar character will render very soon. 🚀")
                    # Open the image using Pillow
                    img1 = Image.open(image)
                    img1 = img1.resize((512, 512))
                    answers = stability_api.generate(
                        prompt=prompt,
                        init_image=img1, # Assign our previously generated img as our Initial Image for transformation.
                        start_schedule=0.5, # Set the strength of our prompt in relation to our initial image.
                        seed=42, # If attempting to transform an image that was previously generated with our API,
                                        # initial images benefit from having their own distinct seed rather than using the seed of the original image generation.
                        steps=30, # Amount of inference steps performed on image generation. Defaults to 30.
                        cfg_scale=7, # Influences how strongly your generation is guided to match your prompt.
                                    # Setting this value higher increases the strength in which it tries to match your prompt.
                                    # Defaults to 7.0 if not specified.
                        width=512, # Generation width, defaults to 512 if not included.
                        height=512, # Generation height, defaults to 512 if not included.
                        sampler=generation.SAMPLER_K_DPMPP_2M # Choose which sampler we want to denoise our generation with.
                                                                    # Defaults to k_dpmpp_2m if not specified. Clip Guidance only supports ancestral samplers.
                                                                    # (Available Samplers: ddim, plms, k_euler, k_euler_ancestral, k_heun, k_dpm_2, k_dpm_2_ancestral, k_dpmpp_2s_ancestral, k_lms, k_dpmpp_2m, k_dpmpp_sde)
                    )
                    # Set up our warning to print to the console if the adult content classifier is tripped.
                    # If adult content classifier is not tripped, display generated image.
                    for resp in answers:
                        for artifact in resp.artifacts:
                            if artifact.finish_reason == generation.FILTER:
                                warnings.warn(
                                    "Your request activated the API's safety filters and could not be processed."
                                    "Please modify the prompt and try again.")
                            if artifact.type == generation.ARTIFACT_IMAGE:
                                st.balloons()
                                img2 = Image.open(io.BytesIO(artifact.binary)) # Set our resulting initial image generation as 'img2' to avoid overwriting our previous 'img' generation.
                                # st.image(img2, width=512)
                                image_comparison(
                                    img1=img1,
                                    img2=img2,
                                    label1="Original",
                                    label2="Gen AI",
                                    width=512,
                                    starting_position=50,
                                    show_labels=True,
                                    make_responsive=True,
                                    in_memory=True,
                                )      
                else: 
                    st.error("You are not yet a paying customer. Use the left menu to subscribe.")
        else: 
            st.error("You are not yet a paying customer. Use the left menu to subscribe.")
    
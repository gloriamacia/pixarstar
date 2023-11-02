import streamlit as st
import io
import warnings

from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from streamlit_image_comparison import image_comparison

# Set up our connection to the API.
stability_api = client.StabilityInference(
    key=st.secrets["stability_key"], # API Key reference.
    verbose=True, # Print debug messages.
    engine="stable-diffusion-xl-1024-v1-0", # Set the engine to use for generation.
    # Check out the following link for a list of available engines: https://platform.stability.ai/docs/features/api-parameters#engine
)

st.set_page_config(page_title="Pixar Star", page_icon="⭐", layout="centered", initial_sidebar_state="collapsed")

st.title("Pixar Star ⭐")
st.subheader("Transform Your Pet into a Pixar movie character")

image = st.file_uploader("Upload your image", type=['png', 'jpeg', 'jpg'])

if image is not None:
    # Open the image using Pillow
    img1 = Image.open(image)
    # Get the width and height of the image
    # width, height = img.size
    # left = (width - 512) / 2
    # top = (height - 512) / 2
    # right = (width + 512) / 2
    # bottom = (height + 512) / 2
    # cropped_image = img.crop((left, top, right, bottom))
    img1 = img1.resize((256, 256))
    answers = stability_api.generate(
    prompt="Disney style, Pixar animation, character design, adorable cute pet in Pixar style, 8k resolution, Disney Pixar movie poster, 3D render, high resolution, 4k, hyperrealistic",
    init_image=img1, # Assign our previously generated img as our Initial Image for transformation.
    start_schedule=0.6, # Set the strength of our prompt in relation to our initial image.
    seed=12345, # If attempting to transform an image that was previously generated with our API,
                    # initial images benefit from having their own distinct seed rather than using the seed of the original image generation.
    steps=50, # Amount of inference steps performed on image generation. Defaults to 30.
    cfg_scale=7, # Influences how strongly your generation is guided to match your prompt.
                # Setting this value higher increases the strength in which it tries to match your prompt.
                # Defaults to 7.0 if not specified.
    width=256, # Generation width, defaults to 512 if not included.
    height=256, # Generation height, defaults to 512 if not included.
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
                img2 = Image.open(io.BytesIO(artifact.binary)) # Set our resulting initial image generation as 'img2' to avoid overwriting our previous 'img' generation.
                # st.image(img2, width=256)
                image_comparison(
                    img1=img1,
                    img2=img2,
                    label1="Original",
                    label2="Gen AI",
                    width=256,
                    starting_position=50,
                    show_labels=True,
                    make_responsive=True,
                    in_memory=True,
                )

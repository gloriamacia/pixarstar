import streamlit as st
import streamlit.components.v1 as components
from st_pages import Page, show_pages, hide_pages

st.set_page_config(page_title="Pixar Star", page_icon="⭐", layout="centered", initial_sidebar_state="collapsed")
# show_pages_from_config()
show_pages(
        [
            Page("genai/streamlit_app.py", "Home", "🏠"),
            Page("genai/stability_ai_app.py", "Draw", "🎨")
        ]
    )
hide_pages(["Draw"])

stripe_js = """<script async
  src="https://js.stripe.com/v3/buy-button.js">
</script>

<stripe-buy-button
  buy-button-id="buy_btn_1O6spGAWMFUrkCpQokDCuxQR"
  publishable-key="{}"
>
</stripe-buy-button>
""".format(st.secrets["stripe_publishable_key"])

st.title("Pixar Star ⭐")
st.subheader("Transform Your Pet into a Pixar movie character")


components.html(html=stripe_js, height=300)


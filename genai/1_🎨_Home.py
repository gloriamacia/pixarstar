import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="XmasMagicPic", page_icon="🎨", layout="centered", initial_sidebar_state="collapsed")

stripe_js = """<script async
  src="https://js.stripe.com/v3/buy-button.js">
</script>

<stripe-buy-button
  buy-button-id="buy_btn_1O6spGAWMFUrkCpQokDCuxQR"
  publishable-key="{}"
>
</stripe-buy-button>
""".format(st.secrets["stripe_publishable_key"])

st.title("Xmas Magic Pic")
st.subheader("Transform Your Photos into Holiday Magic")


components.html(html=stripe_js, height=300)


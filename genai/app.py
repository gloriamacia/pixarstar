import streamlit as st
import streamlit.components.v1 as components

stripe_js = """<script async
  src="https://js.stripe.com/v3/buy-button.js">
</script>

<stripe-buy-button
  buy-button-id="buy_btn_1O6spGAWMFUrkCpQokDCuxQR"
  publishable-key="{}"
>
</stripe-buy-button>
""".format(st.secrets["stripe_publishable_key"])

st.title('Create your own generative AI artwork')



components.html(html=stripe_js,  height=600)
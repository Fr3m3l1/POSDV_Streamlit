import streamlit as st

st.set_page_config(initial_sidebar_state="collapsed")

st.markdown(
        """
    <style>
        [data-testid="collapsedControl"] {
            display: none
        }
    </style>
    """,
        unsafe_allow_html=True,
    )


st.title("404 - Page not found")
st.write("The page you are looking for does not exist.")
st.write("Please go back to the main page to continue exploring the Cardiotocography dataset.")
st.write("[Go back to the main page](/)")
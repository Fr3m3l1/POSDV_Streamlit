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


st.markdown("## Try your own Data")

st.markdown("Enter your own data in the text fields below:")

# Create text input fields for user input
input_fields = st.columns(9)
input_data = {}
for i in range(9):
    input_data[f"input_{i}"] = input_fields[i].text_input(f"Feature {i + 1}")

# Create a button to submit the data
if st.button("Submit"):
    # Display the user input
    st.write("You entered the following data:")
    for key, value in input_data.items():
        st.write(f"{key}: {value}")

# Create a button to clear the input fields
if st.button("Clear"):
    for key in input_data.keys():
        input_data[key] = ""
    st.write("Cleared all input fields")


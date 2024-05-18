import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from ucimlrepo import fetch_ucirepo 
import plotly.express as px

def main(featured_df, target_df):

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

    # Create text input fields for user input data
    # The user can input their own data for the features
    # The input data is stored in a dictionary
    user_input = {}
    user_input['LB'] = st.text_input('FHR baseline (beats per minute)', '130')
    user_input['AC'] = st.text_input('# of accelerations per second', '0')
    user_input['FM'] = st.text_input('# of fetal movements per second', '0')
    user_input['UC'] = st.text_input('# of uterine contractions per second', '0')
    user_input['DL'] = st.text_input('# of light decelerations per second', '0')
    user_input['DS'] = st.text_input('# of severe decelerations per second', '0')
    user_input['DP'] = st.text_input('# of prolongued decelerations per second', '0')
    user_input['ASTV'] = st.text_input('percentage of time with abnormal short term variability', '0')
    user_input['MSTV'] = st.text_input('mean value of short term variability', '0')
    user_input['ALTV'] = st.text_input('percentage of time with abnormal long term variability', '0')
    user_input['MLTV'] = st.text_input('mean value of long term variability', '0')
    user_input['Width'] = st.text_input('width of FHR histogram', '0')
    user_input['Min'] = st.text_input('minimum of FHR histogram', '0')
    user_input['Max'] = st.text_input('maximum of FHR histogram', '0')
    user_input['Nmax'] = st.text_input('# of histogram peaks', '0')
    user_input['Nzeros'] = st.text_input('# of histogram zeros', '0')
    user_input['Mode'] = st.text_input('histogram mode', '0')
    user_input['Mean'] = st.text_input('histogram mean', '0')

    # Create a button to submit the data
    if st.button('Submit'):
        # Check if the input is a number
        for key in user_input:
            try:
                user_input[key] = float(user_input[key])
            except ValueError:
                st.error('Please enter a number for the input field')
                break
            if user_input[key] == 0:
                # skip this loop
                continue
            else:
                st.write(key, user_input[key])
                # create a histogram for each feature
                # show the input value as a vertical line
                # show the histogram of the feature
                fig = px.histogram(featured_df.join(target_df), x=featured_df[key], color='NSP_Label', title=f'Frequency distribution of {key} grouped by NSP')
                fig.add_vline(x=user_input[key], line_dash="dash", line_color="red", annotation_text=f'Your input: {user_input[key]}')
                st.plotly_chart(fig, use_container_width=True)



def loaddata():
    # Fetch dataset
    try:
        cardiotocography = fetch_ucirepo(id=193) 

        # Save data to csv for later use in case the API is down
        cardiotocography.data.features.to_csv('data/featured_df.csv', index=False)
        cardiotocography.data.targets.to_csv('data/target_df.csv', index=False)
        
        # Data (as pandas dataframes) 
        featured_df = cardiotocography.data.features 
        target_df = cardiotocography.data.targets

    except:
        # Load data from csv
        featured_df = pd.read_csv('data/featured_df.csv')
        target_df = pd.read_csv('data/target_df.csv')
        
    # Convert NSP to categorical
    target_df['NSP_Label'] = target_df['NSP'].map({1: 'Normal', 2: 'Suspect', 3: 'Pathologic'})
        
    return featured_df, target_df

if __name__ == '__main__':
    featured_df, target_df = loaddata()
    main(featured_df, target_df)

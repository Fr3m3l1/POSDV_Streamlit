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
    col1, col2, col3 = st.columns(3)
    
    user_input['LB'] = col1.number_input('FHR baseline (beats per minute)', 100, 200, None, 1, placeholder="LB")
    user_input['AC'] = col2.number_input('# # of accelerations per second',  0.0, 0.02, None, 0.01, placeholder="AC")
    user_input['FM'] = col3.number_input('# # of fetal movements per second', 0., 0.6, None, 0.01, placeholder="FM")

    user_input['UC'] = col1.number_input('# # of uterine contractions per second', 0.0, 0.02, None, 0.01, placeholder="UC")
    user_input['DL'] = col2.number_input('# # of light decelerations per second', 0.0, 0.02, None, 0.01, placeholder="DL")
    user_input['DS'] = col3.number_input('# # of severe decelerations per second', 0.0, 0.002, None, 0.001, placeholder="DS")

    user_input['DP'] = col1.number_input('# # of prolongued decelerations per second', 0.0, 0.01, None, 0.001, placeholder="DP")
    user_input['ASTV'] = col2.number_input('percentage of time with abnormal short term variability', 0, 100, None, 1, placeholder="ASTV")
    user_input['MSTV'] = col3.number_input('mean value of short term variability', 0.0, 10.0, None, 0.1, placeholder="MSTV")

    user_input['ALTV'] = col1.number_input('percentage of time with abnormal long term variability', 0.0, 100.0, None, 0.1, placeholder="ALTV")
    user_input['MLTV'] = col2.number_input('mean value of long term variability', 0.0, 55.0, None, 0.1, placeholder="MLTV")
    user_input['Width'] = col3.number_input('width of FHR histogram', 0, 200, None, 1, placeholder="Width")

    user_input['Min'] = col1.number_input('minimum of FHR histogram', 50, 180, None, 1, placeholder="Min")
    user_input['Max'] = col2.number_input('maximum of FHR histogram', 100, 250, None, 1, placeholder="Max")
    user_input['Nmax'] = col3.number_input('# # of histogram peaks', 0, 20, None, 1, placeholder="Nmax")

    user_input['Nzeros'] = col1.number_input('# # of histogram zeros', 0, 15, None, 1, placeholder="Nzeros")
    user_input['Mode'] = col2.number_input('histogram mode', 60, 190, None, 1, placeholder="Mode")
    user_input['Mean'] = col3.number_input('histogram mean', 60, 200, None, 1, placeholder="Mean")

    # Swith for using the normalized data
    # If the switch is on, the data is normalized
    # If the switch is off, the data is not normalized
    # The default value is off
    normalize = st.checkbox('Normalize Data', False)

    if normalize:
        st.write("# Work in progress")

    

    # Create a button to submit the input data
    if st.button('Caluculate'):
        # Check if the input is a number
        for key in user_input:
            if user_input[key] == None:
                # skip this loop
                continue
            else:
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

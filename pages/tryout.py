import streamlit as st
import plotly.express as px

import functions.helpers as helpers


st.set_page_config(initial_sidebar_state="collapsed", page_title="CTG Tryout", page_icon=":heart:", layout="centered")

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

st.markdown("<div id='linkto_top'></div>", unsafe_allow_html=True) 

def main(featured_df, target_df):

    print("---- REFRESH ----")

    # Create back home
    st.link_button("Back to Home", "/")

    st.markdown("## Try your own Data")

    st.markdown("Enter your own data in the text fields below or select a random example with the button:")

    col1_button, col2_button, col3_button = st.columns(3, gap="small")

    sample_data = None

    # select example data with a button click
    if col1_button.button('Normal data'):
        example_data = featured_df[target_df['NSP_Label'] == 'Normal'].sample(1)

        sample_data = True
        target = "Normal"

    if col2_button.button('Suspect Data'):
        example_data = featured_df[target_df['NSP_Label'] == 'Suspect'].sample(1)

        sample_data = True
        target = "Suspect"

    if col3_button.button('Pathologic Data'):
        example_data = featured_df[target_df['NSP_Label'] == 'Pathologic'].sample(1)

        sample_data = True
        target = "Pathologic"

    if not sample_data:

        print("No sample data selected")

        # define the example data as an empty array for each column
        example_data = featured_df.sample(1).copy()
        for col in example_data.columns:
                    example_data[col] = helpers.load_session_data(col)

        sample_data = False
        target = None

    normalize = st.checkbox('Normalize Data', False)

    if normalize:
        change_yScale = True
    else:
        change_yScale = False

    # Create text input fields for user input data
    # The user can input their own data for the features
    # The input data is stored in a dictionary

    with st.form(key='my_form'):
        user_input = {}
            
        col1_1, col2_1, col3_1 = st.columns(3)
        
        user_input['LB'] = col1_1.number_input('FHR baseline (beats per minute)', 100, 200, example_data["LB"].values[0], 1, placeholder="LB")
        user_input['AC'] = col2_1.number_input('# # of accelerations per second',  0.0, 0.02, example_data["AC"].values[0], 0.01, placeholder="AC")
        user_input['FM'] = col3_1.number_input('# # of fetal movements per second', 0., 0.6, example_data["FM"].values[0], 0.01, placeholder="FM")

        col1_2, col2_2, col3_2 = st.columns(3)

        user_input['UC'] = col1_2.number_input('# # of uterine contractions per second', 0.0, 0.02, example_data["UC"].values[0], 0.01, placeholder="UC")
        user_input['DL'] = col2_2.number_input('# # of light decelerations per second', 0.0, 0.02, example_data["DL"].values[0], 0.01, placeholder="DL")
        user_input['DS'] = col3_2.number_input('# # of severe decelerations per second', 0.0, 0.002, example_data["DS"].values[0], 0.001, placeholder="DS")

        col1_3, col2_3, col3_3 = st.columns(3)

        user_input['DP'] = col1_3.number_input('# # of prolongued decelerations per second', 0.0, 0.01, example_data["DP"].values[0], 0.001, placeholder="DP")
        user_input['ASTV'] = col2_3.number_input('percentage of time with abnormal short term variability', 0, 100, example_data["ASTV"].values[0], 1, placeholder="ASTV")
        user_input['MSTV'] = col3_3.number_input('mean value of short term variability', 0.0, 10.0, example_data["MSTV"].values[0], 0.1, placeholder="MSTV")

        col1_4, col2_4, col3_4 = st.columns(3)

        user_input['ALTV'] = col1_4.number_input('percentage of time with abnormal long term variability', 0, 100, example_data["ALTV"].values[0], 1, placeholder="ALTV")
        user_input['MLTV'] = col2_4.number_input('mean value of long term variability', 0.0, 55.0, example_data["MLTV"].values[0], 0.1, placeholder="MLTV")
        user_input['Width'] = col3_4.number_input('width of FHR histogram', 0, 200, example_data["Width"].values[0], 1, placeholder="Width")

        col1_5, col2_5, col3_5 = st.columns(3)

        user_input['Min'] = col1_5.number_input('minimum of FHR histogram', 50, 180, example_data["Min"].values[0], 1, placeholder="Min")
        user_input['Max'] = col2_5.number_input('maximum of FHR histogram', 100, 250, example_data["Max"].values[0], 1, placeholder="Max")
        user_input['Nmax'] = col3_5.number_input('# # of histogram peaks', 0, 20, example_data["Nmax"].values[0], 1, placeholder="Nmax")

        col1_6, col2_6, col3_6 = st.columns(3)

        user_input['Nzeros'] = col1_6.number_input('# # of histogram zeros', 0, 15, example_data["Nzeros"].values[0], 1, placeholder="Nzeros")
        user_input['Mode'] = col2_6.number_input('histogram mode', 60, 190, example_data["Mode"].values[0], 1, placeholder="Mode")
        user_input['Mean'] = col3_6.number_input('histogram mean', 60, 200, example_data["Mean"].values[0], 1, placeholder="Mean")

        col1_7, col2_7, col3_7 = st.columns(3)

        user_input['Median'] = col1_7.number_input('histogram median', 60, 200, example_data["Median"].values[0], 1, placeholder="Median")
        user_input['Variance'] = col2_7.number_input('histogram variance', 0, 100, example_data["Variance"].values[0], 1, placeholder="Variance")
        user_input['Tendency'] = col3_7.number_input('histogram tendency', -1, 1, example_data["Tendency"].values[0], 1, placeholder="Tendency")

        submitted = st.form_submit_button('Calculate')

    # Save the user input data to a csv file
    for key in user_input:
        helpers.save_session_data(key, user_input[key])

    # Swith for using the normalized data
    # If the switch is on, the data is normalized
    # If the switch is off, the data is not normalized
    # The default value is off


    if not sample_data or target is None:

        print(sample_data, target)
        # do calculation with the model
        print("Calculating with the model")

    # Show the result of the calculation
    st.markdown('### Result')
    st.markdown(f'The result of the calculation is: {target}')
    

    # Create a button to submit the input data
    if submitted or sample_data is not False:
        # Check if the input is a number
        for key in user_input:
            if user_input[key] == None:
                # skip this loop
                continue
            else:
                # create a histogram for each feature
                # show the input value as a vertical line
                fig = px.histogram(featured_df.join(target_df), x=featured_df[key], color='NSP_Label', title=f'{key} histogram', labels={'NSP_Label': 'NSP Label', 'count': 'Count', 'x': key}, color_discrete_map={'Normal': 'green', 'Suspect': 'blue', 'Pathologic': 'red'}, facet_row='NSP_Label', facet_row_spacing=0.05, category_orders={'NSP_Label': ['Normal', 'Suspect', 'Pathologic']})
                fig.add_vline(x=user_input[key], line_dash="dash", line_color="red", annotation_text=f'Your input: {user_input[key]}')
                fig.update_layout(barmode='overlay')
                fig.update_traces(opacity=1)

                # Change facet row labels
                #fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
                fig.for_each_annotation(lambda a: a.update(text=""))

                
                # Remove y-axis labels for the first and third plot
                fig.update_layout(yaxis_title="", yaxis3_title="")


                if change_yScale:
                    fig.update_yaxes(matches=None)

                st.plotly_chart(fig, use_container_width=True)
    
                st.markdown("<a href='#linkto_top'>⬆️ Top</a>", unsafe_allow_html=True)

if __name__ == '__main__':
    featured_df, target_df = helpers.loaddata()
    main(featured_df, target_df)

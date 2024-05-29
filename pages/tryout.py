import streamlit as st
import plotly.express as px
import random

import functions.helpers as helpers

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

    st.markdown("Enter your own data in the text fields below or select one example with the button:")

    col1_button, col2_button, col3_button = st.columns(3)

    # select example data with a button click
    if col1_button.button('Select Normal Data'):
        # select random normal data
        random_int = random.randint(0, len(target_df[target_df['NSP_Label'] == 'Normal'])-1)

        example_data = featured_df[target_df['NSP_Label'] == 'Normal'].sample(1)
        # show the example data in the text fields
        st.write(example_data)

        sample_data = True
        target = "Normal"
    elif col2_button.button('Select Suspect Data'):
        # select random suspect data
        random_int = random.randint(0, len(target_df[target_df['NSP_Label'] == 'Suspect'])-1)

        example_data = featured_df[target_df['NSP_Label'] == 'Suspect'].sample(1)
        # show the example data in the text fields
        st.write(example_data)

        sample_data = True
        target = "Suspect"
    elif col3_button.button('Select Pathologic Data'):
        # select random pathologic data
        random_int = random.randint(0, len(target_df[target_df['NSP_Label'] == 'Pathologic'])-1)

        example_data = featured_df[target_df['NSP_Label'] == 'Pathologic'].sample(1)
        # show the example data in the text fields
        st.write(example_data)

        sample_data = True
        target = "Pathologic"
    else:
        # define the example data as an empty array for each column
        example_data = featured_df.sample(1)
        example_data['LB'] = None
        example_data['AC'] = None
        example_data['FM'] = None
        example_data['UC'] = None
        example_data['DL'] = None
        example_data['DS'] = None
        example_data['DP'] = None
        example_data['ASTV'] = None
        example_data['MSTV'] = None
        example_data['ALTV'] = None
        example_data['MLTV'] = None
        example_data['Width'] = None
        example_data['Min'] = None
        example_data['Max'] = None
        example_data['Nmax'] = None
        example_data['Nzeros'] = None
        example_data['Mode'] = None
        example_data['Mean'] = None

        sample_data = False

    # Create text input fields for user input data
    # The user can input their own data for the features
    # The input data is stored in a dictionary
    user_input = {}
    col1, col2, col3 = st.columns(3)

    print(example_data["LB"].values[0])
    
    user_input['LB'] = col1.number_input('FHR baseline (beats per minute)', 100, 200, example_data["LB"].values[0], 1, placeholder="LB")
    user_input['AC'] = col2.number_input('# # of accelerations per second',  0.0, 0.02, example_data["AC"].values[0], 0.01, placeholder="AC")
    user_input['FM'] = col3.number_input('# # of fetal movements per second', 0., 0.6, example_data["FM"].values[0], 0.01, placeholder="FM")

    user_input['UC'] = col1.number_input('# # of uterine contractions per second', 0.0, 0.02, example_data["UC"].values[0], 0.01, placeholder="UC")
    user_input['DL'] = col2.number_input('# # of light decelerations per second', 0.0, 0.02, example_data["DL"].values[0], 0.01, placeholder="DL")
    user_input['DS'] = col3.number_input('# # of severe decelerations per second', 0.0, 0.002, example_data["DS"].values[0], 0.001, placeholder="DS")

    user_input['DP'] = col1.number_input('# # of prolongued decelerations per second', 0.0, 0.01, example_data["DP"].values[0], 0.001, placeholder="DP")
    user_input['ASTV'] = col2.number_input('percentage of time with abnormal short term variability', 0, 100, example_data["ASTV"].values[0], 1, placeholder="ASTV")
    user_input['MSTV'] = col3.number_input('mean value of short term variability', 0.0, 10.0, example_data["MSTV"].values[0], 0.1, placeholder="MSTV")

    user_input['ALTV'] = col1.number_input('percentage of time with abnormal long term variability', 0, 100, example_data["ALTV"].values[0], 1, placeholder="ALTV")
    user_input['MLTV'] = col2.number_input('mean value of long term variability', 0.0, 55.0, example_data["MLTV"].values[0], 0.1, placeholder="MLTV")
    user_input['Width'] = col3.number_input('width of FHR histogram', 0, 200, example_data["Width"].values[0], 1, placeholder="Width")

    user_input['Min'] = col1.number_input('minimum of FHR histogram', 50, 180, example_data["Min"].values[0], 1, placeholder="Min")
    user_input['Max'] = col2.number_input('maximum of FHR histogram', 100, 250, example_data["Max"].values[0], 1, placeholder="Max")
    user_input['Nmax'] = col3.number_input('# # of histogram peaks', 0, 20, example_data["Nmax"].values[0], 1, placeholder="Nmax")

    user_input['Nzeros'] = col1.number_input('# # of histogram zeros', 0, 15, example_data["Nzeros"].values[0], 1, placeholder="Nzeros")
    user_input['Mode'] = col2.number_input('histogram mode', 60, 190, example_data["Mode"].values[0], 1, placeholder="Mode")
    user_input['Mean'] = col3.number_input('histogram mean', 60, 200, example_data["Mean"].values[0], 1, placeholder="Mean")

    # Swith for using the normalized data
    # If the switch is on, the data is normalized
    # If the switch is off, the data is not normalized
    # The default value is off
    normalize = st.checkbox('Normalize Data', False)

    if normalize:
        change_yScale = True
    else:
        change_yScale = False

    if not sample_data or target is None:
        # do calculation with the model
        target = None

    # Show the result of the calculation
    st.markdown('### Result')
    st.markdown(f'The result of the calculation is: {target}')
    

    # Create a button to submit the input data
    if st.button('Caluculate') or sample_data is not False:
        # Check if the input is a number
        for key in user_input:
            if user_input[key] == None:
                # skip this loop
                continue
            else:
                # create a histogram for each feature
                # show the input value as a vertical line
                fig = px.histogram(featured_df.join(target_df), x=featured_df[key], color='NSP_Label', title=f'{key} histogram', labels={'NSP_Label': 'NSP Label', 'count': 'Count', 'x': key}, color_discrete_map={'Normal': 'green', 'Suspect': 'blue', 'Pathologic': 'red'}, facet_row='NSP_Label', facet_row_spacing=0.05)
                fig.add_vline(x=user_input[key], line_dash="dash", line_color="red", annotation_text=f'Your input: {user_input[key]}')
                fig.update_layout(barmode='overlay')
                fig.update_traces(opacity=1)

                # Change facet row labels
                #fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
                fig.for_each_annotation(lambda a: a.update(text=""))

                if change_yScale:
                    fig.update_yaxes(matches=None)

                st.plotly_chart(fig, use_container_width=True)


if __name__ == '__main__':
    featured_df, target_df = helpers.loaddata()
    main(featured_df, target_df)

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ucimlrepo import fetch_ucirepo 
import plotly.express as px
import plotly.graph_objects as go
from sklearn.decomposition import PCA
import seaborn as sns
import os

# Set the page configuration
st.set_page_config(initial_sidebar_state="collapsed")

# Hide sidebar and its pages
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

def main(featured_df, target_df):
    st.title('Cardiotocography Dashboard')

    # Show intro text
    st.markdown('This dashboard provides an overview of a Cardiotocography dataset. The dataset contains features of fetal heart rate (FHR) and uterine contractions (UC) and the target variable Normal, Suspect, Pathologic (NSP). Feel free to explore the dataset by selecting a categorical variable from the dropdown menu below.')

    st.markdown('### Cardiotocography dataset overview:')
    # Number of features
    # Number of samples
    # Number of missing values

    # Display overview on one row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f'Number of features: {featured_df.shape[1]}')
    with col2:
        st.write(f'Number of samples: {featured_df.shape[0]}')
    with col3:
        st.write(f'Number of missing values: {featured_df.isnull().sum().sum()}')

    # Make divider line
    st.write('---')

    # Create an array for the categorical variables with description
    categorical_variables = ["",
                            'LB: FHR baseline (beats per minute)',
                             'AC: # of accelerations per second',
                             'FM: # of fetal movements per second',
                             'UC: # of uterine contractions per second',
                             'DL: # of light decelerations per second',
                             'DS: # of severe decelerations per second',
                             'DP: # of prolongued decelerations per second',
                             'ASTV: percentage of time with abnormal short term variability',
                             'MSTV: mean value of short term variability',
                             'ALTV: percentage of time with abnormal long term variability',
                             'MLTV: mean value of long term variability',
                             'Width: width of FHR histogram',
                             'Min: minimum of FHR histogram',
                             'Max: maximum of FHR histogram',
                             'Nmax: # of histogram peaks',
                             'Nzeros: # of histogram zeros',
                             'Mode: histogram mode',
                             'Mean: histogram mean',
                             'Median: histogram median',
                             'Variance: histogram variance',
                             'Tendency: histogram tendency']
        
    # Introduction and explanation of PCA
    st.markdown('### PCA - Explained Variance per Measurement:')
    st.markdown('Principal Component Analysis (PCA) is a mathematical reduction technique that allows to illuminate the most important measurements in the big datasets. The graph below shows the explained variance for each measurement of a patient. The higher the explained variance, the more important that measurement could be for further treatment.')

    # Perform PCA
    X = featured_df
    pca = PCA(n_components=len(X.columns))
    X_pca = pca.fit_transform(X)

    # Sorting the explained variance ratios and corresponding feature names
    explained_variances = pca.explained_variance_ratio_
    features = X.columns
    indices = np.argsort(explained_variances)[::-1]  # Get the indices that would sort the array
    sorted_variances = explained_variances[indices]
    sorted_features = features[indices]

    # Create bar plot for the sorted explained variances
    fig, ax = plt.subplots()
    bars = ax.barh(sorted_features, sorted_variances, color='green')
    ax.set_xlabel('Explained Variance')
    ax.set_title('PCA - Explained Variance per Feature')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # Add text labels to the bars
    for bar in bars:
        width = bar.get_width()
        label_x_pos = width + 0.02  # adjust this value for label positioning
        ax.text(label_x_pos, bar.get_y() + bar.get_height() / 2, f'{width:.2f}', va='center')

    # Inverting y-axis to show the largest bar on top
    ax.invert_yaxis()

    # Display the plot
    st.pyplot(fig)

    # Make divider line
    st.write('---')
    st.markdown('### Overview of all measurments dirstribution:')

    all_features = featured_df.select_dtypes(include=[np.number]).columns.tolist()

    col1_overview, col2_overview = st.columns(2)

    # Show all features button and reset button
    show_all_features_overview = col1_overview.button('Show all features', key='show_all_features', help='Click to show all features')
    if show_all_features_overview:
        selected_features_overview = st.multiselect("Choose features:", all_features, default=all_features)
    if col2_overview.button('Reset selection', key='reset_selection', help='Click to reset the selection'):
        selected_features_overview = st.multiselect("Choose features:", all_features, default=all_features[:5])
    elif not show_all_features_overview:
        selected_features_overview = st.multiselect("Choose features:", all_features, default=all_features[:5])

        
    


    # Correlation heatmap
    if len(selected_features_overview) > 1:
        # Density plots for all features
        n_cols = 2
        cols = st.columns(n_cols)
        for i, column in enumerate(featured_df[selected_features_overview].columns):
            description = next((desc for desc in categorical_variables if desc.startswith(column)), column)
            with cols[i % n_cols]:
                fig, ax = plt.subplots()
                sns.kdeplot(data=featured_df, x=column, hue=target_df['NSP_Label'], fill=True,
                            palette={'Normal': 'green', 'Suspect': 'blue', 'Pathologic': 'red'})
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.set_title(f'Distribution of {description}')
                st.pyplot(fig)

    #### Heatmap
    ## Dropdown for correlation heatmap
    show_correlation = st.selectbox('Are you interested to learn more about correlation in measurements?', ('Maybe later', 'Yes'))

    if show_correlation == 'Yes':
        
        selected_features_corr = st.multiselect("Choose features:", all_features, default=all_features[:5], key='selected_features_corr')

        # Correlation heatmap
        if len(selected_features_corr) > 1:
            st.subheader('Correlation Heatmap of Selected Features')
            corr_matrix = featured_df[selected_features_corr].corr()
            corr_matrix = corr_matrix.round(2)
            heatmap_fig = px.imshow(corr_matrix, text_auto=True, labels=dict(x="Feature", y="Feature", color="Correlation"), aspect="auto", color_continuous_scale='RdBu_r')
            st.plotly_chart(heatmap_fig, use_container_width=True)
            

            st.markdown("""
            **💡 How to use this correlation matrix?**  
            This correlation matrix displays the relationships between various measurements in a patient's CTG data. 
            Darker shades signify stronger correlations, while lighter shades indicate weaker or no correlations. 
            Look for strong positive or negative correlations, as they may indicate significant information. 
            1 means positive correlation, -1 represents negative correlation.
                """)

        
    # show button to localhost:8501/tryout
    st.link_button('Try your own data', 'http://localhost:8501/tryout')

def loaddata():
    data_dir = 'data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Directory '{data_dir}' created.")
    else:
        print(f"Directory '{data_dir}' already exists.")

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

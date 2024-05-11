import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ucimlrepo import fetch_ucirepo 
import plotly.express as px
import plotly.graph_objects as go
from sklearn.decomposition import PCA

def main(featured_df, target_df):
    st.title('Cardiotocography Dashboard')

    # show intro text
    st.markdown('This dashboard provides an overview of a Cardiotocography dataset. The dataset contains features of fetal heart rate (FHR) and uterine contractions (UC) and the target variable Normal, Suspect, Pathologic (NSP). Feel free to explore the dataset by selecting a categorical variable from the dropdown menu below.')

    st.markdown('### Cardiotocography dataset overview:')
    # Number of features
    # Number of samples
    # Number of missing values

    # display overview on one row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f'Number of features: {featured_df.shape[1]}')
    with col2:
        st.write(f'Number of samples: {featured_df.shape[0]}')
    with col3:
        st.write(f'Number of missing values: {featured_df.isnull().sum().sum()}')

    # Make devider line
    st.write('---')

    # Create a array for the categorical variables with description
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
    
    
    # Red Reset button 
    if st.button('Reset selection', key='reset_selection', help='Click to reset the selection'):
        categorical_variable_selection = st.selectbox('Select a categorical variable:', categorical_variables, index=0)
        return
    
    # PCA
    # show explenation text for PCA
    st.markdown('### PCA - Explained Variance per Feature:')
    st.markdown('Principal Component Analysis (PCA) is a dimensionality reduction technique that is often used to reduce the number of features in a dataset. The plot below shows the explained variance for each feature in the dataset. The higher the explained variance, the more important the feature is for the dataset.')
    
    # Annahme: cardiotocography.data.features ist deine Datenquelle
    X = featured_df 

    # PCA mit Anzahl der Komponenten entsprechend der Anzahl der Merkmale
    pca = PCA(n_components=len(X.columns))
    X_pca = pca.fit_transform(X)

    # Bar-Plot der erklärten Varianz für jede Komponente
    fig, ax = plt.subplots()
    bars = ax.barh(range(len(pca.explained_variance_ratio_)), pca.explained_variance_ratio_, color='green')
    ax.set_ylabel('Feature')
    ax.set_xlabel('Explained variance')
    ax.set_title('PCA - Explained Variance per Feature')

    # Setze Merkmalsnamen als y-Achsenbeschriftungen
    feature_names = X.columns
    ax.set_yticks(range(len(pca.explained_variance_ratio_)))
    ax.set_yticklabels(feature_names)

    # Füge Beschriftungen zu den Balken hinzu
    for bar in bars:
        width = bar.get_width()
        label_x_pos = width + 0.02  # Passe diesen Wert für die richtige Positionierung der Beschriftungen an
        ax.text(label_x_pos, bar.get_y() + bar.get_height()/2, f'{width:.0%}',  # Runde auf ganze Zahl und zeige als Prozent
                va='center', ha='left')
        
    for loc in ['top', 'right']:
        ax.spines[loc].set_visible(False)

    st.pyplot(fig)


    # select a categorical variable
    categorical_variable_selection = st.selectbox('Select a categorical variable for exploration:', categorical_variables, placeholder='Select a categorical variable', index=0)

    # Check if the user has selected a variable
    if categorical_variable_selection == '':
        return
    
    categorical_variable_selection = categorical_variable_selection.split(':')[0]

    # Frequency distribution as bar chart grouped by NSP
    fig = px.histogram(featured_df.join(target_df), x=categorical_variable_selection, color='NSP_Label', title=f'Frequency distribution of {categorical_variable_selection} grouped by NSP')
    st.plotly_chart(fig, use_container_width=True)

    # this is an alternative plot
    fig = go.Figure()
    for nsp in target_df['NSP_Label'].unique():
        fig.add_trace(go.Histogram(x=featured_df[target_df['NSP_Label'] == nsp][categorical_variable_selection], name=nsp))
    fig.update_layout(title=f'Frequency distribution of {categorical_variable_selection} grouped by NSP', barmode='overlay')
    st.plotly_chart(fig, use_container_width=True)






def loaddata():
    # fetch dataset 
    cardiotocography = fetch_ucirepo(id=193) 
    
    # data (as pandas dataframes) 
    featured_df = cardiotocography.data.features 
    target_df = cardiotocography.data.targets

    # convert NSP to categorical
    target_df['NSP_Label'] = target_df['NSP'].map({1: 'Normal', 2: 'Suspect', 3: 'Pathologic'})
    
    return featured_df, target_df

if __name__ == '__main__':
    featured_df, target_df = loaddata()
    main(featured_df, target_df)
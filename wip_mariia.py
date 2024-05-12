import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
from ucimlrepo import fetch_ucirepo 


def main():
    st.title('Cardiotocography Dashboard')

    # Introduction for workers
    st.write("""Welcome to the Cardiotocography Dashboard! This tool helps you analyze CTG data to identify the health status of fetuses. 
    Below, you'll find various visualizations and analyses to help you understand the relationships between different features and outcomes.""")

    # fetch dataset 
    cardiotocography = fetch_ucirepo(id=193) 
    # data (as pandas dataframes) 
    X = cardiotocography.data.features 
    y = cardiotocography.data.targets 
    print(cardiotocography.description)
    # Overview of data structure
    st.write('Dataset Description:', cardiotocography.description)

    # Categorize variables
    categorical_variables = []
    numerical_variables = []
    for row_nr, variable_type in enumerate(cardiotocography.variables['role']):
        if variable_type == 'Feature':
            numerical_variables.append(cardiotocography.variables['name'][row_nr])
        else:
            categorical_variables.append(cardiotocography.variables['name'][row_nr])

    # Dataset overview
    st.write('Cardiotocography dataset overview:')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f'Number of features: {X.shape[1]}')
    with col2:
        st.write(f'Number of samples: {X.shape[0]}')
    with col3:
        st.write(f'Number of missing values: {X.isnull().sum().sum()}')

    # Select a categorical variable for analysis
    categorical_variable = st.selectbox('Select a categorical variable:', categorical_variables)
################################################
# Feature correlation in classes 
################################################
    #col1, col2 = st.columns(2)
    X['NSP'] = y['NSP'] 
    
    ## Dropdown for correlation heatmap
    show_correlation = st.selectbox('Are you intereseted to learn more about correlation in measurements?', ( 'May be later', 'Yes' ))

    if show_correlation == 'Yes':
        # Section: Correlation Heatmap
        st.subheader('Correlation Heatmap of Features')
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(X.corr(), annot=True, cmap='coolwarm', fmt=".2f")
        st.pyplot(fig)

        st.markdown("""
**💡 How to use this correlation matrix?**  
This correlation matrix displays the relationships between various measurements in a patient's CTG data. 
Darker shades signify stronger correlations, while lighter shades indicate weaker or no correlations. 
Look for strong positive or negative correlations, as they may indicate redundant or significant information. 
1 means positive correlation, -1 represents negative correlation.
    """)

    # Section: Feature Analysis for NSP Class 3
    st.subheader('Feature Analysis for pathologic class (NSP = 3)')
    st.markdown("""
**❓ How should I interpret these metrics?**  
These density plots represent the feature importance for different fetal health conditions: normal (1), suspect (2), and pathologic (3). 
By visually analyzing these plots, you can recognize significant differences in feature distributions across various health statuses. 
Areas where the density curves differ notably, especially for pathologic conditions which are highlighted under a grey curve, highlight features that play a crucial role in distinguishing between different health conditions.
    """)

    # Creating two columns for density plots
    cols = st.columns(2)
    for index, feature in enumerate(numerical_variables):
        with cols[index % 2]:
            fig, ax = plt.subplots()
            sns.kdeplot(data=X, x=feature, hue='NSP', fill=True)
            ax.set_title(feature)
            st.pyplot(fig)

if __name__ == '__main__':
    main()
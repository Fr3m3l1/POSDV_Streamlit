import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ucimlrepo import fetch_ucirepo 
import plotly.express as px
from sklearn.decomposition import PCA


def main():
    st.title('Cardiotocography Dashboard')

    # fetch dataset 
    cardiotocography = fetch_ucirepo(id=193) 
    
    # data (as pandas dataframes) 
    X = cardiotocography.data.features 
    y = cardiotocography.data.targets 

    print(cardiotocography.description)

    print(X)
    print(y)

    print(cardiotocography.metadata)

    categorical_variables = []
    numerical_variables = []

    print(cardiotocography.variables)
    # for each row in the variable 
    for row_nr, variable_type in enumerate(cardiotocography.variables['role']):
        if variable_type == 'Feature':
            numerical_variables.append(cardiotocography.variables['name'][row_nr])
        else:
            categorical_variables.append(cardiotocography.variables['name'][row_nr])



    # display dataset overview
    st.write('Cardiotocography dataset overview:')
    # Number of features
    # Number of samples
    # Number of missing values

    # display overview on one row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f'Number of features: {X.shape[1]}')
    with col2:
        st.write(f'Number of samples: {X.shape[0]}')
    with col3:
        st.write(f'Number of missing values: {X.isnull().sum().sum()}')

    # Univariate analysis for a user-selectable categorical variable
        # Frequency distribution as bar chart
        # Pie chart

    # select a categorical variable
    categorical_variable = st.selectbox('Select a categorical variable:', categorical_variables)
    # frequency distribution as bar chart
    fig, ax = plt.subplots()
    y[categorical_variable].value_counts().plot(kind='bar', ax=ax)
    ax.set_xlabel(categorical_variable)
    ax.set_ylabel('Count')
    ax.set_title(f'Frequency distribution of {categorical_variable}')
    st.pyplot(fig)

    # for interactive plot create a plotly figure object
    plt_fig = px.bar(y[categorical_variable].value_counts(), x=y[categorical_variable].value_counts().index, y=y[categorical_variable].value_counts().values)
    # display the plotly figure object
    st.plotly_chart(plt_fig, use_container_width=True)

    # pie chart
    fig, ax = plt.subplots()
    y[categorical_variable].value_counts().plot(kind='pie', ax=ax)
    ax.set_ylabel('Count')
    ax.set_title(f'Pie chart of {categorical_variable}')
    st.pyplot(fig)

    # Grouped box plot for the interaction between a user-selectable categorical variable and a selectable numerical variable
    # select a numerical variable
    numerical_variable = st.selectbox('Select a numerical variable:', numerical_variables)

    # combine the X and y dataframes
    X = X.join(y)
    
    # grouped box plot
    fig, ax = plt.subplots()
    X.boxplot(column=numerical_variable, by=categorical_variable, ax=ax)
    ax.set_xlabel(categorical_variable)
    ax.set_ylabel(numerical_variable)
    ax.set_title(f'Grouped box plot of {numerical_variable} by {categorical_variable}')
    st.pyplot(fig)

    
   
    
    # Perform PCA


    # Annahme: cardiotocography.data.features ist deine Datenquelle
    X = cardiotocography.data.features 

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

    plt.show()


    st.pyplot(fig)


    





if __name__ == '__main__':
    main()
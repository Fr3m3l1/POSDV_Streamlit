import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.decomposition import PCA
import seaborn as sns

import functions.helpers as helpers

# Set the page configuration
st.set_page_config(initial_sidebar_state="collapsed", page_title='Cardiotocography Dashboard', page_icon='🩺')

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
    st.markdown('This dashboard provides an overview of a [Cardiotocography dataset](https://archive.ics.uci.edu/dataset/193/cardiotocography). The dataset contains features of fetal heart rate (FHR) and uterine contractions (UC) and the target variable Normal, Suspect, Pathologic (NSP). Feel free to explore the dataset by selecting a categorical variable from the dropdown menu below.')

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
                             'ASTV: % of time with abnormal short term variability',
                             'MSTV: mean value of short term variability',
                             'ALTV: % of time with abnormal long term variability',
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

    # Description of all features
    st.markdown('### Description of all features:')

    all_features = featured_df.select_dtypes(include=[np.number]).columns.tolist()
    col1_desc, col2_desc = st.columns(2)

    # Show all features button and reset button for the feature descriptions
    show_all_features_desc = col1_desc.button('Show all features (desc)', key='show_all_features_desc', help='Click to show all features')
    if show_all_features_desc:
        selected_features_desc = st.multiselect("Choose features (desc):", all_features, default=all_features, key='multiselect_all_features_desc')
    if col2_desc.button('Reset selection (desc)', key='reset_selection_desc', help='Click to reset the selection'):
        selected_features_desc = st.multiselect("Choose features (desc):", all_features, default=all_features[:5], key='multiselect_reset_desc')
    elif not show_all_features_desc:
        selected_features_desc = st.multiselect("Choose features (desc):", all_features, default=all_features[:5], key='multiselect_default_desc')

    # Descriptions and sources for the features
    feature_descriptions = {
        'LB': 'Baseline value: The average heart rate during a 10-minute window, excluding accelerations and decelerations.',
        'AC': 'Accelerations: Temporary increases in FHR of at least 15 beats per minute above the baseline, lasting for at least 15 seconds.',
        'FM': 'Fetal movements: The number of times the fetus moves during the monitoring period.',
        'UC': 'Uterine contractions: The number of contractions during the monitoring period, used to correlate with FHR patterns.',
        'ASTV': 'Abnormal Short-Term Variability: The percentage of time with abnormal short term variability, indicating potential distress.',
        'MSTV': 'Mean Short-Term Variability: The average beat-to-beat variability of the fetal heart rate.',
        'ALTV': 'Abnormal Long-Term Variability: The percentage of time with abnormal long term variability, indicating potential distress.',
        'MLTV': 'Mean Long-Term Variability: The average variability over longer periods.',
        'DL': 'Light Decelerations: Temporary decreases in FHR, indicating potential distress but usually less severe.',
        'DS': 'Severe Decelerations: More significant decreases in FHR, indicating a higher level of distress.',
        'DP': 'Prolonged Decelerations: Extended periods of decreased FHR, indicating potential sustained distress.',
        'DR': 'Rebound Decelerations: Decreases in FHR that are followed by an increase in FHR, indicating potential sustained distress.',
        'Width' : 'The width of the FHR histogram represents the range of heart rate values observed over the monitoring period. It provides an indication of the variability in fetal heart rate, which is crucial for assessing fetal well-being.',
        'Min': 'The minimum (low frequency) of the FHR histogram represents the lowest recorded fetal heart rate during the monitoring period. It helps in identifying instances of significant bradycardia, which could indicate fetal distress.',
        'Max': 'The maximum (high frequency) of the FHR histogram represents the highest recorded fetal heart rate during the monitoring period. This can highlight episodes of fetal tachycardia, which may be associated with fetal or maternal conditions.',
        'NMax': 'number of histogram peaks',
        'Nzeros': 'number of histogram zeros',
        'Mode': 'The mode of the histogram is the most frequently occurring fetal heart rate value during the monitoring period. It represents the central tendency of the fetal heart rate distribution.',
        'Mean': 'mean of the histogram',
        'Median': 'median of the histogram',
        'Variance': 'The variance of the histogram measures the dispersion of the fetal heart rate values around the mean. High variance indicates greater variability in the fetal heart rate, which can be a sign of fetal well-being or distress.',
        'Tendency': 'Histogram tendency indicates the skewness of the fetal heart rate distribution. A value of -1 indicates left asymmetry, 0 indicates symmetry, and 1 indicates right asymmetry. This feature helps in understanding the distribution pattern of the heart rate.',


    }

    sources = {
        'LB': 'Source: [Bioengineering Journal](https://www.mdpi.com/2306-5354/11/4/368#B30-bioengineering-11-00368)',
        'AC': 'Source: [Frontiers in Bioengineering](https://www.frontiersin.org/articles/10.3389/fbioe.2022.887549/full)',
        'FM': 'Source: [Example no source jet](https://www.example.com)',
        'UC': 'Source: [Bioengineering Journal](https://www.mdpi.com/2306-5354/11/4/368#B30-bioengineering-11-00368)',
        'ASTV': 'Source: [Frontiers in Bioengineering](https://www.frontiersin.org/articles/10.3389/fbioe.2022.887549/full)',
        'MSTV': 'Source: [Example no source jet](https://www.example.com)',
        'ALTV': 'Source: [Bioengineering Journal](https://www.mdpi.com/2306-5354/11/4/368#B30-bioengineering-11-00368)',
        'MLTV': 'Source: [Frontiers in Bioengineering](https://www.frontiersin.org/articles/10.3389/fbioe.2022.887549/full)',
        'DL': 'Source: [Example no source jet](https://www.example.com)',
        'DS': 'Source: [Bioengineering Journal](https://www.mdpi.com/2306-5354/11/4/368#B30-bioengineering-11-00368)',
        'DP': 'Source: [Frontiers in Bioengineering](https://www.frontiersin.org/articles/10.3389/fbioe.2022.887549/full)',
        'DR': 'Source: [Example no source jet](https://www.example.com)',
        'Width' : 'Source: [Journal of Advanced Analytics in Healthcare Management](https://research.tensorgate.org/index.php/JAAHM/article/view/38/44)',
        'Min': 'Source: [Journal of Advanced Analytics in Healthcare Management](https://research.tensorgate.org/index.php/JAAHM/article/view/38/44)',
        'Max': 'Source: [Journal of Advanced Analytics in Healthcare Management](https://research.tensorgate.org/index.php/JAAHM/article/view/38/44)',
        'NMax': 'Source: [Research Article](https://www.researchgate.net/publication/357179891_Investigating_the_interpretability_of_fetal_status_assessment_using_antepartum_cardiotocographic_records)',
        'Nzeros': 'Source: [Research Article](https://www.researchgate.net/publication/357179891_Investigating_the_interpretability_of_fetal_status_assessment_using_antepartum_cardiotocographic_records )',
        'Mode': 'Source: [Journal of Advanced Analytics in Healthcare Management](https://research.tensorgate.org/index.php/JAAHM/article/view/38/44)',
        'Mean': 'Source: [Example no source jet](https://www.example.com)',
        'Median': 'Source: [Example no source jet](https://www.example.com)',
        'Variance': 'Source: [Journal of Advanced Analytics in Healthcare Management](https://research.tensorgate.org/index.php/JAAHM/article/view/38/44)',
        'Tendency': 'Source: [Journal of Advanced Analytics in Healthcare Management](https://research.tensorgate.org/index.php/JAAHM/article/view/38/44)',
    }

    st.markdown('#### Detailed Descriptions of Selected Features')
    for feature in selected_features_desc:
        description = feature_descriptions.get(feature, 'No description available.')
        source = sources.get(feature, 'No source available.')
        st.markdown(f"**{feature}**: {description}\n{source}")

    # Make divider line
    st.write('---')

    st.markdown('### Overview of all measurements distribution:')

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

    # Intermittent red lines for normal reference values
    red_lines = {
        'LB': [110, 150],
        'AC': [0, 0.013],
        #'FM': [0.00139, 0.00417],
        'UC': [0, 0.0083],
        'DL': [0.00167, 0],
        #'DS': [0.00111, 0],
        #'DP': [0, 0.00056],
        'ASTV': [20, 58],
        'MSTV': [0.5, 2.5],
        'ALTV': [0, 13],
        'MLTV': [4, 17],
        'Width': [25, 140],
        #'Min': [50, 100],
        #'Max': [100, 200],
        #'Nmax': [0, 10],
        #'Nzeros': [0, 10],
        #'Mode': [100, 150],
        #'Mean': [100, 150],
        #'Median': [100, 150],
        #'Variance': [0, 100],
        #'Tendency': [-1, 1]
    }
    

    if len(selected_features_overview) > 1:
        # Density plot for selected features
        n_cols = 2
        n_rows = (len(selected_features_overview) + 1) // n_cols

        fig, axes = plt.subplots(n_rows, n_cols, figsize=(18, n_rows * 6), constrained_layout=True)

        # Letter size for the subplots
        for ax in axes.flatten():
            for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
                        ax.get_xticklabels() + ax.get_yticklabels()):
                item.set_fontsize(18)

        for i, column in enumerate(featured_df[selected_features_overview].columns):
            if n_rows == 1:
                ax = axes[i % n_cols]
            else:
                ax = axes[i // n_cols, i % n_cols]
            description = next((desc for desc in categorical_variables if desc.startswith(column)), column)
            sns.kdeplot(data=featured_df, x=column, hue=target_df['NSP_Label'], fill=True,
                        palette={'Normal': 'green', 'Suspect': 'blue', 'Pathologic': 'red'}, ax=ax)

            # Add intermittent red lines
            if column in red_lines:
                for line in red_lines[column]:
                    ax.axvline(line, color='red', linestyle='--', linewidth=1)
            
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.set_title(f'Distribution of {description}', fontsize=18, fontweight='bold')

            ax.get_legend().remove()

        # Add legend outside of the subplots
        if n_rows == 1:
            fig.legend(['Pathologic', 'Normal', 'Suspect'], loc='upper left', bbox_to_anchor=(0, 1.3), fontsize=18, title='NSP Label', title_fontsize='18')
        else:
            fig.legend(['Pathologic', 'Normal', 'Suspect'], loc='upper left', bbox_to_anchor=(0, 1.15 - (len(selected_features_overview)/2) *0.011), fontsize=18, title='NSP Label', title_fontsize='18')


        # Hide any unused subplots
        for j in range(i + 1, n_rows * n_cols):
            fig.delaxes(axes.flatten()[j])

        st.pyplot(fig)

    else:
        # Density plot for selected features
        fig, ax = plt.subplots(figsize=(12, 6))

        for column in selected_features_overview:
            description = next((desc for desc in categorical_variables if desc.startswith(column)), column)
            sns.kdeplot(data=featured_df, x=column, hue=target_df['NSP_Label'], fill=True,
                        palette={'Normal': 'green', 'Suspect': 'blue', 'Pathologic': 'red'}, ax=ax)

            # Add intermittent red lines
            if column in red_lines:
                for line in red_lines[column]:
                    ax.axvline(line, color='red', linestyle='--', linewidth=1)

            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.set_title(f'Distribution of {description}', fontsize=18, fontweight='bold')

        st.pyplot(fig)


    #### Heatmap
    ## Dropdown for correlation heatmap
    show_correlation = st.selectbox('Are you interested to learn more about correlation in measurements?', ('Maybe later', 'Yes'))

    if show_correlation == 'Yes':

        st.write('---')
        st.markdown('### Correlation Heatmap:')

        col1_corr, col2_corr = st.columns(2)

        # Show all features button and reset button
        show_all_features_corr = col1_corr.button('Show all features', key='show_all_features_corr', help='Click to show all features')

        if show_all_features_corr:
            selected_features_corr = st.multiselect("Choose features:", all_features, default=all_features, key='multiselect_all_features_corr')
        if col2_corr.button('Reset selection', key='reset_selection_corr', help='Click to reset the selection'):
            selected_features_corr = st.multiselect("Choose features:", all_features, default=all_features[:5], key='multiselect_reset_corr')
        elif not show_all_features_corr:
            selected_features_corr = st.multiselect("Choose features:", all_features, default=all_features[:5], key='multiselect_default_corr')

        # Correlation heatmap
        if len(selected_features_corr) > 1:
            st.markdown('#### Correlation Heatmap of Selected Measurements:')
            corr_matrix = featured_df[selected_features_corr].corr()
            corr_matrix = corr_matrix.round(2)
            heatmap_fig = px.imshow(corr_matrix, text_auto=True, labels=dict(x="Feature", y="Feature", color="Correlation"), aspect="auto", color_continuous_scale='RdBu_r', zmin=-1, zmax=1)
            st.plotly_chart(heatmap_fig, use_container_width=True)
            

            st.markdown("""
            **💡 How to use this correlation matrix?**  
            This correlationheatmap displays the relationships between various measurements in a patient's CTG data. 
            Darker shades of red signify stronger positive correlations, while lighter shades indicate weaker correlations. 
            Look for strong positive or negative correlations, as they may indicate significant information. 
            1 means positive correlation, -1 represents negative correlation, 0 indicates no correlation.
                """)

        
    # show button to localhost:8501/tryout
    st.link_button('Try your own data', '/tryout')

if __name__ == '__main__':
    featured_df, target_df = helpers.loaddata()
    main(featured_df, target_df)

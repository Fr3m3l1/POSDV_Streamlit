# explore_more.py
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.decomposition import PCA
from dashboard import loaddata, main

def explore_more(featured_df, target_df):
    st.title('Explore More - Detailed Feature Analysis')
    
    st.markdown("Select the features you want to analyze with PCA:")
    all_features = featured_df.select_dtypes(include=[np.number]).columns.tolist()
    selected_features = st.multiselect("Choose features:", all_features, default=all_features[:5])

    if selected_features:
        # Perform PCA on selected features
        X = featured_df[selected_features]
        pca = PCA(n_components=min(len(selected_features), 5))
        pca.fit(X)
        top_features = selected_features
        top_variances = pca.explained_variance_ratio_

        # Pie chart of PCA results
        pie_fig = px.pie(values=top_variances, names=top_features, title='PCA Feature Contribution')
        st.plotly_chart(pie_fig, use_container_width=True)

        st.markdown("### Feature Explanation")
        st.markdown("""
        The PCA chart above shows how much each selected feature contributes to the variance of the dataset. 
        This analysis helps identify the most significant features that could influence outcomes and provides 
        insights into the underlying structure of the data.
        """)

        # Correlation heatmap
        if len(selected_features) > 1:
            st.subheader('Correlation Heatmap of Selected Features')
            corr_matrix = featured_df[selected_features].corr()
            heatmap_fig = px.imshow(corr_matrix, text_auto=True, labels=dict(x="Feature", y="Feature", color="Correlation"), aspect="auto", color_continuous_scale='RdBu_r')
            st.plotly_chart(heatmap_fig, use_container_width=True)

        # Display explanations for the top PCA features
        top_indices = np.argsort(-top_variances)[:3]  # Get indices of top 3 features
        for index in top_indices:
            feature = top_features[index]
            st.markdown(f"#### {feature}")
            st.markdown(f"""
            **{feature}** is one of the key features because it explains a significant portion of the variability in the dataset.
            It can be particularly influential in predicting outcomes due to its high correlation with other important metrics (if applicable).
            """)

        # Further analysis based on user input
        if st.button('Further Analyze Top Feature'):
            top_feature = top_features[np.argmax(top_variances)]
            st.write(f"Further analysis on {top_feature}:")
            # Implement specific analysis, e.g., distribution, trends over time, etc.
            dist_fig = px.histogram(featured_df, x=top_feature, title=f'Distribution of {top_feature}')
            st.plotly_chart(dist_fig, use_container_width=True)

if __name__ == '__main__':
    featured_df, target_df = loaddata()
    # Use Streamlit's multipage app handling to decide which function to run
    app_mode = st.sidebar.selectbox('Choose the app mode:',
                                    ['Main Dashboard', 'Explore More'])
    if app_mode == 'Main Dashboard':
        main(featured_df, target_df)
    elif app_mode == 'Explore More':
        explore_more(featured_df, target_df)



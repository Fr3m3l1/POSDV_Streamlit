import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import functions.helpers as helpers

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

def train_model(featured_df, target_df):
    # Prepare the data for model building
    X = featured_df
    y = target_df['NSP_Label']

    # Map string labels to numeric labels
    label_mapping = {'Normal': 0, 'Suspect': 1, 'Pathologic': 2}
    y = y.map(label_mapping)

    # Ensure target values match the expected classes
    unique_classes = y.unique()
    if not all(cls in [0, 1, 2] for cls in unique_classes):
        st.error(f"Unexpected class labels found: {unique_classes}")
        return None, [], None, None

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the Random Forest Classifier with class weights
    clf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')

    # Train the model
    clf.fit(X_train, y_train)

    # Make predictions
    y_pred = clf.predict(X_test)

    return clf, X.columns.tolist(), y_test, y_pred

def main():
    st.title('Cardiotocography Dashboard')

    # Load the data
    featured_df, target_df = helpers.loaddata()

    # Train the model
    clf, feature_columns, y_test, y_pred = train_model(featured_df, target_df)

    if clf is None:
        return

    # Show intro text
    st.markdown('This dashboard provides an overview of a [Cardiotocography dataset](https://archive.ics.uci.edu/dataset/193/cardiotocography). The dataset contains features of fetal heart rate (FHR) and uterine contractions (UC) and the target variable Normal, Suspect, Pathologic (NSP). Feel free to explore the dataset by selecting a categorical variable from the dropdown menu below.')

    st.markdown('### Cardiotocography dataset overview:')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f'Number of features: {featured_df.shape[1]}')
    with col2:
        st.write(f'Number of samples: {featured_df.shape[0]}')
    with col3:
        st.write(f'Number of missing values: {featured_df.isnull().sum().sum()}')

    st.write('---')

    # Feature selection filter
    st.markdown('### Select Features to Input Values')
    selected_features = st.multiselect('Choose features:', feature_columns)

    if 'input_data' not in st.session_state:
        st.session_state.input_data = {}

    if selected_features:
        st.markdown('### Enter Values for Selected Features')
        input_data = {}
        for column in selected_features:
            min_value = float(featured_df[column].min())
            max_value = float(featured_df[column].max())
            if column not in st.session_state.input_data:
                st.session_state.input_data[column] = min_value
            input_data[column] = st.number_input(
                f'Enter value for {column} (Range: {min_value} - {max_value})', 
                value=st.session_state.input_data[column],
                min_value=min_value,
                max_value=max_value,
                key=column
            )

        # Create a DataFrame with all required features
        input_data_df = pd.DataFrame([input_data])
        for col in feature_columns:
            if col not in input_data_df.columns:
                input_data_df[col] = featured_df[col].mean()  # Fill missing features with the mean value

        # Ensure the input DataFrame has the same column order as the training DataFrame
        input_data_df = input_data_df[feature_columns]

        # Mapping of numeric labels to class names
        class_names = {0: 'Normal', 1: 'Suspect', 2: 'Pathologic'}

        if st.button('Predict'):
            prediction = clf.predict(input_data_df)
            prediction_proba = clf.predict_proba(input_data_df)

            if prediction[0] in class_names:
                predicted_class_name = class_names[prediction[0]]
                st.write(f'Predicted Class: {predicted_class_name}')
                st.write(f'Probability of Normal class: {prediction_proba[0][0]}')
                st.write(f'Probability of Suspect class: {prediction_proba[0][1]}')
                st.write(f'Probability of Pathologic class: {prediction_proba[0][2]}')
            else:
                st.error(f"Unexpected prediction value: {prediction[0]}")

            # Add a toggle list to show the evaluation of the model
            with st.expander("Learn more about the prediction model"):
                st.write(f"Model Accuracy: {accuracy_score(y_test, y_pred)}")
                st.write("Classification Report:")
                st.text(classification_report(y_test, y_pred))

if __name__ == '__main__':
    main()

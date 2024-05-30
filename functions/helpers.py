import os
import json
import pandas as pd
from ucimlrepo import fetch_ucirepo 

pd.options.mode.chained_assignment = None  # Suppress the warning

def loaddata():
    """Load the Cardiotocography dataset from the UCI repository."""

    data_dir = 'data'
    os.makedirs(data_dir, exist_ok=True)

    try:
        cardiotocography = fetch_ucirepo(id=193) 

        featured_df = cardiotocography.data.features  # Get the original DataFrames
        target_df = cardiotocography.data.targets

        featured_df.to_csv('data/featured_df.csv', index=False)
        target_df.to_csv('data/target_df.csv', index=False)

    except:
        featured_df = pd.read_csv('data/featured_df.csv')
        target_df = pd.read_csv('data/target_df.csv')

    target_df.loc[:, 'NSP_Label'] = target_df['NSP'].map({1: 'Normal', 2: 'Suspect', 3: 'Pathologic'})

    return featured_df, target_df
def save_session_data(variable, value):
    """
    Save the session data to a csv file. Dont overwrite the existing data.
    """
    try:
        # open the json file and read the data as a dictionary
        with open('data/session_data.json', 'r') as session_file:
            session_data_list = json.load(session_file)
    except:
        # if the file does not exist, create a new dictionary
        session_data_list = {}

    # add the new data to the dictionary
    session_data_list[variable] = value
        
    # save dictionary to the json file
    with open('data/session_data.json', 'w') as session_file:
        json.dump(session_data_list, session_file)


def load_session_data(variable):
    """
    Load the session data from the csv file.
    """
    
    with open('data/session_data.json', 'r') as session_file:
        session_data_list = json.load(session_file)
        value = session_data_list.get(variable, None)


    return value
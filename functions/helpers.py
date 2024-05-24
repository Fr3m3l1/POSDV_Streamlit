import os
import pandas as pd
from ucimlrepo import fetch_ucirepo 

def loaddata():
    """
    Load the Cardiotocography dataset from the UCI repository.
    """

    # Create data directory if it does not exist
    data_dir = 'data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)
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
import pandas as pd
from utils import save_to_json
from twitterAPI.auth import build_client
from twitterAPI.users import fetch_followees_by_usernames

def get_followees(seed_users, credentials_filepath, user_fields=None,
                  save_data=False, data_filepath='raw.json'):
    '''Connects to the Twitter API and returns followees of users
    from the provided seed list of Twitter usernames.

    Parameters
    ----------
    seed_users : list
        List of seed Twitter usernames as comma-separated strings (without "@")
    credentials_filepath : str
        Path to file with Twitter credentials (consumer_key, consumer_secret, tokens)
    user_fields : list, optional
        Enables to collect further user fields in addition to default ones (id, name, username)
        https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/user
    save_data : bool, optional
        If activated, saves raw data in json format
    data_filepath : str, optional
        Filepath to store raw data if save_data is activated

    Returns
    -------
    dict
        a dictionary with seed usernames as keys and the correspoding lists of followees as values
    '''
    # Connect to Twitter API with provided credentials
    tweepy_client, user_auth = build_client(credentials_filepath)
    # Collect followees from Twitter with Tweepy Client
    data = fetch_followees_by_usernames(seed_users, client=tweepy_client,
                                        user_fields=user_fields, user_auth=user_auth)
    if save_data:
        save_to_json(data, filepath=data_filepath)
    return data

def preprocess_data(data):
    '''Transforms data from dict format {username: [list of followed users]}
       into a pandas dataframe with 'username' and 'following' columns.
    '''
    # Transform data from dict to pandas dataframe format
    df = pd.DataFrame.from_dict(data, orient='index').reset_index()
    df = pd.melt(df, id_vars='index', value_name='following')[['index', 'following']]
    # Rename columns
    df.columns = ['seed_username', 'following']
    df.dropna(subset=['following'], inplace=True)
    # Split column with dict into separate columns
    df = pd.concat([
        df.drop(['following'], axis=1),
        df['following'].apply(pd.Series, dtype=str)], axis=1)
    # If present, split public_metrics from dict to separate columns
    if "public_metrics" in df.columns:
        df = pd.concat([
            df.drop(['public_metrics'], axis=1),
            df['public_metrics'].apply(eval).apply(pd.Series, dtype="Int64")], axis=1)
    df.sort_values('seed_username', inplace=True)
    return df

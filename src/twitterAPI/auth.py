import os
from dotenv import load_dotenv
import tweepy

def read_credentials(filepath):
    '''Reads Twitter credentials from the specified file.'''
    load_dotenv(filepath)
    res = {
        'bearer_token': os.getenv('bearer_token'),
        'consumer_key': os.getenv('consumer_key'),
        'consumer_secret': os.getenv('consumer_secret'),
        'access_token': os.getenv('access_token'),
        'access_token_secret': os.getenv('access_token_secret'),
    }
    return res

def init_client(bearer_token=None, consumer_key=None, consumer_secret=None,
                access_token=None, access_token_secret=None):
    '''Connects to Twitter API with provided credentials.
       Supports both App-only and User-context authentification depending on provided credentials:
       https://developer.twitter.com/en/docs/authentication/overview
    '''
    # If credentials for user context authentificaton are provided, set user_auth to True
    user_auth = bool(access_token and access_token_secret and consumer_key and consumer_secret)
    if (bearer_token is None) and (user_auth is False):
        raise TypeError('''
        You need to provide either bearer_token for Application-only authentication, or
        consumer_key, consumer_secret, access_token and access_token_secret for User Context authentication.
        ''')
    client = tweepy.Client(
        bearer_token=bearer_token,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
        wait_on_rate_limit=True
        )
    return client, user_auth

def build_client(credentials_filepath):
    '''Reads credentials from the given file and connects to the Twitter API.
       Returns tweepy client.
    '''
    credentials = read_credentials(credentials_filepath)
    return init_client(**credentials)

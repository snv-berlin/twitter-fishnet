import os
import pandas as pd
from data import get_followees, preprocess_data

# Provide directory to store all data
DATA_DIR = "../data/"
# Provide filepath to Twitter API credentials
AUTH_PATH = "../config/.env"
# Define user_fields to collect additional info on followees
USER_FIELDS = ["description", "public_metrics", "verified"]

# Import original (seed) usernames as list
usernames = pd.read_csv(os.path.join(DATA_DIR, "usernames.csv")).username.to_list()

# Collect raw data from Twitter
data = get_followees(seed_users=usernames, credentials_filepath=AUTH_PATH, user_fields=USER_FIELDS,
    save_data=True, data_filepath=os.path.join(DATA_DIR, "raw.json"))
# Preprocess raw data
df = preprocess_data(data)

# Count how many accounts from the seed list follow each followee and sort in descending order
df['followed_count'] = df.groupby('username').seed_username.transform('count')
df.sort_values(['followed_count', 'username'], ascending=[False, True], inplace=True)
df.drop("seed_username", axis=1, inplace=True)
df.drop_duplicates(subset=['username'], inplace=True)

# Save resulting dataframe as CSV
df.to_csv(os.path.join(DATA_DIR, "results.csv"), index=False, encoding='utf-8-sig', sep=';')

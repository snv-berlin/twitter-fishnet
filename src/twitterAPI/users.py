import tweepy

USERS_LIMIT = 100
FOLLOWING_LIMIT = 1000

def fetch_followees_by_usernames(usernames, client, user_fields=None, user_auth=False):
    '''Collects users followed by users from the provided list of usernames using Tweepy client.

    Parameters
    ----------
    usernames : list
        List of Twitter usernames (without "@") to collect the users they follow
    client : tweepy.Client
        Twitter API client
    user_fields : list, optional
        Enables to add additional user fields to collect to default ones (id, name, username)
        https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/user
    user_auth : bool
        Whether or not to use OAuth 1.0a User Context to authenticate.

    Returns
    -------
    dict
        a dictionary with seed usernames as keys and the correspoding lists of followees as values
    '''
    # Collect Twitter IDs for given usernames (can only access followed users via user ID)
    user_ids = fetch_user_ids(usernames, client, user_auth = user_auth)
    # Return resulting dict using dict generator
    return {username : fetch_followees_by_id(user_id, client, user_fields=user_fields)
            for username, user_id in user_ids.items()}

def fetch_user_ids(usernames, client, user_auth=False):
    '''Collects Twitter user IDs of the given usernames using the Tweepy client.

    Parameters
    ----------
    usernames : list
        List of Twitter usernames (without "@")
    client : tweepy.Client
        Twitter API client
    user_auth : bool
        Whether or not to use OAuth 1.0a User Context to authenticate.

    Returns
    -------
    dict
        a dictionary with usernames as keys and corresponding user IDs as values
    '''
    # Initialize dict to store results
    users = {}
    # Loop through max allowed batches (Twitter limit)
    for i in range(0, len(usernames), USERS_LIMIT):
        batch = usernames[i:i+USERS_LIMIT]
        collected_users = client.get_users(usernames=batch, user_auth=user_auth).data
        users.update({user.username: user.id for user in collected_users})
    # Check that all usernames were identified
    if len(usernames) > len(users):
        print(f'''{len(users)} user IDs out of {len(usernames)} usernames found.
            The following usernames not identified: {set(usernames) - set(users)}''')
    else:
        print(f"All {len(usernames)} user IDs collected.")
    return users

def fetch_followees_by_id(user_id, client, user_fields=None, user_auth=False):
    '''Collects Twitter users followed by a user with the provided Twitter user ID.

    Parameters
    ----------
    user_id : int
        Twitter user id
    client : tweepy.Client
        Twitter API client
    user_fields : list, optional
        Enables to add additional user fields to collect to default ones (id, name, username)
        https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/user
    user_auth : bool
        Whether or not to use OAuth 1.0a User Context to authenticate.

    Returns
    -------
    list
        list of dictionaries for every user followed by a Twitter user ID
    '''
    followees = []
    # Generate user attributes based on user_fields
    user_attrs = ['username', 'name'] + user_fields
    # Paginate through followees (one response is limited by max allowed number of followees)
    paginator = tweepy.Paginator(client.get_users_following, id=user_id,  user_auth=user_auth,
                                 user_fields=user_fields, max_results=FOLLOWING_LIMIT)
    for response in paginator:
        followees.extend([{attr : getattr(user, attr) for attr in user_attrs}
                          for user in response.data])
    return followees

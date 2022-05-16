# Twitter Fishnet
Which experts am I missing for my panel? Which organisations are working on AI ethics in Germany? Who should I invite to our next workshop on cyber security? Whom should I send our expert survey? 

This method helps to expand the circle of relevant actors for questions like these using Tweepy - a Python library for accessing the Twitter API. It involves the following three steps:  

1. Start with a sample (~10-20) of known relevant Twitter accounts ("seed") 
2. Collect all accounts followed by the seed using the Twitter API. Sort these by indegree centrality and output the result list. This means accounts that are followed by many seed accounts (and thus probably relevant) are higher up the list. 
3. Manually look over the list and sort the results (thus the name "fishnet" :smile:) to identify relevant accounts for your question. 

__Notes:__ 
- Consider GDPR given the involvement of personal data. 
- You can sort the list in step 2 by the relative indegree centrality by dividing through the number of followers each account has. This improves the results in some cases and tends to highlight smaller accounts. 
- Highlighting or filtering users with relevant keywords in their Twitter bio (like "journalist" or "cyber") can ease the manual sorting in step 3.
- Instead of a followee network, you can alter the code to obtain a retweets or mentions network. 
- You can iterate step 1 by modifying the seed based on the initial results to refine your outcome. 

## Instructions for deploying 🔨
_The instructions below were tested on Ubuntu 20.04.1._
### 0. Clone Git repository
### 1. Activate virtual environment
If you don't have `virtualenv`, run: 
```bash
pip install virtualenv
```
Navigate to the project folder and set up `virtualenv` for that project by running:
```bash
cd twitter-fischnetz/
virtualenv venv
```
These commands create a `venv/` directory in your project. You need to activate it first though (in every terminal instance where you are working on your project):
```bash
source venv/bin/activate
```
Install packages with pip from the *requirements* file:
```bash
pip install -r requirements.txt
```
If you find you need to install another package, run `pip freeze > requirements.txt` and commit the changes to version control. You can also use [`pipreqs`](https://pypi.org/project/pipreqs/) package for this.

To leave the virtual environment run:
```bash
deactivate
```
### 2. Provide Twitter credentials
To run the project you need to have a Twitter developer account. There you will find the necessary credentials for accessing Twitter API. Put them in the `config/.env` file (added to `.gitignore`, so you need to create the directory!) like that:
```bash
bearer_token = "1234"
consumer_key = "1234"
consumer_secret = "1234"
access_token = "1234"
access_token_secret = "1234"
```
__Note:__ if you only need the App authentification (no user involved, just the publicly accessible data) you can only provide the `bearer_token`. For the User context authentificaiton it is required to provide all of the `consumer_key`, `consumer_secret`, `access_token` and `access_token_secret`. See [Tweepy documentation](https://developer.twitter.com/en/docs/authentication/overview) for more details. The user context authentification will switch automatically depending on the provided credentials. 

If there is an error in the credentials, you will get `tweepy.errors.Unauthorized: 401 Unauthorized`.

### 3. Run the code
Navigate to `src/` folder and run `main.py`.

Default arguments are as follows:
* `DATA_DIR = "../data/"` - directory to store resulting data in the _data_ folder in the project directory
* `AUTH_PATH = "../config/.env"` - filepath with credentials in the _config_ folder in the project directory
* `USER_FIELDS = ["description", "public_metrics", "verified"]` - [user fields](https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/user) to collect in addition to default ones
* seed list of usernames is accessed from the *username* column in `"../data/usernames.csv"`

# License
[MIT licence](https://github.com/snv-berlin/twitter-fishnet/blob/main/LICENSE). If you use the fishnet method, we appreciate a reference. :wink:

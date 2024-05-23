#geolocation intergration
import requests

def get_location(ip_address):
    url = f'http://ip-api.com/json/{ip_address}'
    response = requests.get(url)
    data = response.json()
    return data

# Example usage:
ip_address = '148.185.153.148'
location_data = get_location(ip_address)
print(location_data)

import tweepy

# Define your Twitter API credentials
consumer_key = 'your_consumer_key'
consumer_secret = 'your_consumer_secret'
access_token = 'your_access_token'
access_token_secret = 'your_access_token_secret'
# Authenticate with Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Search for mentions of your website content
mentions = api.search(q='your_website_keyword', count=10)

# Process and analyze the mentions
for mention in mentions:
    print(mention.text)
    print(mention.user.screen_name)
    print(mention.created_at)

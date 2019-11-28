# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 12:32:01 2019

@author: Dhiral
"""

#%%
import warnings
import requests
import numpy as np
from requests_oauthlib import OAuth1
import tweepy as tw
import pandas as pd
import os
from sklearn import tree

#%%   Your Account info
consumer_key = 'HYE8UXTCKR0B6pUFANnlMPsi5'
consumer_secret = '5Z3hn5SWhfChFPekmJDMOyjfdGTLjjOA4HbHpsJVBzwBZQi1Ef'
access_token = '918726623662301184-HZLSkCtTVU0EHm6P1ZVmkmjKl8aZvbT'
access_token_secret = 'WwN4JwSYtUH4bttxoFPHNq19m40FlSPjSOr4jUwRW0otI'


auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

oauth = OAuth1(consumer_key,
                client_secret=consumer_secret,
                resource_owner_key=access_token,
                resource_owner_secret=access_token_secret)

#%%

REQUIRED_FIELDS = ['id','id_str','screen_name','location','description','url',
                   'followers_count','friends_count', 'listed_count', 'created_at',
                   'favourites_count', 'verified','statuses_count','lang','status',
                   'default_profile','default_profile_image','has_extended_profile',
                   'name','bot']

def write_to_csv(responses):
    user_l = []
    for response in responses:
        final_fields = {}

        try:
            response_dict = response.json()[0]
        except AttributeError:
            response_dict = response
        final_fields['bot'] = 0
        final_fields['status'] = ''
    
        for key, value in response_dict.items():
            if key in REQUIRED_FIELDS:
                final_fields[key] = value
                #print(key)
        
        user_l.append(final_fields)

        user_df = pd.DataFrame(user_l)  
    #print(user_df)

    twitter_user_data = open(os.getcwd() + '/test.csv', 'w',encoding="utf-8")
    user_df[REQUIRED_FIELDS].to_csv(twitter_user_data,index=False)
    #print(twitter_user_data)
    twitter_user_data.close()
#%% Get all the details
def bottell(twitterid):
    uname = twitterid
    print(uname)
    #uname = "filipe_a_morais"
    user = api.get_user(uname)
    """print(user.name)
    print(user.friends_count)
    print(user.description)"""
    responses = []
    response = requests.get(url="https://api.twitter.com/1.1/users/lookup.json?screen_name="+str(uname), auth=oauth)
    if response.status_code == 200:
        responses.append(response)
    write_to_csv(responses)
    
    #%%
    
    
    train_data = pd.read_csv(os.getcwd() + '/kaggle_train.csv')
    
    bot_data = pd.read_csv(os.getcwd() + '/bots_data.csv',engine='python')
    nonbot_data = pd.read_csv(os.getcwd() + '/nonbots_data.csv',engine='python')
    test_data = pd.read_csv(os.getcwd() + '/test.csv')
    
    #%%
    
    train_attr = train_data[
      ['followers_count', 'friends_count', 'listedcount', 'favourites_count', 'statuses_count', 'verified']]
    train_label = train_data[['bot']]
    
    #%%
    
    bot_attr = bot_data[
      ['followers_count', 'friends_count', 'listedcount', 'favourites_count', 'statuses_count', 'verified']]
    bot_label = bot_data[['bot']]
    
    nonbot_attr = nonbot_data[
      ['followers_count', 'friends_count', 'listedcount', 'favourites_count', 'statuses_count', 'verified']]
    nonbot_label = nonbot_data[['bot']]
    
    test_attr = test_data[
      ['followers_count', 'friends_count', 'listed_count', 'favourites_count', 'statuses_count', 'verified']]
    test_label = test_data[['bot']]
    
    #%%
    
    clf = tree.DecisionTreeClassifier()
    
    X = train_attr.as_matrix()
    Y = train_label.as_matrix()
    clf = clf.fit(X, Y)
    
    #%%
    
    actual = np.array(test_label)
    predicted = clf.predict(test_attr)
    pred = np.array(predicted)
    
    if pred==1:
        print("Its a bot")
    else:
        print("Its not a bot")
        
    #%%
        
    warnings.filterwarnings('ignore')
    print(pred)
    return(pred)
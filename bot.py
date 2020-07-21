import json 
import pandas as pd
import requests
import tweepy
import time
import os
from os import environ
def get_content():
    url = "https://corona-api.com/timeline"
    headers = {
        "Content-Type":"application/json"
    }
    response = requests.request("GET", url,headers=headers)
    b=str(response.content)
    data=(b.split("b'")[1].split("[")[1].split("{")[1:3])
    count=data[0].replace("},","")
    url = "https://api.smartable.ai/coronavirus/news/global"
    headers = {
        "subscription-key":environ['smartable_aikey'],
        "location":"global"
    }
    response = requests.request("GET", url,headers=headers)
    df1=json.loads(response.text)
    url = "http://newsapi.org/v2/everything?from=2020-07-19&q=covid-19 vaccines&sortBy=popularity&apiKey="+environ['news_apikey']
    response = requests.request("GET", url)
    df=json.loads(response.text)
    top_news=[]
    for i in range(0,2):
        content=dict(df['articles'][i])
        top_news.append(['Source: '+content['source']['name'],'Published At: '+content['publishedAt'],content['title'],'For more Details visit: '+content['url']])
        top_news.append(['Source: '+df1['news'][i]['provider']['name'],'Published At :'+df1['news'][i]['publishedDateTime'],df1['news'][i]['title'],'For more Details visit: '+df1['news'][i]['webUrl']])
    return count,top_news
def authent_tweet(count,top_news):
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(environ['twitter_consumerkey'], 
        environ['twitter_consumertoken'])
    auth.set_access_token(environ['twitter_apikey'],environ['twitter_apitoken'])

    api = tweepy.API(auth, wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True)

    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")
        return 0
    count=count.replace('"','').replace(",",'\n').replace('is_in_progress:true','').replace(":",": ")
    for i in top_news:
        news=''
        news='\n'.join(k for k in i)
        api.update_status(news)
    api.update_status(count)
    return 1
def main():
    interval=60*60*12
    while True:
        count,top_news=get_content()
        authent_tweet(count,top_news)
        time.sleep(interval)
if __name__=='__main__':
    main()

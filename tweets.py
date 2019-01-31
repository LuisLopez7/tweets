# coding=utf-8
import got
import pandas as pd
import time
import json
import tweepy
from itertools import chain

username = ""
since = ""
until = ""

#Get tweet ids from the month to mine. Match the Query Search pattern.
tweetCriteria = got.manager.TweetCriteria().setQuerySearch("{}".format(username)).setSince(since).setUntil(until)
mentions= got.manager.TweetManager.getTweets(tweetCriteria)[1:100000]
contador_ids = 0
ids = []
for i in mentions:
    contador_ids = contador_ids + 1
    percentage = round(float(contador_ids) / float(len(mentions)) * 100, 2)
    print "{0:.2f}%".format(percentage)
    ids.extend([i.id])

#ids_no_duplicates = list(set(ids))

#Access keys for twitter API
consumer_key=""
consumer_secret=""
access_token=""
access_token_secret= ""
auth =  tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)



#Construct the Data Frame with neccesary information to mine.
tweets = []
contador = 0
for i in ids:
    try:
        x = api.get_status(i)
        contador = contador + 1
        percentage = round(float(contador) / float(len(ids)) * 100, 2)
        print "{0:.2f}%".format(percentage)
        print(x.created_at)
        temp = dict(Tweet_Id= x.id, Usuario_Nombre = x.author.name)
        temp.update(Usuario_Id = x.author.id)
        temp.update(Mensaje = x.text)
        temp.update(Favoritos = x.favorite_count)
        temp.update(Retweets = x.retweet_count)
        temp.update(Fecha = x.created_at)
        temp.update(En_Respuesta_A_Nombre = x.in_reply_to_screen_name)
        temp.update(En_Respuesta_A_Id = x.in_reply_to_user_id)
        temp.update(Tweet_id = i)
        tweets.append(temp)
    except tweepy.TweepError:
        next
    time.sleep(1)


Mentions = pd.DataFrame.from_dict(tweets)
Mentions.to_csv("{}_Mentions.csv".format(username),
        header=True, index=False, encoding="utf-8")

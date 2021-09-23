'''
@author: Souvik Das
Institute: University at Buffalo
'''
import re
import tweepy
import datetime
from datetime import timedelta
from dateutil.parser import parse
from random import randint


class Twitter:
    def __init__(self):
        self.auth = tweepy.OAuthHandler("IGWNiyjPK2LzqeuMLdAfEknbz", "R0leI2rWC80Yu2xbs9yemukk9eDuy8KLSyBfMa1zq0ySt8RrJ8")
        self.auth.set_access_token("1432781960951304192-5f6wPKBg2a6kYfcbi1BoiZy779p561", "9eOI0afRTcEcZVJ1hGDpUGLy0B0S4D4WLaGwqBMw9xEp4")
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    def _meet_basic_tweet_requirements(self):
        '''
        Add basic tweet requirements logic, like language, country, covid type etc.
        :return: boolean
        '''
        raise NotImplementedError
    def get_tweets_by_poi_screen_name(self, poi_screen_name):
        '''
        Use user_timeline api to fetch POI related tweets, some postprocessing may be required.
        :return: List
        '''
        tweets = []
        covid_tweets = []
        key_word_tweets_count = 0
        max_id = None
        reply_max_id = None
        while key_word_tweets_count < 51 or len(tweets) < 600:
            tweets_temp = self.api.user_timeline(screen_name=poi_screen_name,count=600,include_rts = False,tweet_mode = 'extended',max_id=max_id)
            max_id = tweets_temp[-1].id
            for tweet in tweets_temp:
                #print("Text : ",tweet.full_text)
                if 'COVID' in tweet.full_text.upper():
                    key_word_tweets_count +=1
                    covid_tweets.append(tweet)
            tweets.extend(tweets_temp)
            print("collected covid----------------------",key_word_tweets_count)
        print("Total tweets count -",len(tweets))
        results = []
        replies_result = []
        invalid =0
        covid_tweets = covid_tweets[0:10]
        for tweet in covid_tweets:
            ran = randint(8, 16)  
            reply_max_id = None
            replies_count = 0
            #while replies_count < 11:
            replies = self.get_replies("to:{}".format(tweet.user.screen_name) , tweet.id)
            
            replies_for_current_tweet = []
            for reply in replies:
                if reply.in_reply_to_status_id == tweet.id:
                    replies_for_current_tweet.append(reply)
                    replies_count +=1
                else :
                    invalid +=1
            replies_result.extend(replies_for_current_tweet)
            print("replies - ",len(replies)," related -",len(replies_for_current_tweet))
                #if len(replies) > 0:
                #    reply_max_id = replies[-1].id
            if len(replies_result) > 600:
                break
                
        tweets.extend(replies_result)
        print("Replies count : ",len(replies_result))
        return tweets
        #raise NotImplementedError

    def get_tweets_by_lang_and_keyword(self,keyword):
        '''
        Use search api to fetch keywords and language related tweets, use tweepy Cursor.
        :return: List
        '''
        tweets = []
        max_id = None
        while len(tweets) < 300:
            
            tweets_temp = self.api.search(q=keyword,count=200,include_rts = False,tweet_mode = 'extended',max_id=max_id)
            print("1------------",len(tweets_temp))
            max_id = tweets_temp[-1].id
            tweets.extend(tweets_temp)

        results = []
        replies_result = []
        invalid = 0
        tweet_count = 0
        max_id = None

        
        return tweets
        #raise NotImplementedError

    def get_replies(self,query,since_id):
        '''
        Get replies for a particular tweet_id, use max_id and since_id.
        For more info: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/guides/working-with-timelines
        :return: List
        '''
        #print(query)
        replies = self.api.search(q = query, since_id=since_id,count =500)
        #for reply in replies:
        #    print(reply,"reply-------------------------------------------------")
        return replies
        #raise NotImplementedError

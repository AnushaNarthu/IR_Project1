'''
@author: Souvik Das
Institute: University at Buffalo
'''
import re
import tweepy
import datetime
from datetime import timedelta
from dateutil.parser import parse


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

    def get_tweets_by_poi_screen_name(self, poi_screenname,cnt):
        '''
        Use user_timeline api to fetch POI related tweets, some postprocessing may be required.
        :return: List
        '''
        #max_tweets=150
        c = 0
        d = 0
        oldest_id = None
        tweets_data = []
        while d < 801 :
            tweets = self.api.user_timeline(id =poi_screenname, count =100, max_id = oldest_id,tweet_mode='extended',)
            #print(len(tweets))
            for tweet in tweets:
                single_tweet = {}
                d = d+1
                
                

                single_tweet["id"] = str(tweet.id)
                single_tweet["verified"] = tweet.user.verified
                single_tweet["poi_name"] = tweet.user.screen_name
                single_tweet["poi_id"] = tweet.user.id
                if tweet.lang == "en":
                    single_tweet["country"] = "USA"
                elif tweet.lang  == "hi":
                    single_tweet["country"] =  "INDIA"
                else:
                    single_tweet["country"] = "MEXICO"
                single_tweet["tweet_text"] = tweet.full_text
                single_tweet["tweet_lang"] = tweet.lang


                x = tweet.entities
                y = x['hashtags']
                count_hashtags = len(y)
                all_hashtags = []
                if count_hashtags>0:
                    for hashtag in y:
                        hash_text = hashtag['text']
                        all_hashtags.append(hash_text)
                    single_tweet["hashtags"] = all_hashtags
                #mentions
                result_mention = []
                mentions = x['user_mentions']
                if len(mentions)>0:
                    for mention in mentions:
                        result_mention.append(mention['screen_name'])
                    single_tweet["mentions"] = result_mention
                
                
                ####
                #urls
                result_url = []
                urls = x['urls']
                if len(urls)>0:
                    for url in urls:
                        result_url.append(url['url'])
                    single_tweet["urls"] = result_url
                    
                
                
                ####
                date_str = parse(str(tweet.created_at))
                time_obj = date_str.replace(second=0, microsecond=0, minute=0, hour=date_str.hour) + timedelta(
                hours=date_str.minute // 30)
                date_str = datetime.datetime.strftime(time_obj, '%Y-%m-%dT%H:%M:%SZ')

                #single_tweet["tweet_date"]= status.created_at.strftime("%y-%m-%dT%H:%M:%SZ")
                #single_tweet["tweet_date"]= str(status.created_at)
                single_tweet["tweet_date"] = date_str
                tweets_data.append(single_tweet)

                if re.search("COVID", tweet.full_text):
                    c =c+1                   

                tweetid =tweet.id
            oldest_id = tweetid

        print("covid",c)
        return tweets_data
       
     #  raise NotImplementedError

    def get_tweets_by_lang_and_keyword(self,key_count,key_name,key_lang):
        '''
        Use search api to fetch keywords and language related tweets, use tweepy Cursor.
        :return: List
        '''

        tweets_data = []
        
    
        for status in tweepy.Cursor(self.api.search,q = key_name, lang = key_lang).items(300):
            #print(status)
            #status_dict = dict(vars(status))
            #keys = status_dict.keys()
            #for k in keys:
                #print(k)
            #    single_tweet[k] = status_dict[k]
            #user_dict = dict(vars(status_dict['user']))
            
            single_tweet = {}
            single_tweet["id"] = str(status.id)
            single_tweet["verified"] = status.user.verified
            if key_lang == "en":
                single_tweet["country"] = "USA"
            elif key_lang == "hi":
                single_tweet["country"] =  "INDIA"
            else:
                single_tweet["country"] = "MEXICO"
            single_tweet["tweet_text"] = status.text
            single_tweet["tweet_lang"] = key_lang

            
            
            x = status.entities
            y = x['hashtags']
            count_hashtags = len(y)
            all_hashtags = []
            if count_hashtags>0:
                for hashtag in y:
                    hash_text = hashtag['text']
                    all_hashtags.append(hash_text)

            single_tweet["hashtags"] = all_hashtags
            
            
            #mentions
            result_mention = []
            mentions = x['user_mentions']
            if len(mentions)>0:
                for mention in mentions:
                    result_mention.append(mention['screen_name'])
                single_tweet["mentions"] = result_mention
                
                
            ####
            #urls
            result_url = []
            urls = x['urls']
            if len(urls)>0:
                for url in urls:
                    result_url.append(url['url'])
                single_tweet["urls"] = result_url
                    
                
                
                ####
            
            
            date_str = parse(str(status.created_at))
            time_obj = date_str.replace(second=0, microsecond=0, minute=0, hour=date_str.hour) + timedelta(
            hours=date_str.minute // 30)
            date_str = datetime.datetime.strftime(time_obj, '%Y-%m-%dT%H:%M:%SZ')

            #single_tweet["tweet_date"]= status.created_at.strftime("%y-%m-%dT%H:%M:%SZ")
            #single_tweet["tweet_date"]= str(status.created_at)
            single_tweet["tweet_date"] = date_str
            tweets_data.append(single_tweet)


        return tweets_data
            

        
        #print(tweets_data)
        #raise NotImplementedError
        
  
    def get_replies(self, query, max_id ):
        '''
        Get replies for a particular tweet_id, use max_id and since_id.
        For more info: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/guides/working-with-timelines
        :return: List
        '''
        replies = self.api.search(q= query, since_id =max_id, count =1000)
        return replies
        raise NotImplementedError

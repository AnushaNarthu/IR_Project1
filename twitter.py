'''
@author: Souvik Das
Institute: University at Buffalo
'''

import tweepy
import re


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

    def get_tweets_by_poi_screen_name(self,screen,cnt):
        '''
        Use user_timeline api to fetch POI related tweets, some postprocessing may be required.
        :return: List
        '''
        #user_timeline = self.api.user_timeline(screen_name= screen, count = cnt)
        """
        tweets_data = []
        search = "COVID"
        for status in tweepy.Cursor(self.api.search,q = search,screen_name = screen).items(5):
            print(status.user.screen_name)
            print(status.text)

        """
        return
        #raise NotImplementedError

    def get_tweets_by_lang_and_keyword(self,key_count,key_name,key_lang):
        '''
        Use search api to fetch keywords and language related tweets, use tweepy Cursor.
        :return: List
        '''

        tweets_data = []
        #key_name = "टीकाकरण"
        #key_lang = "hi"
    
        for status in tweepy.Cursor(self.api.search,q = key_name, lang = key_lang).items(100):
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
            
            date_str = parse(str(status.created_at))
            time_obj = date_str.replace(second=0, microsecond=0, minute=0, hour=date_str.hour) + timedelta(
            hours=date_str.minute // 30)
            date_str = datetime.datetime.strftime(time_obj, '%Y-%m-%d %H:%M:%S')

            #single_tweet["tweet_date"]= status.created_at.strftime("%y-%m-%dT%H:%M:%SZ")
            #single_tweet["tweet_date"]= str(status.created_at)
            single_tweet["tweet_date"] = date_str
            tweets_data.append(single_tweet)


        return tweets_data
            

        
        #print(tweets_data)
        #raise NotImplementedError

    def get_replies(self):
        '''
        Get replies for a particular tweet_id, use max_id and since_id.
        For more info: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/guides/working-with-timelines
        :return: List
        '''
        


        raise NotImplementedError

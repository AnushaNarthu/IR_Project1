'''
@author: Souvik Das
Institute: University at Buffalo
'''

import tweepy


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

    def get_tweets_by_poi_screen_name(self, poi_screenname):
        '''
        Use user_timeline api to fetch POI related tweets, some postprocessing may be required.
        :return: List
        '''
        #max_tweets=150
        c = 0
        oldest_id = None
        covid_tweets=[]
        while c <50 :
            tweets = self.api.user_timeline(id =poi_screenname, count =500, max_id = oldest_id,tweet_mode='extended',)
            #print(len(tweets))
            for tweet in tweets:
                if re.search("COVID", tweet.full_text):
                    c =c+1
                    covid_tweets.append(tweet)
                tweetid =tweet.id
            oldest_id = tweetid
        print("covid",c)

        results=[]
        tweet_replies =[]
        for tweet in tweets:
            reply_max_id = tweet.id
            replies = self.get_replies("to:{}".format(poi_screenname), reply_max_id)
            replies_for_tweet=[]
            for reply in replies :
                if reply.in_reply_to_status_id == tweet.id:
                    replies_for_tweet.append(reply)
            tweet_replies.extend(replies_for_tweet)
            #reply_max_id = replies[-1].id
            replies.append(tweet)
        results.extend(tweet_replies)
        print( "replies count ", len(tweet_replies))
        for tweet in tweepy.Cursor(self.api.search,q='to:'+screenname, result_type='recent', timeout=999999).items(1000):
            if hasattr(tweet, 'in_reply_to_status_id_str'):
                if (tweet.in_reply_to_status_id_str==tweet.id):
                    replies.append(tweet)
        return results
        raise NotImplementedError


    def get_tweets_by_lang_and_keyword(self, name):
        '''
        Use search api to fetch keywords and language related tweets, use tweepy Cursor.
        :return: List
        '''
        max_tweets=200
        #text_query = 'carona virus'
        tweets_keyword = self.api.search(q=name,tweet_mode='extended', count= max_tweets)

        results =[]
        replies_result=[]
        invalid =0
        tweet_count =0
        max_id =None
        for tweet in tweets_keyword:
            tweet_count =+1
            replies = self.get_replies("to:{}".format(tweet.user.screen_name)+ "filter:replies", None, tweet._json['id'])
            replies_for_current_tweet =[ ]
            for reply in replies:
                if reply.reply.in_reply_to_status_id == tweet.id :
                    replies_for_current_tweet.append(reply)
                else :
                    invalid +=1
            replies_result.extend(replies_for_current_tweet)
            results.append(tweet)
        print(tweet_count, "tweet_count")
        results.extend(replies_result)
        print( len(replies_result))
        return results
        raise NotImplementedError

    def get_replies(self, query, max_id ):
        '''
        Get replies for a particular tweet_id, use max_id and since_id.
        For more info: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/guides/working-with-timelines
        :return: List
        '''
        replies = self.api.search(q= query, since_id =max_id, count =1000)
        return replies
        raise NotImplementedError

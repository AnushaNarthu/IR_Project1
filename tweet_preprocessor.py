import demoji, re, datetime
import preprocessor


# demoji.download_codes()


class TWPreprocessor:
    @classmethod
    def preprocess(cls, tweet, poi, tweet_type):
        '''
        Do tweet pre-processing before indexing, make sure all the field data types are in the format as asked in the project doc.
        :param tweet:
        :return: dict
        '''
        clean_text = '';emojis = [];lng=''
        text = ''
        poisList = ["JoeBiden","KamalaHarris","CDCgov","GOPLeader","LeaderMcConnell","narendramodi","RahulGandhi","MoHFW_INDIA","ShashiTharoor","ArvindKejriwal"]
        if tweet._json.get('text'):
            text = tweet._json.get('text')
        elif tweet._json.get('full_text'):
            text = tweet._json.get('full_text')


        if text != '':
            clean_text, emojis= _text_cleaner(text)
            key_lang = tweet.lang
            if key_lang == "en":
                lng = 'tweet_en'
                #tweet["text_en"] = tt
            elif key_lang == "hi":
                lng = 'tweet_hi'
                #tweet["text_hi"] =  tt
            else:
                lng = 'tweet_es'
                #tweet["text_es"] = tt
        if tweet_type == 'poi':
            #print("N ",tweet.user.screen_name, "-", tweet.user.id)
            data = {
                    'poi_name': tweet.user.screen_name,
                    'poi_id': tweet.user.id,
                    'verified': tweet.user.verified,
                    'country': poi['country'],
                    'id' : tweet.id,
                    'tweet_text': text,
                    lng : clean_text,
                    'tweet_lang': tweet.lang,
                    'hashtags': _get_entities(tweet,type='hashtags'),
                    'mentions': _get_entities(tweet,type='mentions'),
                    'tweet_urls':_get_entities(tweet,type='urls'),
                    #'tweet_date': _get_tweet_date(str(tweet.created_at)),
                    "tweet_date":_get_tweet_date(tweet._json['created_at']).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    'tweet_loc': tweet.geo,
                    'retweeted': tweet.retweeted,
                    'tweet_emoticons':emojis,
                    'reply_text': None
            }
        else:
            data = {
                    'id' : tweet.id,
                    'verified': tweet.user.verified,
                    'country': poi['country'],
                    'tweet_text': text,
                    'tweet_lang': tweet.lang,
                    lng : clean_text,
                    'hashtags': _get_entities(tweet,type='hashtags'),
                    #'tweet_date': _get_tweet_date(str(tweet.created_at))
                    "tweet_date":_get_tweet_date(tweet._json['created_at']).strftime("%Y-%m-%dT%H:%M:%SZ")
            }


        if tweet.in_reply_to_user_id and tweet_type =='poi':
            temp = {
                'replied_to_tweet_id': tweet.in_reply_to_status_id,
                'replied_to_user_id': tweet.in_reply_to_user_id,
                'reply_text' : text,
            }
            del data['poi_id']
            del data['poi_name']
            del data['tweet_urls']
            del data['hashtags']
            del data['retweeted']
            del data['tweet_emoticons']

            data.update(temp)
        elif tweet.in_reply_to_user_id and tweet_type == 'keyword':
            temp = {
                'replied_to_tweet_id': tweet.in_reply_to_status_id,
                'replied_to_user_id': tweet.in_reply_to_user_id,
                'reply_text' : text,
            }
            data.update(temp)
        if 'poi_name' in data and data['poi_name'] not in poisList:
            return None
        return data



def _get_entities(tweet, type=None):
    result = []
    if type == 'hashtags':
        hashtags = tweet.entities['hashtags']

        for hashtag in hashtags:
            result.append(hashtag['text'])
    elif type == 'mentions':
        mentions = tweet.entities['user_mentions']

        for mention in mentions:
            result.append(mention['screen_name'])
    elif type == 'urls':
        urls = tweet.entities['urls']

        for url in urls:
            result.append(url['url'])

    return result


def _text_cleaner(text):
    emoticons_happy = list([
        ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
        ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
        '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
        'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
        '<3'
    ])
    emoticons_sad = list([
        ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
        ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
        ':c', ':{', '>:\\', ';('
    ])
    all_emoticons = emoticons_happy + emoticons_sad

    emojis = list(demoji.findall(text).keys())
    clean_text = demoji.replace(text, '')

    for emo in all_emoticons:
        if (emo in clean_text):
            clean_text = clean_text.replace(emo, '')
            emojis.append(emo)

    clean_text = preprocessor.clean(text)
    # preprocessor.set_options(preprocessor.OPT.EMOJI, preprocessor.OPT.SMILEY)
    # emojis= preprocessor.parse(text)

    return clean_text, emojis


def _get_tweet_date(tweet_date):
    return _hour_rounder(datetime.datetime.strptime(tweet_date, '%a %b %d %H:%M:%S +0000 %Y'))


def _hour_rounder(t):
    # Rounds to nearest hour by adding a timedelta hour if minute >= 30
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
            + datetime.timedelta(hours=t.minute // 30))

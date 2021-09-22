'''
@author: Souvik Das
Institute: University at Buffalo
'''

import demoji, re, datetime
import preprocessor


# demoji.download_codes()


class TWPreprocessor:
    @classmethod
    def preprocess(cls, tweet, poi):
        '''
        Do tweet pre-processing before indexing, make sure all the field data types are in the format as asked in the project doc.
        :param tweet:
        :return: dict
        '''
        text = None
        if tweet.in_reply_to_user_id:
            temp = ''
            if tweet._json.get('text'):
                temp = tweet._json.get('text').split(" ")
            else :
                temp = tweet._json.get('full_text').split(" ")
            temp.pop(0)
            temp = " ".join(temp)
            text = temp
        else :
            text = tweet.full_text

        clean_text, emojis = _text_cleaner(text)
        data = {'poi_name': tweet.user.screen_name,
            'poi_id': tweet.user.id,
            'verified': tweet.user.verified,
            'country': poi['country'],
            'replied_to_tweet_id': tweet.in_reply_to_status_id,
            'replied_to_user_id': tweet.in_reply_to_user_id,
            'tweet_text': text,
            'tweet_xx': clean_text,
            'tweet_lang': tweet.lang,
            'hashtags': _get_entities(tweet,type ="hashtags"),
            'mentions': _get_entities(tweet, type ="mentions"),
            'tweet_urls': _get_entities(tweet,type = "urls"),
            'tweet_date': tweet.created_at,
            'tweet_loc': tweet.geo,
            'retweeted': tweet.retweeted,
            'replied_to_screen_name': tweet.in_reply_to_screen_name,
            'tweet_emoticons':emojis,
            'reply_text': None
           }
        if tweet.in_reply_to_user_id:
            temp1 ={
            'poi_name': tweet.user.screen_name,
            'poi_id': tweet.user.id,
            'reply_text': text
            }
            data.update(temp1)
        #print(data)
        return data
        raise NotImplementedError


def _get_entities(tweet, type=None):
    result = []
    if type == 'hashtags':
        hashtags = tweet['entities']['hashtags']

        for hashtag in hashtags:
            result.append(hashtag['text'])
    elif type == 'mentions':
        mentions = tweet['entities']['user_mentions']

        for mention in mentions:
            result.append(mention['screen_name'])
    elif type == 'urls':
        urls = tweet['entities']['urls']

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

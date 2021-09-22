import json
import pandas as pd
from twitter import Twitter
from tweet_preprocessor import TWPreprocessor
from indexer import Indexer

reply_collection_knob = False


def read_config():
    with open("config.json") as json_file:
        data = json.load(json_file)

    return data


def write_config(data):
    with open("config.json", 'w') as json_file:
        json.dump(data, json_file)


def save_file(data, filename):
    df = pd.DataFrame(data)
    df.to_pickle("data/" + filename)


def read_file(type, id):
    return pd.read_pickle(f"data/{type}_{id}.pkl")


def main():
    config = read_config()
    indexer = Indexer()
    twitter = Twitter()

    pois = config["pois"]
    #keywords = config["keywords"]
    keywords = [
    {
      "id": 1,
      "name": "covid vaccine",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
    {
      "id": 2,
      "name": "vaccines",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
    {
      "id": 3,
      "name": "cuarentena",
      "count": 5,
      "lang": "es",
      "country": "MEXICO",
      "finished": 0
    },
    {
      "id": 3,
      "name": "ventilator",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
    {
      "id": 3,
      "name": "homequarantine",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    }


  ]
    """

    for i in range(len(pois)):
        if pois[i]["finished"] == 0:
            print(f"---------- collecting tweets for poi: {pois[i]['screen_name']}")
            raw_tweets = twitter.get_tweets_by_poi_screen_name(pois[i]["screen_name"], pois[i]["count"])
            
            processed_tweets = []
            for tw in raw_tweets:
                processed_tweets.append(TWPreprocessor.preprocess(tw))

            indexer.create_documents(processed_tweets)

            pois[i]["finished"] = 1
            pois[i]["collected"] = len(processed_tweets)

            write_config({
                "pois": pois, "keywords": keywords
            })

            save_file(processed_tweets, f"poi_{pois[i]['id']}.pkl")
            print("------------ process complete -----------------------------------")
    """
    count = 0
    for i in range(len(keywords)):
        if keywords[i]["finished"] == 0:
            print(f"---------- collecting tweets for keyword: {keywords[i]['name']}")
            raw_tweets = twitter.get_tweets_by_lang_and_keyword(keywords[i]["count"], keywords[i]["name"], keywords[i]["lang"])

            processed_tweets = []
            
            for tw in raw_tweets:
                processed_tweets.append(TWPreprocessor.preprocess(tw))
                count = count + 1
                print(tw)
            print(count)

            
            indexer.create_documents(processed_tweets)

            keywords[i]["finished"] = 1
            keywords[i]["collected"] = len(processed_tweets)

            write_config({
                "pois": pois, "keywords": keywords
            })

            save_file(processed_tweets, f"keywords_{keywords[i]['id']}.pkl")
            
            print("------------ process complete -----------------------------------")

    if reply_collection_knob:
        # Write a driver logic for reply collection, use the tweets from the data files for which the replies are to collected.
        raise NotImplementedError
    


    return
if __name__ == "__main__":
    main()

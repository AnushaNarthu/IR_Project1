import json
import re
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

    
    pois = [{"id": 1, "screen_name": "JoeBiden", "country": "USA", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
           {"id": 2, "screen_name": "CDCgov", "country": "USA", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
           {"id": 3, "screen_name": "drharshvardhan", "country": "INDIA", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
           {"id": 4, "screen_name": "SenatorLeahy", "country": "USA", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
           {"id": 5, "screen_name": "SecBecerra", "country": "USA", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
           {"id": 6, "screen_name": "narendramodi", "country": "INDIA", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
           {"id": 7, "screen_name": "AmitShah", "country": "INDIA", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
           {"id": 8, "screen_name": "KTRTRS", "country": "INDIA", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
            {"id": 9, "screen_name": "RahulGandhi", "country": "INDIA", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
            {"id": 10, "screen_name": "ArvindKejriwal", "country": "INDIA", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
            {"id":11, "screen_name": "osoriochong", "country": "MEXICO", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
            {"id": 12, "screen_name": "FelipeCalderon", "country": "MEXICO", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
            {"id": 13, "screen_name": "lopezobrador_", "country": "MEXICO", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
            {"id": 14, "screen_name": "GustavoMadero", "country": "MEXICO", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
            {"id": 15, "screen_name": "ManceraMiguelMX", "country": "MEXICO", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
            {"id": 16, "screen_name": "GovLarryHogan", "country": "USA", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
            {"id": 17, "screen_name": "AyushmanNHA", "country": "INDIA", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
            {"id": 18, "screen_name": "PMOIndia", "country": "INDIA", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
            {"id": 19, "screen_name": "MoHFW_INDIA", "country": "INDIA", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0}]
    #keywords = config["keywords"]
    keywords = [
    {
      "id": 1,
      "name": "covid",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
    {
      "id": 2,
      "name": "vaccine",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
    {
      "id": 3,
      "name": "salud",
      "count": 5,
      "lang": "es",
      "country": "MEXICO",
      "finished": 0
    },
    {
      "id": 4,
      "name": "ventilator",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
    {
      "id": 5,
      "name": "quarantine",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
    {
      "id": 6,
      "name": "corona",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
    {
      "id": 7,
      "name": "cuarentena",
      "count": 5,
      "lang": "es",
      "country": "MEXICO",
      "finished": 0
    },
    {
      "id": 8,
      "name": "oxígeno",
      "count": 5,
      "lang": "es",
      "country": "MEXICO",
      "finished": 0
    },
    {
      "id": 9,
      "name": "desinfectante",
      "count": 5,
      "lang": "es",
      "country": "MEXICO",
      "finished": 0
    },
    {
      "id": 10,
      "name": "mascaras",
      "count": 5,
      "lang": "es",
      "country": "MEXICO",
      "finished": 0
    },
    {
      "id": 11,
      "name": "quedate en casa",
      "count": 5,
      "lang": "es",
      "country": "MEXICO",
      "finished": 0
    },
    {
      "id": 12,
      "name": "trabajar desde casa",
      "count": 5,
      "lang": "es",
      "country": "MEXICO",
      "finished": 0
    },
    {
      "id": 13,
      "name": "anticuerpos",
      "count": 5,
      "lang": "es",
      "country": "MEXICO",
      "finished": 0
    },
    {
      "id": 14,
      "name": "vacuna covid",
      "count": 5,
      "lang": "es",
      "country": "MEXICO",
      "finished": 0
    },
    {
      "id": 15,
      "name": "dosis de vacuna",
      "count": 5,
      "lang": "es",
      "country": "MEXICO",
      "finished": 0
    },
    {
      "id": 16,
      "name": "inyección de refuerzo",
      "count": 5,
      "lang": "es",
      "country": "MEXICO",
      "finished": 0
    },
    {
      "id": 17,
      "name": "vacunado",
      "count": 5,
      "lang": "es",
      "country": "MEXICO",
      "finished": 0
    },
    {
      "id": 18,
      "name": "vacunas",
      "count": 5,
      "lang": "es",
      "country": "MEXICO",
      "finished": 0
    },
    {
      "id": 19,
      "name": "vacuna",
      "count": 5,
      "lang": "es",
      "country": "MEXICO",
      "finished": 0
    },
  
    {
      "id": 25,
      "name": "rt-pcr",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
    {
      "id": 26,
      "name": "oxygen",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
    {
      "id": 27,
      "name": "stayhomestaysafe",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
    {
      "id": 28,
      "name": "covid19",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
    {
      "id": 29,
      "name": "face mask",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
  
    {
      "id": 34,
      "name": "covid symptoms",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
    {
      "id": 35,
      "name": "covidiot",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
    
   
    {
      "id": 54,
      "name": "वैश्विकमहामारी",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 55,
      "name": "सुरक्षित रहें",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 56,
      "name": "मास्क",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 57,
      "name": "वायरस",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 54,
      "name": "संक्रमण",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 58,
      "name": "सैनिटाइज़र",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 59,
      "name": "संक्रमण",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 60,
      "name": "वायरस",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 61,
      "name": "सामाजिक दूरी",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 62,
      "name": "प्रक्षालक",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id":  63,
      "name": "कोरोना",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 64,
      "name": "कोविड 19",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 65,
      "name": "कोविड",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
   
    {
      "id": 74,
      "name": "कोविड के केस",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 75,
      "name": "प्रकोप",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 76,
      "name": "संक्रमित",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 77,
      "name": "कोरोनावाइरस",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id":78,
      "name": "मास्क पहनें",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 79,
      "name": "ऑक्सीजन",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 80,
      "name": "कोरोनावायरस",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 81,
      "name": "महामारी",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 82,
      "name": "रोग",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 83,
      "name": "टीका",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 84,
      "name": "फाइजर",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 85,
      "name": "एस्ट्राजेनेका",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 54,
      "name": "कोविड टीका",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 86,
      "name": "टीकाजीतका",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 87,
      "name": "टीका लगवाएं",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 88,
      "name": "दुष्प्रभाव",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 89,
      "name": "लसीकरण",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 90,
      "name": "प्रभाव",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 91,
      "name": "वैक्सीन",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 92,
      "name": "कोविन",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    
   
  ]
    cnt=0
    for i in range(len(pois)):
        if pois[i]["finished"] == 0:
            print(f"---------- collecting tweets for poi: {pois[i]['screen_name']}")
            raw_tweets = twitter.get_tweets_by_poi_screen_name(pois[i]["screen_name"], pois[i]["count"])
            
            processed_tweets = []
            for tw in raw_tweets:                
                processed_tweets.append(TWPreprocessor.preprocess(tw))
                cnt = cnt + 1
                #print(tw)
                #print(cnt)

            indexer.create_documents(processed_tweets)

            pois[i]["finished"] = 1
            pois[i]["collected"] = len(processed_tweets)

            write_config({
                "pois": pois, "keywords": keywords
            })

            save_file(processed_tweets, f"poi_{pois[i]['id']}.pkl")
            print("------------ process complete -----------------------------------")
   
    count = 0
    for i in range(len(keywords)):
        if keywords[i]["finished"] == 0:
            print(f"---------- collecting tweets for keyword: {keywords[i]['name']}")
            raw_tweets = twitter.get_tweets_by_lang_and_keyword(keywords[i]["count"], keywords[i]["name"], keywords[i]["lang"])

            processed_tweets = []
            
            for tw in raw_tweets:
                processed_tweets.append(TWPreprocessor.preprocess(tw))
                count = count + 1
                #print(tw)
                #print(count)

            
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

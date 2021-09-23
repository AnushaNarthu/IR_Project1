import json
import pandas as pd
from twitter import Twitter
from tweet_preprocessor import TWPreprocessor
from indexer import Indexer
import re

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
           {"id": 3, "screen_name": "GavinNewsom", "country": "USA", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
           {"id": 4, "screen_name": "HHSGov", "country": "USA", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
           {"id": 5, "screen_name": "sensanders", "country": "USA", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
           {"id": 6, "screen_name": "narendramodi", "country": "INDIA", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
           {"id": 7, "screen_name": "AmitShah", "country": "INDIA", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
           {"id": 8, "screen_name": "JPNadda", "country": "INDIA", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
            {"id": 9, "screen_name": "RahulGandhi", "country": "INDIA", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
            {"id": 10, "screen_name": "ArvindKejriwal", "country": "INDIA", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
            {"id":11, "screen_name": "osoriochong", "country": "MEXICO", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
            {"id": 12, "screen_name": "FelipeCalderon", "country": "MEXICO", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
            {"id": 13, "screen_name": "SSalud_mx", "country": "MEXICO", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
            {"id": 14, "screen_name": "lopezobrador_", "country": "MEXICO", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
            {"id": 15, "screen_name": "GustavoMadero", "country": "MEXICO", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
            {"id": 16, "screen_name": "ManceraMiguelMX", "country": "MEXICO", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
            {"id": 17, "screen_name": "GovLarryHogan", "country": "USA", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
            {"id": 18, "screen_name": "AyushmanNHA", "country": "INDIA", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
            {"id": 19, "screen_name": "MoHFW_INDIA", "country": "INDIA", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
            {"id": 20, "screen_name": "KamalaHarris", "country": "USA", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
            {"id": 21, "screen_name": "POTUS", "country": "USA", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
            {"id": 22, "screen_name": "SecBecerra", "country": "USA", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
            {"id": 23, "screen_name": "SenatorLeahy", "country": "USA", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
            {"id": 24, "screen_name": "mansukhmandviya", "country": "INDIA", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
            {"id": 25, "screen_name": "rashtrapatibhvn", "country": "INDIA", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0},
            {"id": 26, "screen_name": "PMOIndia", "country": "INDIA", "count": 1, "finished": 0 , "reply_finished": 0, "collected": 0}]
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
      "id": 20,
      "name": "eficacia",
      "count": 5,
      "lang": "es",
      "country": "MEXICO",
      "finished": 0
    },
    {
      "id": 21,
      "name": "segunda dosis",
      "count": 5,
      "lang": "es",
      "country": "MEXICO",
      "finished": 0
    },
    {
      "id": 22,
      "name": "dosis",
      "count": 5,
      "lang": "es",
      "country": "MEXICO",
      "finished": 0
    },
    {
      "id": 23,
      "name": "hospital",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
    {
      "id": 24,
      "name": "covidresources",
      "count": 5,
      "lang": "en",
      "country": "USA",
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
      "id": 30,
      "name": "covidsecondwaveinindia",
      "count": 5,
      "lang": "en",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 31,
      "name": "flattenthecurve",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
    {
      "id": 32,
      "name": "stay safe",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
    {
      "id": 33,
      "name": "covid test",
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
      "id": 36,
      "name": "disease",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
    {
      "id": 37,
      "name": "staysafe",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
    {
      "id": 38,
      "name": "doctor",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
    {
      "id": 39,
      "name": "facemask",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
    {
      "id": 40,
      "name": "epidemic",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
    {
      "id": 41,
      "name": "transmission",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
    {
      "id": 42,
      "name": "social distance",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
    {
      "id": 43,
      "name": "surgical mask",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
    {
      "id": 44,
      "name": "vaccines",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
    {
      "id": 45,
      "name": "covid vaccine",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
    {
      "id": 46,
      "name": "vaccine side effect",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
    {
      "id": 47,
      "name": "johnson & johnson",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
    {
      "id": 48,
      "name": "immunity",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
    {
      "id": 49,
      "name": "vaccination drive",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
    {
      "id":50,
      "name": "we4vaccine",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
    {
      "id": 51,
      "name": "injection",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
    {
      "id": 52,
      "name": "sputnik",
      "count": 5,
      "lang": "en",
      "country": "USA",
      "finished": 0
    },
    {
      "id": 53,
      "name": "astrazeneca",
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
      "id": 66,
      "name": "वाइरस",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 67,
      "name": "वेंटिलेटर",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 68,
      "name": "डेल्टा",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 69,
      "name": "मौत",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 70,
      "name": "कोविड महामारी",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 71,
      "name": "फ़्लू",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 72,
      "name": "स्वच्छ",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 73,
      "name": "लक्षण",
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
    {
      "id": 93,
      "name": "कोवैक्सीन",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 94,
      "name": "कोवैक्सिन",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 95,
      "name": "खराब असर",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 96,
      "name": "कोविड का टीका",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 97,
      "name": "वाइरस",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 98,
      "name": "खुराक",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 99,
      "name": "कोवेक्सिन",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 100,
      "name": "वैक्सीनेशन",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 101,
      "name": "एंटीबॉडी",
      "count": 5,
      "lang": "hi",
      "country": "INDIA",
      "finished": 0
    },
    {
      "id": 102,
      "name": "कोविशील्ड",
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
                
                if re.search("RT", tw['tweet_text']):
                   continue
                key_lang = tw["tweet_lang"]
                if key_lang == "en":
                    count_en = count_en + 1
                elif key_lang == "hi":
                    count_hi = count_hi + 1
                else:
                    count_es = count_es +1
                processed_tweets.append(TWPreprocessor.preprocess(tw))

            indexer.create_documents(processed_tweets)

            pois[i]["finished"] = 1
            pois[i]["collected"] = len(processed_tweets)

            write_config({
                "pois": pois, "keywords": keywords
            })

            save_file(processed_tweets, f"poi_{pois[i]['id']}.pkl")
            print("------------ process complete -----------------------------------")
    
    
    for i in range(len(keywords)):
        if keywords[i]["finished"] == 0:
            print(f"---------- collecting tweets for keyword: {keywords[i]['name']}")
            raw_tweets = twitter.get_tweets_by_lang_and_keyword(keywords[i]["count"], keywords[i]["name"], keywords[i]["lang"])

            processed_tweets = []
            
            for tw in raw_tweets:
                if re.search("RT", tw['tweet_text']):
                   continue
                key_lang = tw["tweet_lang"]
                if key_lang == "en":
                    count_en = count_en + 1
                elif key_lang == "hi":
                    count_hi = count_hi + 1
                else:
                    count_es = count_es +1
                processed_tweets.append(TWPreprocessor.preprocess(tw))
                count = count + 1
                #print(tw)
            print(count)

            
            indexer.create_documents(processed_tweets)

            keywords[i]["finished"] = 1
            keywords[i]["collected"] = len(processed_tweets)

            write_config({
                "pois": pois, "keywords": keywords
            })

            save_file(processed_tweets, f"keywords_{keywords[i]['id']}.pkl")
            
            print("------------ process complete -----------------------------------")
    
            print("count_en"+str(count_en))
            print("count_en"+str(count_hi))
            print("count_en"+str(count_es))
    
    if reply_collection_knob:
        # Write a driver logic for reply collection, use the tweets from the data files for which the replies are to collected.
        raise NotImplementedError
    


    return
if __name__ == "__main__":
    main()

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import KafkaProducer, KafkaClient
from sentiment import *
import json

access_token = "1323451448781238274-ARnzAE9Jr9T4KjiruQSqIJM4WnAiCk"
access_token_secret =  "KfMietdsdxqRqKiEVVEJdKypfGbrWjFaE9Y92Y1ij4ilk"
consumer_key =  "doz9ZltVGwMmlg2PTptGcoMLd"
consumer_secret =  "0BrrMlwj443opgxpjkowqJ18vqrwLnHUaY1eooYTvL4xZmtfFJ"

class StdOutListener(StreamListener):
    def __init__(self):
        self.sentiment_analyzer = Sentiment()

    def on_data(self, data):
        json_obj = json.loads(data)
        producer.send("trump", data.encode('utf-8'))
        if 'text' in json_obj:
            if json_obj['lang'] == 'en':
                score = self.sentiment_analyzer.score_text(json_obj["text"])

        return True
    def on_error(self, status):
        print (status)

kafka = KafkaClient()
producer = KafkaProducer()
l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l)
stream.filter(track="trump")

# if __name__ == "__main__":
#     TS = TwitterStreamer()
#     TS.stream_tweets()
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import KafkaProducer, KafkaClient
from sentiment import *
import json

class TwitterStreamProducer:
    def __init__(self, topic):
        access_token = "1323451448781238274-ARnzAE9Jr9T4KjiruQSqIJM4WnAiCk"
        access_token_secret =  "KfMietdsdxqRqKiEVVEJdKypfGbrWjFaE9Y92Y1ij4ilk"
        consumer_key =  "doz9ZltVGwMmlg2PTptGcoMLd"
        consumer_secret =  "0BrrMlwj443opgxpjkowqJ18vqrwLnHUaY1eooYTvL4xZmtfFJ"
        kafka = KafkaClient()
        producer = KafkaProducer()
        l = StdOutListener(kafka, producer, topic)
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        stream = Stream(auth, l)
        stream.filter(track="twitter")

class StdOutListener(StreamListener):
    def __init__(self, kafka, producer, topic):
        self.kafka = kafka
        self.producer = producer
        self.topic = topic

    def on_data(self, data):
        self.producer.send(self.topic, data.encode('utf-8'))
        json_obj = json.loads(data)
        if 'text' in json_obj:
            if json_obj['lang'] == 'en':
                print('Message {}'.format(json_obj['text']))
        return True

    def on_error(self, status):
        print (status)
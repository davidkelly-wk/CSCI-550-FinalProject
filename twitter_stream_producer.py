from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import KafkaProducer
import json

# Twitter API access keys
access_token = "1323451448781238274-ARnzAE9Jr9T4KjiruQSqIJM4WnAiCk"
access_token_secret =  "KfMietdsdxqRqKiEVVEJdKypfGbrWjFaE9Y92Y1ij4ilk"
consumer_key =  "doz9ZltVGwMmlg2PTptGcoMLd"
consumer_secret =  "0BrrMlwj443opgxpjkowqJ18vqrwLnHUaY1eooYTvL4xZmtfFJ"
# Topic and producer
topic = "default_topic"
producer = KafkaProducer(bootstrap_servers='localhost:9092')

class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return auth


class TwitterStreamProducer():
    def __init__(self, topic_name):
        global topic
        topic = topic_name
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self):
        while True:
            listener = TwitterStreamListener()
            auth = self.twitter_authenticator.authenticate_twitter_app()
            stream = Stream(auth, listener)
            stream.filter(track="twitter", stall_warnings=True, languages= ["en"])
        

class TwitterStreamListener(StreamListener):
    def on_data(self, data):
        producer.send(topic, data.encode('utf-8'))
        json_obj = json.loads(data)
        if 'text' in json_obj:
            if json_obj['lang'] == 'en':
                print('Message {}'.format(json_obj['text']))
        return True

    def on_error(self, status):
        print (status)

if __name__ == "__main__":
    topic = input('Enter a kafka topic name: ')
    run_producer = input('Do you wish to run the twitter producer (y/n)? ')
    if run_producer == 'y':
        tsp = TwitterStreamProducer(topic)
        tsp.stream_tweets()
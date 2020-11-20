from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import KafkaProducer
import threading
import metrics
import json

#JoeBiden id: 939091
#realDonaldTrump id: 25073877

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
        self.metrics = metrics.Metrics(producer=producer)

    def stream_tweets(self):
        self.log_metrics()
        while True:
            listener = TwitterStreamListener()
            auth = self.twitter_authenticator.authenticate_twitter_app()
            stream = Stream(auth, listener)
            stream.filter(track=['trump', 'biden'], stall_warnings=True, languages= ["en"])

    def log_metrics(self):
        producer_metrics = self.metrics.get_producer_metrics()
        print(producer_metrics)
        timerThread = threading.Timer(10, self.log_metrics)
        timerThread.daemon = True
        timerThread.start()
        

class TwitterStreamListener(StreamListener):
    def on_data(self, data):
        producer.send(topic, data.encode('utf-8'))
        """
        json_obj = json.loads(data)
        if 'text' in json_obj:
            if json_obj['lang'] == 'en':
                print('Message {}'.format(json_obj['text']))
        """
        return True

    def on_error(self, status):
        print (status)

if __name__ == "__main__":
    topic = 'trumpbiden'
    tsp = TwitterStreamProducer(topic)
    tsp.stream_tweets()
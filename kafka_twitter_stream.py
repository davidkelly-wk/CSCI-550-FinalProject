from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import KafkaProducer, KafkaClient

access_token = "1323451448781238274-ARnzAE9Jr9T4KjiruQSqIJM4WnAiCk"
access_token_secret =  "KfMietdsdxqRqKiEVVEJdKypfGbrWjFaE9Y92Y1ij4ilk"
consumer_key =  "doz9ZltVGwMmlg2PTptGcoMLd"
consumer_secret =  "0BrrMlwj443opgxpjkowqJ18vqrwLnHUaY1eooYTvL4xZmtfFJ"

class StdOutListener(StreamListener):
    def on_data(self, data):
        producer.send("trump", data.encode('utf-8'))
        print (data)
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
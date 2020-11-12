from kafka import KafkaConsumer
from json import loads
from sentiment import *
from data_aggregator import *

class AverageSentimentConsumer:
    def __init__(self, topic):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id=None,
            value_deserializer=lambda x: loads(x.decode('utf-8')))
        self.sentiment_analyzer = Sentiment()
        #self.data_aggregator = Data_Aggregator()
    
    def calculate_sentiment_score(self, message):
        if 'text' in message:
            if message['lang'] == 'en':
                score = self.sentiment_analyzer.score_text(message['text'])
                print('Message score: {} for message: {}'.format(score, message['text']))
        return score

    def average_sentiment(self, consumer):
        i = 0
        avg_score = float(0)
        for message in consumer:
            message = message.value
            score = self.calculate_sentiment_score(message)
            if avg_score != float(0): # if this is the first message, just add it rather than average it
                avg_score = (avg_score + score) / 2
            else: 
                avg_score = score
            print('Avg score: {} after message {}'.format(avg_score, i))
        i += 1
        if i % 10 == 0: # plot after 10 messages
            i = 0
            avg_score = float(0)
            #self.data_aggregator.add_score(avg_score)
            #self.data_aggregator.update_plot()


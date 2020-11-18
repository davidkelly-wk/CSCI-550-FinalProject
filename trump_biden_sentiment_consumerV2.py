from kafka import KafkaConsumer
from json import loads
from sentiment import *
import numpy as np
from pylive import live_plotter

class AverageSentimentConsumer():
    def __init__(self, topic):
        self.consumers = []
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            auto_commit_interval_ms =  5000,
            fetch_max_bytes = 128,
            max_poll_records = 100,
            group_id=None,
            value_deserializer=lambda x: loads(x.decode('utf-8')))
        self.sentiment_analyzer = Sentiment()

        size = 100
        self.x_vec = np.linspace(0, 1, size + 1)[0:-1]
        self.y_vec_trump = np.zeros(len(self.x_vec))
        self.y_vec_biden = np.zeros(len(self.x_vec))
        self.line_trump = []
        self.line_biden = []

    def calculate_sentiment_score(self, message):
        score = float('inf') # in case message not in english
        if 'text' in message:
            if message['lang'] == 'en':
                score = self.sentiment_analyzer.score_text(message['text'])
                # print('Message score: {} for message: {}'.format(score, message['text']))
        return score

    def average_sentiment(self, consumer):
        trump_i = 0
        biden_i = 0
        avg_score_trump = float(0)
        avg_score_biden = float(0)
        for message in consumer:
            message = message.value
            score = self.calculate_sentiment_score(message)
            if score != float('inf'): # if 'inf' something went wrong calculating the score
                if 'trump' in message['text'].lower():
                    trump_i += 1
                    if avg_score_trump != float(0): # if this is the first message, just add it rather than average it

                        avg_score_trump = (avg_score_trump + score) / 2
                    else:
                        avg_score_trump = score
                if 'biden' in message['text'].lower():
                    biden_i += 1
                    if avg_score_biden != float(0):  # if this is the first message, just add it rather than average it

                        avg_score_biden = (avg_score_biden + score) / 2
                    else:
                        avg_score_biden = score

            # print('Avg score trump: {} after message {}'.format(avg_score_trump, trump_i))
            # print('Avg score biden: {} after message {}'.format(avg_score_biden, biden_i))

            if biden_i > 10 or trump_i > 10:
                consume_rate = consumer.metrics()['consumer-fetch-manager-metrics']['records-consumed-rate']
                #send to graph
                self.y_vec_trump[-1] = avg_score_trump
                self.y_vec_biden[-1] = avg_score_biden
                self.line_trump, self.line_biden = live_plotter(self.x_vec, self.y_vec_trump, self.y_vec_biden,  self.line_trump, self.line_biden)
                self.y_vec_trump = np.append(self.y_vec_trump[1:], 0.0)
                self.y_vec_biden = np.append(self.y_vec_biden[1:], 0.0)
                biden_i = 0
                avg_score_biden = float(0)
                trump_i = 0
                avg_score_trump = float(0)

        

    def start_consumer(self):
        while True:
            self.average_sentiment(self.consumer)

if __name__ == "__main__":
    topic = 'trumpbiden'
    asc = AverageSentimentConsumer(topic)
    asc.start_consumer()
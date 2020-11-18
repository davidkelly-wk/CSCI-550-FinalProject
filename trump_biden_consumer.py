from kafka import KafkaConsumer
from json import loads
from sentiment import *

class TrumpBidenConsumer():
    def __init__(self, topic):
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

    def calculate_sentiment_score(self, message):
        score = float('inf') # in case message not in english
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
            if score != float('inf'): # if 'inf' something went wrong calculating the score
                if avg_score != float(0): # if this is the first message, just add it rather than average it
                    avg_score = (avg_score + score) / 2
                else: 
                    avg_score = score
            print('Avg score: {} after message {}'.format(avg_score, i))
            i += 1
            if i > 10:
                break
        return i, avg_score
        

    def start_consumer(self):
        while True:
            fetched_records, avg_score = self.average_sentiment(self.consumer)
            print('Records fetched: {} with avg. score : {}'.format(fetched_records, avg_score))
        self.average_sentiment(self.consumer)

if __name__ == "__main__":
    topic = input('Enter a kafka topic name: ')
    run_average_consumer = input('Do you wish to run the sentiment averaging consumer (y/n)? ')

    if run_average_consumer == 'y':
        asc = AverageSentimentConsumer(topic)
        asc.start_consumer()
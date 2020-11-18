from kafka import KafkaConsumer
from json import loads
from sentiment import *
from pylive_1line import *

class AverageSentimentConsumer():
    def __init__(self, topic):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            auto_commit_interval_ms =  5000,
            group_id=None,
            value_deserializer=lambda x: loads(x.decode('utf-8')))
        self.sentiment_analyzer = Sentiment()

        size = 100
        self.x_vec = np.linspace(0, 1, size + 1)[0:-1]
        self.y_vec = np.zeros(len(self.x_vec))
        self.line1 = []

    def calculate_sentiment_score(self, message):
        score = float('inf') # in case message not in english
        if 'text' in message:
            if message['lang'] == 'en':
                message = self.sentiment_analyzer.remove_url(message['text'])
                score = self.sentiment_analyzer.score_text(message)
                print('Message score: {} for message: {}'.format(score, message))
        return score

    def average_sentiment(self, consumer):
        i = 1
        avg_score = float(0)
        msg_pack = self.consumer.poll(timeout_ms=5000)
        for tp, messages in msg_pack.items():
            #print(len(msg_pack.items()))
            #print(len(messages))
            for message in messages:
                message = message.value
                score = self.calculate_sentiment_score(message)
                if score != float('inf'): # if 'inf' something went wrong calculating the score
                    if avg_score != float(0): # if this is the first message, just add it rather than average it
                        avg_score = (avg_score + score) / 2
                    else: 
                        avg_score = score
                print('Avg score: {} after message {}'.format(avg_score, i))
                i += 1
                # send to graph
                self.y_vec[-1] = avg_score
                self.line1 = live_plotter(self.x_vec, self.y_vec, self.line1)
                self.y_vec = np.append(self.y_vec[1:], 0.0)
        consume_rate = consumer.metrics()['consumer-fetch-manager-metrics']['records-consumed-rate']


    def start_consumer(self):
        while True:
            fetched_records, avg_score = self.average_sentiment(self.consumer)
            print('Records fetched: {} with avg. score : {}'.format(fetched_records, avg_score))

if __name__ == "__main__":
    topic = input('Enter a kafka topic name: ')
    run_average_consumer = input('Do you wish to run the sentiment averaging consumer (y/n)? ')

    if run_average_consumer == 'y':
        asc = AverageSentimentConsumer(topic)
        asc.start_consumer()
import twitter_stream_producer as tsp
import average_sentiment_consumer as asc

class Main:
    def __init__(self, topic, run_producer, run_average_consumer):
            self.topic = topic
            self.run_producer = run_producer
            self.run_average_consumer = run_average_consumer

    def main(self):
        if (self.run_producer == 'y'):
            print(self.run_producer)
            self.tsp = tsp.TwitterStreamProducer(self.topic)
        #if (self.run_average_consumer == 'y'):
        #    self.asc = asc.AverageSentimentConsumer(self.topic)

topic = input('Enter a kafka topic name: ')
run_producer = input('Do you wish to run the twitter producer (y/n)? ')
run_average_consumer = input('Do you wish to run the sentiment averaging consumer (y/n)? ')
Main(topic, run_producer, run_average_consumer).main()


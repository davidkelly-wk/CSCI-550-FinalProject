import json
from kafka import KafkaConsumer, KafkaProducer


class Metrics(object):
    def __init__(self, producer = None, consumer = None):
        self.producer = producer
        self.consumer = consumer
        self.producer_metrics = {}
        self.producer_metrics['producer metrics'] = []
        self.consumer_metrics = {}
        self.consumer_metrics['consumer metrics'] = []
   
    def get_producer_metrics(self):
        self.producer_metrics['producer metrics'] = []
        send_rate = self.producer.metrics()['producer-metrics']['record-send-rate']
        self.producer_metrics['producer metrics'].append({'record-send-rate': send_rate})
        self.write_metrics('producer_metrics.txt', self.producer_metrics)
        return send_rate

    def get_consumer_metrics(self):
        self.consumer_metrics['consumer metrics'] = []
        consumption_rate = self.consumer.metrics()['consumer-fetch-manager-metrics']['records-consumed-rate']
        self.consumer_metrics['consumer metrics'].append({'records-consumed-rate': consumption_rate})
        self.write_metrics('consumer_metrics.txt', self.consumer_metrics)
        return consumption_rate
    
    def write_metrics(self, filename, metrics):
        with open(filename, 'w') as outfile:
            json.dump(metrics, outfile, indent=2)
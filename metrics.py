import json
import psutil
import platform
import cpuinfo #pip install py-cpuinfo
from kafka import KafkaConsumer, KafkaProducer


class Metrics(object):
    def __init__(self, producer = None, consumer = None):
        self.producer = producer
        self.consumer = consumer
   
    def get_producer_metrics(self):
        producer_metrics = {}
        producer_metrics['producer metrics'] = []
        metrics = self.producer.metrics()

        send_rate = metrics['producer-metrics']['record-send-rate']
        records_per_request = metrics['producer-metrics']['records-per-request-avg']
        produce_throttle_time = metrics['producer-metrics']['produce-throttle-time-avg']

        producer_metrics['producer metrics'].append({'record-send-rate': send_rate})
        producer_metrics['producer metrics'].append({'records-per-request-avg': records_per_request})
        producer_metrics['producer metrics'].append({'produce-throttle-time-avg': produce_throttle_time})

        # write producer metrics
        self.write_metrics('producer_metrics.txt', producer_metrics)

        # write system metrics
        system_metrics = self.get_system_metrics()
        self.write_metrics('system_metrics.txt', system_metrics)

        return send_rate

    def get_consumer_metrics(self):
        consumer_metrics = {}
        consumer_metrics['consumer metrics'] = []
        metrics = self.consumer.metrics()
        consumption_rate = metrics['consumer-fetch-manager-metrics']['records-consumed-rate']
        records_per_request = metrics['consumer-fetch-manager-metrics']['records-per-request-avg']
        request_latency = metrics['consumer-metrics']['request-latency-avg']

        consumer_metrics['consumer metrics'].append({'records-consumed-rate': consumption_rate})
        consumer_metrics['consumer metrics'].append({'records-per-request-avg': records_per_request})
        consumer_metrics['consumer metrics'].append({'request-latency-avg': request_latency})
        request_latency
        self.write_metrics('consumer_metrics.txt', consumer_metrics)
        
        # write system metrics
        system_metrics = self.get_system_metrics()
        self.write_metrics('system_metrics.txt', system_metrics)

        return consumption_rate
    
    def get_system_metrics(self):
        uname = platform.uname()
        cpufreq = psutil.cpu_freq()
        svmem = psutil.virtual_memory()

        system_metrics = {}
        system_metrics['system'] = []
        system_metrics['system'].append({'system': uname.system})
        system_metrics['system'].append({'node name': uname.node})
        system_metrics['system'].append({'release': uname.release})
        system_metrics['system'].append({'version': uname.version})
        system_metrics['system'].append({'machine': uname.machine})
        system_metrics['system'].append({'processor': uname.processor})

        system_metrics['cpu info'] = []
        system_metrics['cpu info'].append({'model': cpuinfo.get_cpu_info()['brand_raw']})
        system_metrics['cpu info'].append({'physical cores': psutil.cpu_count(logical=False)})
        system_metrics['cpu info'].append({'total cores': psutil.cpu_count(logical=True)})
        system_metrics['cpu info'].append({'total cores': psutil.cpu_count(logical=True)})
        system_metrics['cpu info'].append({'max frequency': f'{cpufreq.max:.2f}Mhz'})
        system_metrics['cpu info'].append({'min frequency': f'{cpufreq.min:.2f}Mhz'})
        system_metrics['cpu info'].append({'current frequency': f'{cpufreq.current:.2f}Mhz'})

        system_metrics['memory info'] = []
        system_metrics['memory info'].append({'total': f'{self.get_size(svmem.total)}'})
        system_metrics['memory info'].append({'available': f'{self.get_size(svmem.available)}'})
        system_metrics['memory info'].append({'used': f'{self.get_size(svmem.used)}'})

        return system_metrics

    def get_size(self, bytes, suffix="B"):
        """
        Scale bytes to its proper format
        e.g:
            1253656 => '1.20MB'
            1253656678 => '1.17GB'
        """
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor

    def write_metrics(self, filename, metrics):
        with open(filename, 'w') as outfile:
            json.dump(metrics, outfile, indent=2)
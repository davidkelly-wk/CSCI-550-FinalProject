import json
import psutil
import platform
import cpuinfo
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
        system_metrics = self.get_system_metrics()
        self.write_metrics('system_metrics.txt', system_metrics)
        return send_rate

    def get_consumer_metrics(self):
        self.consumer_metrics['consumer metrics'] = []
        consumption_rate = self.consumer.metrics()['consumer-fetch-manager-metrics']['records-consumed-rate']
        self.consumer_metrics['consumer metrics'].append({'records-consumed-rate': consumption_rate})
        self.write_metrics('consumer_metrics.txt', self.consumer_metrics)
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
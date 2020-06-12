import json
import os
import pigpio
import requests

from ConfigParser import SafeConfigParser
from lib import DHT22
from time import sleep


class DHT22CurrentTemp:

    def __init__(self):
        parser = SafeConfigParser()
        cwd = os.path.dirname(os.path.realpath(__file__))
        parser.read(os.path.join(cwd, 'config.ini'))
        self.delay = int(os.getenv('DHT22_SERVICE_DELAY', parser.get('general', 'delay')))
        gpio = int(os.getenv('DHT22_SERVICE_GPIO', parser.get('general', 'gpio')))
        pi = pigpio.pi()
        self.dht22 = DHT22.sensor(pi, gpio)
        self.upload_api_url = os.getenv('DHT22_SERVICE_API_URL', parser.get('api', 'url'))
        self.api_key = os.getenv('DHT22_SERVICE_API_KEY', parser.get('api', 'api_key'))

    def update_remote(self, humidity, temp):
        headers = {
            'X-API-KEY': self.api_key
        }
        payload = {
          "temp_f": temp,
          "humidity_percent": humidity
        }
        return requests.put(self.upload_api_url, data=json.dumps(payload), headers=headers)

    def celcius_to_fahrenheit(self, celcius):
        return celcius * (9/5.0) + 32

    def read_dht22(self):
        self.dht22.trigger()
        humidity = '{0:.2f}'.format(round(self.dht22.humidity(), 2))
        temp = '{0:.2f}'.format(self.celcius_to_fahrenheit(round(self.dht22.temperature(), 2)))
        return humidity, temp

    def run(self):
        # clear out initial -99999 readings
        self.read_dht22()
        sleep(3)
        self.read_dht22()
        sleep(3)

        while True:
            humidity, temp = self.read_dht22()
            print("current temp {0} F and humidity {1}%".format(temp, humidity))
            response = self.update_remote(humidity, temp)
            if not response or response.status_code != 201:
                print('ERROR: uploading data to API failed')
            sleep(self.delay)


if __name__ == "__main__":
    current = DHT22CurrentTemp()
    current.run()

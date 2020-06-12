# DHT22 Service

A service to read a DHT22 sensor that is connected to a raspberry pi. The service will read the temperature and humidity every 5 seconds and update to the specified API endpoint.

By default the service reads from gpio 12 and reads every 5 seconds (the DHT22 sensor won't work well if faster then 3 seconds). If you want to change the values then simply edit the main method


## Prerequisites
None if you use the Docker script I made. Just move onto the Install section to use it.

If you don't want to use the Docker script and would rather install this manually then you'll need:

- [pigpio](http://abyz.co.uk/rpi/pigpio/download.html)
- [pigpio as a service](https://www.raspberrypi.org/forums/viewtopic.php?f=32&t=103752)
- [DHT22 Sensor](https://www.adafruit.com/product/385) and everything else (breadboard, wires, ribbon cable to connect breadboard to the pi) to connect this to your raspberry pi

## Install

Build:
```
$ docker build -t cpitzak/weather-dht22-service .
```
Run:
```
$ docker run -e "DHT22_SERVICE_API_URL=https://example.com/api/put-method" \
             -e "DHT22_SERVICE_API_KEY=YOUR_API_KEY" \
             -e "DHT22_SERVICE_DELAY=5" \
             -e "DHT22_SERVICE_GPIO=12" \
             --cap-add SYS_RAWIO \
             --device /dev/mem \
             --device /dev/vcio \
             -p 8888:8888 \
             cpitzak/weather-dht22-service
```

Or to setup Manually
```
$ sudo mkdir /apps
$ sudo chown pi /apps
$ cd /apps
$ git clone https://github.com/cpitzak/dht22Service.git
$ cd dht22Service
$ sudo cp init.d/dht22Service /etc/init.d/
$ sudo chmod 755 /etc/init.d/dht22Service
$ sudo update-rc.d dht22Service defaults
$ sudo update-rc.d dht22Service enable
$ sudo systemctl daemon-reload
$ sudo service dht22Service start
```


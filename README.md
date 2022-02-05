# OctoPrint-PlotlyTempGraph-DHT11

This plugin plots the enclosure temperature through OctoPrint-PlotlyTempGraph plugin.

Enclosure temperature is measured by a DHT11/DHT22 sensor conhected to a GPIO
pin defined by the `PIN` constant in the code.

Based on https://github.com/jneilliii/OctoPrint-PlotlyTempGraph/blob/master/klipper_additional_temp.py

Requires https://github.com/adafruit/Adafruit_Python_DHT

## Setup

* Hardware: https://learn.adafruit.com/dht/connecting-to-a-dhtxx-sensor
* Raspberry Pi: `sudo pip3 install Adafruit_DHT`
* Octoprint: upload this file through `Plugin Manager > Get More > ...from URL`

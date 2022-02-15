# OctoPrint-ChamberTempGraph-DHTxx

Plugin for plotting chamber/enclosure temperature.

Chamber temperature is measured by a DHT11/DHT22 sensor conhected to a GPIO
pin defined by the `PIN` constant in the code.

Based on https://github.com/jneilliii/OctoPrint-PlotlyTempGraph/blob/master/klipper_additional_temp.py

Requires https://github.com/adafruit/Adafruit_Python_DHT

## Setup

* Hardware: https://learn.adafruit.com/dht/connecting-to-a-dhtxx-sensor
* Raspberry Pi: `sudo pip3 install Adafruit_DHT`
* Octoprint: upload the plugin file through `Plugin Manager > Get More > ...from URL`
* OctoPrint-PlotlyTempGraph plugin: In the Name Mapping, select name `C`, set any label you want. Note: As of 2/2022, PlotlyTempGraph is incompatible with TouchUI plugin.
* Standard `Temperature` tab: In your printer profile, `Heated Chamber` in `Print bed & build volume` must be checked.


# coding=utf-8
from __future__ import absolute_import
import octoprint.plugin
import octoprint.util
import Adafruit_DHT

#
# Plot enclosure temperature with OctoPrint-PlotlyTempGraph plugin.
#
# Enclosure temperature is measured by a DHT11/DHT22 sensor conhected to the GPIO
# pin defined by the PIN constant below.
#
# Based on https://github.com/jneilliii/OctoPrint-PlotlyTempGraph/blob/master/klipper_additional_temp.py
# Requires https://github.com/adafruit/Adafruit_Python_DHT
#
# Setup:
# - Hardware: https://learn.adafruit.com/dht/connecting-to-a-dhtxx-sensor
# - Raspberry Pi: sudo pip3 install Adafruit_DHT
# - Octoprint: upload this file through Plugin Manager > Get More > ...from URL
#

# GPIO pin connected to DHTXX data pin
GPIO = 23
SENSOR = Adafruit_DHT.DHT22


class DHTEnclosureTemp(octoprint.plugin.StartupPlugin, octoprint.plugin.RestartNeedingPlugin):
	def __init__(self):
		self.last_dht_temp = dict()
		# Be on the safe side (because of clones) and only sample DHTXX every 3 seconds.
		octoprint.util.RepeatedTimer(3.0, self.sample_dht).start()

	def sample_dht(self):
		# Read quickly as possible, skip if error (temperature won't update in the graph)
		humidity, temperature = Adafruit_DHT.read(SENSOR, GPIO)
		if humidity is not None and temperature is not None:
			self.last_dht_temp["Enclosure"] = (temperature, None)

	def dht_temp_callback(self, comm, parsed_temps):
		parsed_temps.update(self.last_dht_temp)
		return parsed_temps

__plugin_name__ = "Enclosure Temperature"
__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_version__ = "0.0.1"
__plugin_implementation__ = DHTEnclosureTemp()
__plugin_hooks__ = {
	"octoprint.comm.protocol.temperatures.received": __plugin_implementation__.dht_temp_callback
}

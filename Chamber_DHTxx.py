# coding=utf-8
from __future__ import absolute_import
import octoprint.plugin
import octoprint.util
import copy
import Adafruit_DHT

#
# Plot chamber temperature in the "Temperature" tab.
#
# Chamber temperature is measured by a DHT11/DHT22 sensor conhected to the GPIO
# pin defined by the PIN constant below.
#
# Standard "Temperature" tab:
# - In your printer profile, "Heated Chamber" in "Print bed & build volume" must be checked.
#
# OctoPrint-PlotlyTempGraph plugin:
# - In the Name Mapping, select name "C", set any label you want.
#   NOTE: As of 2/2022, PlotlyTempGraph is incompatible with TouchUI plugin.
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


class DHTChamberTemp(octoprint.plugin.StartupPlugin, octoprint.plugin.RestartNeedingPlugin):
	def __init__(self):
		self.last_dht_temp = None
		self.platform = Adafruit_DHT.common.get_platform() # Only do it once for speed sake.
		# Be on the safe side (because of clones) and only sample DHTXX every 3 seconds.
		octoprint.util.RepeatedTimer(3.0, self.sample_dht).start()

	def sample_dht(self):
		try:
			humidity, temperature = Adafruit_DHT.read(SENSOR, GPIO, self.platform)
			# Skip if error (it's fine, the temperature just won't update in the graph)
			if humidity is None or temperature is None:
				return
			# Ignore subtle drops in temperature.
			# https://github.com/adafruit/Adafruit_Python_DHT/blob/master/Adafruit_DHT/common.py#L65
			if self.last_dht_temp and temperature - self.last_dht_temp <= -2:
				return
			self.last_dht_temp = temperature
		except:
			pass

	def dht_temp_callback(self, comm, parsed_temps):
		t = copy.deepcopy(parsed_temps)
		if self.last_dht_temp:
			t.update({ "C": (self.last_dht_temp, None) })
		return t


__plugin_name__ = "Chamber Temperature"
__plugin_author__ = "Adriano Cunha"
__plugin_description__ = "Provides chamber temperature in the 'Temperature' tab using a DHTxx sensor."
__plugin_url__ = "https://github.com/adrcunha/OctoPrint-ChamberTempGraph-DHTxx"
__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_version__ = "0.0.1"
__plugin_implementation__ = DHTChamberTemp()
__plugin_hooks__ = {
	"octoprint.comm.protocol.temperatures.received": __plugin_implementation__.dht_temp_callback
}

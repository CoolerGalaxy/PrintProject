# coding = utf-8

from __future__ import absolute_import
import octoprint.plugin
import requests # this will probably go away
from .ServerLogic import ServerLogic

class PrintFarmer(octoprint.plugin.AssetPlugin,
					octoprint.plugin.SettingsPlugin,
					octoprint.plugin.ShutdownPlugin,
					octoprint.plugin.StartupPlugin,
					octoprint.plugin.TemplatePlugin):
					
	def on_after_startup(self):
		
		# this snippet divides each server reboot in the log file for easier viewing
		division = ""
		for x in range(0,150):
			division = division + "="
		self._logger.info(division)
		
		self._logger.info("PrintFarmer Loaded (current site: %s)" % self._settings.get(["server_url"]))
		
		self.server_url = self._settings.get(["server_url"])
		self.server_port = self._settings.get(["server_port"])
		self.printer_name = self._settings.get(["printer_name"])
		

		self.client = ServerLogic(self)
		self._logger.info("STARTING LOOP!")
		self.client.loop()
		self._logger.info("PAST LOOP!")

	def get_template_configs(self):
		return [
			dict(type="navbar", custom_bindings=False),
			dict(type="settings", custom_bindings=False)
		]

	def get_settings_defaults(self):
		return dict(server_url="Enter Server URL Here",
					server_port="Enter Server Port Here",
					printer_name="Enter Printer Name Here")

	def on_settings_save(self, data):
		# This line needs validation to ensure unique printer name
		octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
		
	# asset mixins
	def get_assets(self):
		return dict( js=["js/printfarmer.js"] )

	# update hook
	def get_update_information(self):
		return dict(
			printfarmer=dict(
				displayName="Print Farmer Plugin",
				displayVersion=self._plugin_version,

				# github info
				type="github_release",
				user="CoolerGalaxy",
				repo="OctoPrint-PrintFarmer",
				current=self._plugin_version,
				pip="setup the github" # TODO: create github page to distribute zip
			)
		)
		
	
		
__plugin_name__ = "PrintFarmer"
__plugin_pythoncompat__ = ">=2.7,<4"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = PrintFarmer()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
	}





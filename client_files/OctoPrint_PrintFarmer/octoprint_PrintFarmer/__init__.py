# coding = utf-8

from __future__ import absolute_import
import octoprint.plugin
import requests

class PrintFarmer(octoprint.plugin.AssetPlugin,
					octoprint.plugin.SettingsPlugin,
					octoprint.plugin.ShutdownPlugin,
					octoprint.plugin.StartupPlugin,
					octoprint.plugin.TemplatePlugin):

	def on_after_startup(self):
	
		# this is to more easily see the server restarts in the log file
		division = ""
		for x in range(0,150):
			division = division + "="
		self._logger.info(division)
		
		self._logger.info("PrintFarmer Loaded (current site: %s)" % self._settings.get(["url"]))
		piNeedsHelp = requests.get("http://" + self._settings.get(["url"]) + ":8080/pi", {'Heartbeat': 'true'}) #working
		self._plugin_manager.send_plugin_message(self._identifier, dict(success="Stream stopped"))

	def get_template_configs(self):
		return [
			dict(type="navbar", custom_bindings=False),
			dict(type="settings", custom_bindings=False)
		]

	def get_settings_defaults(self):
		return dict(url="EnterURLHere")

	def on_settings_save(self, data):
		octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
		
	# asset mixin
	def get_assets(self):
		return dict( js=["js/printfarmer.js"] )
		
	# API stuff
	def get_api_commands(self):
		return dict(startStream=[])
		
	def on_api_command(self, command, data):
		if command == 'startStream': # this should be able to bind to some jquery or something
			self.start_stream()

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
		
	#utilities
	def start_stream(self):
		self._plugin_manager.send_plugin_message(self._identifier, dict(success="Stream started"))

__plugin_name__ = "PrintFarmer"
__plugin_pythoncompat__ = ">=2.7,<4"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = PrintFarmer()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
	}





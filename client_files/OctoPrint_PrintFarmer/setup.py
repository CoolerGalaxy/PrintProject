# coding = utf-8
plugin_identifier = "PrintFarmer"
plugin_package = "octoprint_PrintFarmer"
plugin_name = "OctoPrint-PrintFarmer"
plugin_version = "0.0.1"
plugin_description = """Client software to control multiple 3D printers"""
plugin_author = "Jason Morgan"
plugin_author_email = "jmorgan@una.edu"
plugin_url = "github" # TODO: create github page for distribution
plugin_license = "MIT?" # does the license matter?

plugin_requires = ['requests_toolbelt==0.8.0']
plugin_additional_data = []
plugin_additional_packages = []
plugin_ignored_packages = []
additional_setup_parameters = {}

from setuptools import setup

try:
	import octoprint_setuptools
except:
	print("Could not import OctoPrint's setuptools, are you sure you are running that under "
	      "the same python installation that OctoPrint is installed under?")
	import sys
	sys.exit(-1)

setup_parameters = octoprint_setuptools.create_plugin_setup_parameters(
	identifier=plugin_identifier,
	package=plugin_package,
	name=plugin_name,
	version=plugin_version,
	description=plugin_description,
	author=plugin_author,
	mail=plugin_author_email,
	url=plugin_url,
	license=plugin_license,
	requires=plugin_requires,
	additional_packages=plugin_additional_packages,
	ignored_packages=plugin_ignored_packages,
	additional_data=plugin_additional_data
)

if len(additional_setup_parameters):
	from octoprint.util import dict_merge
	setup_parameters = dict_merge(setup_parameters, additional_setup_parameters)

setup(**setup_parameters)
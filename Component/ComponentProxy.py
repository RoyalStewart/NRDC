import binascii
import iso8601
import pytz
import requests
from flask import Flask, jsonify, json, request

# CONFIGURATION
destination =
default = {}
default['Unique Identifier'] =
default['Name'] =
default['Manufacturer'] =
default['Model'] =
default['Serial Number'] =
default['Vendor'] =
default['Supplier'] =
default['Installation Details'] =
default['Wiring Notes'] =
default['Deployment'] =
default['Installation Date'] =
default['Modification Date'] =
default['Last Calibrated Date'] =
default['Creation Date'] =
default['Photo'] =

class Component:

	def __init__(self, JSON = default):
		self.unique = JSON['Unique Identifier']
		self.name = JSON['Name']
		self.creation = JSON['Creation Date']
		self.installation = JSON['Installation Date']
		self.modification = JSON['Modification Date']
		self.calibration = JSON['Last Calibrated Date']
		self.manufacturer = JSON['Manufacturer']
		self.model = JSON['Model']
		self.serial = JSON['Serial Number']
		self.vendor = JSON['Vendor']
		self.supplier= JSON['Supplier']
		self.details= JSON['Installation Details']
		self.wiring = JSON['Wiring Notes']
		self.deployment = JSON['Deployment']
		self.photo = JSON['Photo']

	def ImportJSON(self,JSON):
		self.unique = JSON['Unique Identifier']
		self.name = JSON['Name']
		self.creation = JSON['Creation Date']
		self.installation = JSON['Installation Date']
		self.modification = JSON['Modification Date']
		self.calibration = JSON['Last Calibrated Date']
		self.manufacturer = JSON['Manufacturer']
		self.model = JSON['Model']
		self.serial = JSON['Serial Number']
		self.vendor = JSON['Vendor']
		self.supplier= JSON['Supplier']
		self.details= JSON['Installation Details']
		self.wiring = JSON['Wiring Notes']
		self.deployment = JSON['Deployment']
		self.photo = JSON['Photo']

	def ExportJSON(self):
		out = {}
		out['Unique Identifier'] = self.unique
		out['Name'] = self.name
		out['Manufacturer'] = self.manufacturer
		out['Model'] = self.model
		out['Serial Number'] = self.serial
		out['Vendor'] = self.vendor
		out['Supplier'] = self.supplier
		out['Installation Details'] = self.details
		out['Wiring Notes'] = self.wiring
		out['Deployment'] = self.deployment
		out['Installation Date'] = self.installation
		out['Modification Date'] = self.modification
		out['Last Calibrated Date'] = self.calibration
		out['Creation Date'] = self.creation
		out['Photo'] = self.photo
		return out

class Components:

	def __init__(self, URL = destination):
		self.url = URL

	"""
	Component Proxy for the the NRDC. This proxy handles all calls to the Component Module.
	Function Methods:

	GetAllComponents()
	Description: Sends a GET request to the Component module of the NRDC and returns a JSON of all Components in the NRDC database.

	CreateComponent(JSON)
	Description: Sends a POST request to the Component module of the NRDC, creating the Component specified in the JSON.

	UpdateComponent(JSON)
	Description: Sends a PUT request to the Component module of the NRDC, updating any Component specified in the JSON.

	DeleteComponent(UniqueId)
	Description: Sends a DELETE request to the Component module of the NRDC, deleting the Component with the specified unique identifier.
	"""

	def GetComponent(self,uid):
		sent = requests.get(self.url+ str(uid))
		return sent.json()

	def GetAllComponents(self):

		# Request GET call to Component Module
		sent = requests.get(self.url)
		return sent.json()

	def GetAllComponentsWithDeployment(self,deploymentid):
		sent = requests.get(self.url + "deployment/" + str(deploymentid))
		return sent.json()

	def CreateComponent(self,Component):

		# Request POST method to Component module
		try:

			# Set header
			headers = {'content-type': 'application/json'}

			# Send to module
			sent = requests.post(self.url, data=json.dumps(Component.ExportJSON()), headers=headers)

			# Return success
			print "You have successfully submitted a Component entry"
			return True

		# Catch
		except Exception, e:
			print str(e)
			return False, str(e)

	def UpdateComponent(self,Component):

		# Request POST method to Component module
		try:

			# Set header
			headers = {'content-type': 'application/json'}

			# Send to module
			sent = requests.put(self.url, data=json.dumps(Component.ExportJSON()), headers=headers)

			# Return success
			print "You have successfully submitted an update to Component entry"
			return True

		# Catch
		except Exception, e:
			print str(e)
			return False, str(e)

	def DeleteComponent(self,uid):

		# Try
		try:

			# Send DELETE Request with UniqueID
			sent = requests.delete(self.url + str(uid))
			print "You have successfully sent a DELETE request"
			return True

		# Catch
		except Exception, e:
			print str(e)
			return False, str(e)
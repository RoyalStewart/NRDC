import binascii
import iso8601
import pytz
import requests
from flask import Flask, jsonify, json, request

# CONFIGURATION
destination =
default = {}
default['Details'] =
default['Installation Location'] =
default['Name'] =
default['Power'] =
default['Unique Identifier'] =
default['Manager'] =
default['Creation Date'] =
default['Installation Date'] =
default['Modification Date'] =
default['Photo'] =
default['Site'] =

class System:

	def __init__(self, JSON = default):
		self.unique = JSON['Unique Identifier']
		self.name = JSON['Name']
		self.creation = JSON['Creation Date']
		self.installation = JSON['Installation Date']
		self.modification = JSON['Modification Date']
		self.details = JSON['Details']
		self.location = JSON['Installation Location']
		self.power = JSON['Power']
		self.manager = JSON['Manager']
		self.photo = JSON['Photo']
		self.site = JSON['Site']

	def ImportJSON(self,JSON):
		self.unique = JSON['Unique Identifier']
		self.name = JSON['Name']
		self.creation = JSON['Creation Date']
		self.installation = JSON['Installation Date']
		self.modification = JSON['Modification Date']
		self.details = JSON['Details']
		self.location = JSON['Installation Location']
		self.power = JSON['Power']
		self.manager = JSON['Manager']
		self.photo = JSON['Photo']
		self.site = JSON['Site']

	def ExportJSON(self):
		out = {}
		out['Details'] = self.details
		out['Installation Location'] = self.location
		out['Name'] = self.name
		out['Power'] = self.power
		out['Unique Identifier'] = self.unique
		out['Manager'] = self.manager
		out['Creation Date'] = self.creation
		out['Installation Date'] = self.installation
		out['Modification Date'] = self.modification
		out['Photo'] = self.photo
		out['Site'] = self.site
		return out


class Systems:

	def __init__(self, URL = destination):
		self.url = URL


	"""
	System Proxy for the the NRDC. This proxy handles all calls to the System Module.
	Function Methods:

	GetAllSystems()
	Description: Sends a GET request to the System module of the NRDC and returns a JSON of all Systems in the NRDC database.

	CreateSystem(JSON)
	Description: Sends a POST request to the System module of the NRDC, creating the System specified in the JSON.

	UpdateSystem(JSON)
	Description: Sends a PUT request to the System module of the NRDC, updating any System specified in the JSON.

	Delete(UniqueId)
	Description: Sends a DELETE request to the System module of the NRDC, deleting the System with the specified unique identifier.
	"""

	def GetSystem(self,uid):
		sent = requests.get(self.url+ str(uid))
		return sent.json()

	def GetAllSystems(self):

		# Request GET call to System Module
		sent = requests.get(self.url)
		return sent.json()

	def GetAllSystemsWithSite(self,siteid):

		# Request GET call with siteid included
		sent = requests.get(self.url + "/site/" + str(siteid))
		return sent.json()

	def CreateSystem(self,System):

		# Request POST method to System module
		try:

			# Set header
			headers = {'content-type': 'application/json'}

			# Send to module
			sent = requests.post(self.url, data=json.dumps(System.ExportJSON()), headers=headers)

			# Return success
			print "You have successfully submitted a System entry"
			return True

		# Catch
		except Exception, e:
			print str(e)
			return False, str(e)

	def UpdateSystem(self,System):

		# Request POST method to System module
		try:

			# Set header
			headers = {'content-type': 'application/json'}

			# Send to module
			sent = requests.put(self.url, data=json.dumps(System.ExportJSON()), headers=headers)

			# Return success
			print "You have successfully submitted an update to System entry"
			return True

		# Catch
		except Exception, e:
			print str(e)
			return False, str(e)

	def DeleteSystem(self,uid):

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
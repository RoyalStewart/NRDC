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
default['Date'] =
default['Notes'] =
default['Operation'] =
default['Project'] =
default['Creator'] =
default['System'] =
default['Component'] =
default['Creation Date'] =
default['Modification Date'] =
default['Photo'] =

class ServiceEntry:

	def __init__(self, JSON = default):
		self.unique = JSON['Unique Identifier']
		self.name = JSON['Name']
		self.notes = JSON['Notes']
		self.operation = JSON['Operation']
		self.project = JSON['Project']
		self.creator = JSON['Creator']
		self.system = JSON['System']
		self.component = JSON['Component']
		self.creation = JSON['Creation Date']
		self.modification = JSON['Modification Date']
		self.date = JSON['Date']
		self.photo = JSON['Photo']

	def ImportJSON(self,JSON):
		self.unique = JSON['Unique Identifier']
		self.name = JSON['Name']
		self.notes = JSON['Notes']
		self.operation = JSON['Operation']
		self.project = JSON['Project']
		self.creator = JSON['Creator']
		self.system = JSON['System']
		self.component = JSON['Component']
		self.creation = JSON['Creation Date']
		self.modification = JSON['Modification Date']
		self.date = JSON['Date']
		self.photo = JSON['Photo']

	def ExportJSON(self):
		out = {}
		out['Unique Identifier'] = self.unique
		out['Name'] = self.name
		out['Notes'] = self.notes
		out['Operation'] = self.operation
		out['Project'] = self.project
		out['Creator'] = self.creator
		out['System'] = self.system
		out['Component'] = self.component
		out['Creation Date'] = self.creation
		out['Modification Date'] = self.modification
		out['Date'] = self.date
		out['Photo'] = self.photo
		return out


class ServiceEntries:

	def __init__(self, URL = destination):
		self.url = URL

	"""
	ServiceEntry Proxy for the the NRDC. This proxy handles all calls to the ServiceEntry Module.
	Function Methods:

	GetAllServiceEntries()
	Description: Sends a GET request to the ServiceEntry module of the NRDC and returns a JSON of all ServiceEntries in the NRDC database.

	CreateServiceEntry(JSON)
	Description: Sends a POST request to the ServiceEntry module of the NRDC, creating the ServiceEntry specified in the JSON.

	UpdateServiceEntry(JSON)
	Description: Sends a PUT request to the ServiceEntry module of the NRDC, updating any ServiceEntry specified in the JSON.

	DeleteServiceEntry(UniqueId)
	Description: Sends a DELETE request to the ServiceEntry module of the NRDC, deleting the ServiceEntry with the specified unique identifier.
	"""

	def GetServiceEntry(self,uid):
		sent = requests.get(self.url+ str(uid))
		return sent.json()

	def GetAllServiceEntries(self):

		# Request GET call to ServiceEntry Module
		sent = requests.get(self.url)
		return sent.json()

	def GetAllServiceEntriesWithModules(self,systemid,componentid):

		sent = requests.get(self.url + "system/" + str(systemid) + "/component/" + str(componentid))
		return sent.json()

	def CreateServiceEntry(self,ServiceEntry):

		# Request POST method to ServiceEntry module
		try:

			# Set header
			headers = {'content-type': 'application/json'}

			# Send to module
			sent = requests.post(self.url, data=json.dumps(ServiceEntry.ExportJSON()), headers=headers)

			# Return success
			print "You have successfully submitted a ServiceEntry entry"
			return True

		# Catch
		except Exception, e:
			print str(e)
			return False, str(e)

	def UpdateServiceEntry(self,ServiceEntry):

		# Request POST method to ServiceEntry module
		try:

			# Set header
			headers = {'content-type': 'application/json'}

			# Send to module
			sent = requests.put(self.url, data=json.dumps(ServiceEntry.ExportJSON()), headers=headers)

			# Return success
			print "You have successfully submitted an update to ServiceEntry entry"
			return True

		# Catch
		except Exception, e:
			print str(e)
			return False, str(e)

	def DeleteServiceEntry(self,uid):

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
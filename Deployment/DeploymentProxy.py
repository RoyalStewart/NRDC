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
default['Purpose'] =
default['Center Offset'] =
default['Location'] =
default['Height From Ground'] =
default['Parent Logger'] =
default['Established Date'] =
default['Abandoned Date'] =
default['Creation Date'] =
default['Modification Date'] =
default['System'] =

# Deployment Class
class Deployment:

	def __init__(self, JSON = default):
		self.unique = JSON['Unique Identifier']
		self.name = JSON['Name']
		self.purpose = JSON['Purpose']
		self.centeroffset = JSON['Center Offset']
		self.location = JSON['Location']
		self.heightfromground = JSON['Height From Ground']
		self.parentlogger = JSON['Parent Logger']
		self.establisheddate = JSON['Established Date']
		self.abandoneddate = JSON['Abandoned Date']
		self.creationdate = JSON['Creation Date']
		self.modificationdate = JSON['Modification Date']
		self.system = JSON['System']

	def ImportJSON(self, JSON):
		self.unique = JSON['Unique Identifier']
		self.name = JSON['Name']
		self.purpose = JSON['Purpose']
		self.centeroffset = JSON['Center Offset']
		self.location = JSON['Location']
		self.heightfromground = JSON['Height From Ground']
		self.parentlogger = JSON['Parent Logger']
		self.establisheddate = JSON['Established Date']
		self.abandoneddate = JSON['Abandoned Date']
		self.creationdate = JSON['Creation Date']
		self.modificationdate = JSON['Modification Date']
		self.system = JSON['System']

	def ExportJSON(self):
		export = {}
		export['Unique Identifier'] = self.unique
		export['Name'] = self.name
		export['Purpose'] = self.purpose
		export['Center Offset'] = self.centeroffset
		export['Location'] = self.location
		export['Height From Ground'] = self.heightfromground
		export['Parent Logger'] = self.parentlogger
		export['Established Date'] = self.establisheddate
		export['Abandoned Date'] = self.abandoneddate
		export['Creation Date'] = self.creationdate
		export['Modification Date'] = self.modificationdate
		export['System'] = self.system
		return export

class Deployments:

	def __init__(self, URL = destination):
		self.url = URL

	"""
	Deployment Proxy for the the NRDC. This proxy handles all calls to the Deployment Module.
	Function Methods:

	GetAllDeployments()
	Description: Sends a GET request to the Deployment module of the NRDC and returns a JSON of all Deployments in the NRDC database.

	CreateDeployment(JSON)
	Description: Sends a POST request to the Deployment module of the NRDC, creating the Deployment specified in the JSON.

	UpdateDeployment(JSON)
	Description: Sends a PUT request to the Deployment module of the NRDC, updating any Deployment specified in the JSON.

	Delete(UniqueId)
	Description: Sends a DELETE request to the Deployment module of the NRDC, deleting the Deployment with the specified unique identifier.
	"""

	def GetDeployment(self,uid):
		sent = requests.get(self.url+ str(uid))
		return sent.json()

	def GetAllDeployments(self):

		# Request GET call to Deployment Module
		sent = requests.get(self.url)
		return sent.json()

	def GetAllDeploymentsWithSystem(self,systemid):

		sent = requests.get(self.url + 'system/' + str(systemid))
		return sent.json()

	def CreateDeployment(self,Deployment):

		# Request POST method to Deployment module
		try:

			# Set header
			headers = {'content-type': 'application/json'}

			# Send to module
			sent = requests.post(self.url, data=json.dumps(Deployment.ExportJSON()), headers=headers)

			# Return success
			print "You have successfully submitted a Deployment entry"
			return True

		# Catch
		except Exception, e:
			print str(e)
			return False, str(e)

	def UpdateDeployment(self,Deployment):

		# Request POST method to Deployment module
		try:

			# Set header
			headers = {'content-type': 'application/json'}

			# Send to module
			sent = requests.put(self.url, data=json.dumps(Deployment.ExportJSON()), headers=headers)

			# Return success
			print "You have successfully submitted an update to Deployment entry"
			return True

		# Catch
		except Exception, e:
			print str(e)
			return False, str(e)

	def DeleteDeployment(self,uid):

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
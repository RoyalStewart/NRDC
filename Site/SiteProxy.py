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
default['Notes'] =
default['Alias'] =
default['Location'] =
default['Land Owner'] =
default['Permit Holder'] =
default['Time Zone Name'] =
default['Time Zone Abbreviation'] =	
default['Time Zone Offset'] =
default['Project'] =
default['GPS Landmark'] =
default['Landmark Photo'] =

class Site:

	def __init__(self, JSON = default):
		self.unique = JSON['Unique Identifier']
		self.name = JSON['Name']
		self.notes = JSON['Notes']
		self.alias = JSON['Alias']
		self.location = JSON['Location']
		self.owner = JSON['Land Owner']
		self.permit = JSON['Permit Holder']
		self.zone = JSON['Time Zone Name']
		self.abbreviation = JSON['Time Zone Abbreviation']
		self.offset = JSON['Time Zone Offset']
		self.project = JSON['Project']
		self.landmark = JSON['GPS Landmark']
		self.photo = JSON['Landmark Photo']

	def ImportJSON(self,JSON):
		self.unique = JSON['Unique Identifier']
		self.name = JSON['Name']
		self.notes = JSON['Notes']
		self.alias = JSON['Alias']
		self.location = JSON['Location']
		self.owner = JSON['Land Owner']
		self.permit = JSON['Permit Holder']
		self.zone = JSON['Time Zone Name']
		self.abbreviation = JSON['Time Zone Abbreviation']
		self.offset = JSON['Time Zone Offset']
		self.project = JSON['Project']
		self.landmark = JSON['GPS Landmark']
		self.photo = JSON['Landmark Photo']		

	def ExportJSON(self):
		out = {}
		out['Unique Identifier'] = self.unique
		out['Name'] = self.name
		out['Notes'] = self.notes
		out['Alias'] = self.alias
		out['Location'] = self.location
		out['Land Owner'] = self.owner
		out['Permit Holder'] = self.permit
		out['Time Zone Name'] = self.zone
		out['Time Zone Abbreviation'] = self.abbreviation
		out['Time Zone Offset'] = self.offset
		out['Project'] = self.project
		out['GPS Landmark'] = self.landmark
		out['Landmark Photo'] = self.photo
		return out

class Sites:

	def __init__(self, URL = destination):
		self.url = URL

	"""
	Site Proxy for the the NRDC. This proxy handles all calls to the Site Module. Include the following methods in your application
	to be able to access the Site module. The following function methods will be used.
	Function Methods:

	GetAllSites()
	Description: Sends a GET request to the Site module of the NRDC and returns a JSON of all Site in the NRDC database.

	CreateSite(JSON)
	Description: Sends a POST request to the Site module of the NRDC, creating the Site specified in the JSON.

	UpdateSite(JSON)
	Description: Sends a PUT request to the Site module of the NRDC, updating any Site specified in the JSON.

	DeleteSite(UniqueId)
	Description: Sends a DELETE request to the Site module of the NRDC, deleting the Site with the specified unique identifier.
	"""
	def GetSite(self,uid):
		sent = requests.get(self.url+ str(uid))
		return sent.json()

	def GetAllSites(self):

		# Request GET call to Site Module
		sent = requests.get(self.url)
		return sent.json()

	def CreateSite(self,Site):

		# Request POST method to Site module
		try:

			# Set header
			headers = {'content-type': 'application/json'}

			# Send to module
			sent = requests.post(self.url, data=json.dumps(Site.ExportJSON()), headers=headers)

			# Return success
			print "You have successfully submitted a Site entry"
			return True

		# Catch
		except Exception, e:
			print str(e)
			return False, str(e)

	def UpdateSite(self,Site):

		# Request POST method to Site module
		try:

			# Set header
			headers = {'content-type': 'application/json'}

			# Send to module
			sent = requests.put(self.url, data=json.dumps(Site.ExportJSON()), headers=headers)

			# Return success
			print "You have successfully submitted an update to Site entry"
			return True

		# Catch
		except Exception, e:
			print str(e)
			return False, str(e)

	def DeleteSite(self,uid):

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
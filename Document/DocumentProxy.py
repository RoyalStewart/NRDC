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
default['Path'] =
default['Creation Date'] =
default['Modification Date'] =
default['Project'] =
default['Site'] =
default['Deployment'] =
default['Component'] =
default['Service Entry'] =

# Document Class
class Document:

	def __init__(self,JSON =default):
		self.unique = JSON['Unique Identifier']
		self.name = JSON['Name']
		self.notes = JSON['Notes']
		self.path = JSON['Path']
		self.creationdate = JSON['Creation Date']
		self.modificationdate = JSON['Modification Date']
		self.project = JSON['Project']
		self.site = JSON['Site']
		self.deployment = JSON['Deployment']
		self.component = JSON['Component']
		self.serviceentry = JSON['Service Entry']

	def ImportJSON(self,JSON):
		self.unique = JSON['Unique Identifier']
		self.name = JSON['Name']
		self.notes = JSON['Notes']
		self.path = JSON['Path']
		self.creationdate = JSON['Creation Date']
		self.modificationdate = JSON['Modification Date']
		self.project = JSON['Project']
		self.site = JSON['Site']
		self.deployment = JSON['Deployment']
		self.component = JSON['Component']
		self.serviceentry = JSON['Service Entry']

	def ExportJSON(self):
		export = {}
		export['Unique Identifier'] = self.unique
		export['Name'] = self.name
		export['Notes'] = self.notes
		export['Path'] = self.path
		export['Creation Date'] = self.creationdate
		export['Modification Date'] = self.modificationdate
		export['Project'] = self.project
		export['Site'] = self.site
		export['Deployment'] = self.deployment
		export['Component'] = self.component
		export['Service Entry'] = self.serviceentry
		return export

class Documents:

	def __init__(self, URL = destination):
		self.url = URL

	"""
	Document Proxy for the the NRDC. This proxy handles all calls to the Document Module.
	Function Methods:

	GetAllDocuments()
	Description: Sends a GET request to the Document module of the NRDC and returns a JSON of all Documents in the NRDC database.

	CreateDocument(JSON)
	Description: Sends a POST request to the Document module of the NRDC, creating the Document specified in the JSON.

	UpdateDocument(JSON)
	Description: Sends a PUT request to the Document module of the NRDC, updating any Document specified in the JSON.

	DeleteDocument(UniqueId)
	Description: Sends a DELETE request to the Document module of the NRDC, deleting the Document with the specified unique identifier.
	"""

	def GetDocument(self,uid):
		sent = requests.get(self.url+ str(uid))
		return sent.json()

	def GetAllDocuments(self):

		# Request GET call to Document Module
		sent = requests.get(self.url)
		return sent.json()

	def GetAllDocumentsWithModules(self,siteid,serviceentryid,deploymentid,componentid):
		print "Inside proxy"
		sent = requests.get(self.url + "site/" + str(siteid) + "/service_entry/" + str(serviceentryid) + "/deployment/" + str(deploymentid) + "/component/" + str(componentid))
		return sent.json()

	def CreateDocument(self,Document):

		# Request POST method to Document module
		try:

			# Set header
			headers = {'content-type': 'application/json'}

			# Send to module
			sent = requests.post(self.url, data=json.dumps(Document.ExportJSON()), headers=headers)

			# Return success
			print "You have successfully submitted a Document entry"
			return True

		# Catch
		except Exception, e:
			print str(e)
			return False, str(e)

	def UpdateDocument(self,Document):

		# Request POST method to Document module
		try:

			# Set header
			headers = {'content-type': 'application/json'}

			# Send to module
			sent = requests.put(self.url, data=json.dumps(Document.ExportJSON()), headers=headers)

			# Return success
			print "You have successfully submitted an update to Document entry"
			return True

		# Catch
		except Exception, e:
			print str(e)
			return False, str(e)

	def DeleteDocument(self,uid):

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
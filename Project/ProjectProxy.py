import binascii
import iso8601
import pytz
import requests
from flask import Flask, jsonify, json, request

# CONFIGURATION
destination = 
default = {}
default['Institution Name'] = 
default['Grant Number String'] = 
default['Unique Identifier'] =
default['Name'] =
default['Principal Investigator'] = 
default['Original Funding Agency'] = 
default['Modification Date'] =
default['Creation Date'] =
default['Started Date'] =

class Project:

	def __init__(self, JSON = default):
		try:
			self.unique = JSON['Unique Identifier']
			self.name = JSON['Name']
			self.funding = JSON['Original Funding Agency']
			self.investigator = JSON['Principal Investigator']
			self.creation = JSON['Creation Date']
			self.started = JSON['Started Date']
			self.modification = JSON['Modification Date']
			self.institution = JSON['Institution Name']
			self.grant = JSON['Grant Number String']
		# Catch
		except Exception, e:
			print str(e)
			return False, str(e)


	def ImportJSON(self, JSON):
		self.unique = JSON['Unique Identifier']
		self.name = JSON['Name']
		self.funding = JSON['Original Funding Agency']
		self.investigator = JSON['Principal Investigator']
		self.creation = JSON['Creation Date']
		self.started = JSON['Started Date']
		self.modification = JSON['Modification Date']
		self.institution = JSON['Institution Name']
		self.grant = JSON['Grant Number String']

	def ExportJSON(self):
		out = {}
		out['Institution Name'] = self.institution
		out['Grant Number String'] = self.grant
		out['Unique Identifier'] = self.unique
		out['Name'] = self.name
		out['Principal Investigator'] = self.investigator
		out['Original Funding Agency'] = self.funding
		out['Modification Date'] = self.modification
		out['Creation Date'] = self.creation
		out['Started Date'] = self.started
		return out

class Projects:

	def __init__(self, URL = destination):
		self.url = URL

	"""
	Project Proxy for the the NRDC. This proxy handles all calls to the Project Module. Include the following methods in your application
	to be able to access the Project module. The following function methods will be used.
	Function Methods:

	GetAllProjects()
	Description: Sends a GET request to the Project module of the NRDC and returns a JSON of all Project in the NRDC database.

	CreateProject(JSON)
	Description: Sends a POST request to the Project module of the NRDC, creating the Project specified in the JSON.

	UpdateProject()
	Description: Sends a PUT request to the Project module of the NRDC, updating any Project specified in the JSON.

	DeleteProject()
	Description: Sends a DELETE request to the Project module of the NRDC, deleting the Project with the specified unique identifier.
	"""

	def GetProject(self,uid):
		sent = requests.get(self.url+ str(uid))
		return sent.json()

	def GetAllProjects(self):

		# Request GET call to Project Module
		sent = requests.get(self.url)
		return sent.json()

	def CreateProject(self,Project):

		# Request POST method to Project module
		try:

			# Set header
			headers = {'content-type': 'application/json'}

			# Send to module
			sent = requests.post(self.url, data=json.dumps(Project.ExportJSON()), headers=headers)

			# Return success
			print "You have successfully submitted a Project entry"
			return True

		# Catch
		except Exception, e:
			print str(e)
			return False, str(e)

	def UpdateProject(self,Project):

		# Request POST method to Project module
		try:

			# Set header
			headers = {'content-type': 'application/json'}

			# Send to module
			sent = requests.put(self.url, data=json.dumps(Project.ExportJSON()), headers=headers)

			# Return success
			print "You have successfully submitted an update to Project entry"
			return True

		# Catch
		except Exception, e:
			print str(e)
			return False, str(e)

	def DeleteProject(self,uid):

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
import sys
sys.path.append("..")
import binascii
import iso8601
import pytz
import requests
from flask import Flask, jsonify, json, request

# CONFIGURATION
destination =
default = {}
default['Unique Identifier'] =
default['First Name'] = 
default['Last Name'] = 
default['Phone'] =
default['Email'] = 
default['Organization'] = 
default['Creation Date'] = 
default['Modification Date'] =
default['Photo'] =

class Person:

	def __init__(self, JSON = default):
		self.unique = JSON['Unique Identifier']
		self.first = JSON['First Name']
		self.last = JSON['Last Name']
		self.phone = JSON['Phone']
		self.email = JSON['Email']
		self.organization = JSON['Organization']
		self.creation = JSON['Creation Date']
		self.modification = JSON['Modification Date']
		self.photo = JSON['Photo']

	def ImportJSON(self,JSON):
		self.unique = JSON['Unique Identifier']
		self.first = JSON['First Name']
		self.last = JSON['Last Name']
		self.phone = JSON['Phone']
		self.email = JSON['Email']
		self.organization = JSON['Organization']
		self.creation = JSON['Creation Date']
		self.modification = JSON['Modification Date']
		self.photo = JSON['Photo']

	def ExportJSON(self):
		out = {}
		out['Unique Identifier'] = self.unique
		out['First Name'] = self.first
		out['Last Name'] = self.last
		out['Phone'] = self.phone
		out['Email'] = self.email
		out['Organization'] = self.organization
		out['Creation Date'] = self.creation
		out['Modification Date'] = self.modification
		out['Photo'] = self.photo
		return out


class People:

	def __init__(self, URL = destination):
		self.url = URL

	"""
	GetAllPeople()
	Description: Sends a GET request to the Person module of the NRDC and returns a JSON of all people in the NRDC database.

	CreatePerson(JSON)
	Description: Sends a POST request to the Person module of the NRDC, creating the person specified in the JSON.

	UpdatePerson(JSON)
	Description: Sends a PUT request to the Person module of the NRDC, updating any person specified in the JSON.

	DeletePerson(UniqueId)
	Description: Sends a DELETE request to the Person module of the NRDC, deleting the person with the specified unique identifier.
	"""
	def GetPerson(self,uid):
		sent = requests.get(self.url+ str(uid))
		return sent.json()

	def GetAllPeople(self):

		# Request GET call to Person Module
		sent = requests.get(self.url)
		return sent.json()

	def CreatePerson(self,Person):

		# Request POST method to Person module
		try:

			# Set header
			headers = {'content-type': 'application/json'}

			# Send to module
			sent = requests.post(self.url, data=json.dumps(Person.ExportJSON()), headers=headers)

			# Return success
			return True

		# Catch
		except Exception, e:
			print str(e)
			return False, str(e)

	def UpdatePerson(self,Person):

		# Request POST method to Person module
		try:

			# Set header
			headers = {'content-type': 'application/json'}

			# Send to module
			sent = requests.put(self.url, data=json.dumps(Person.ExportJSON()), headers=headers)

			# Return success
			return True

		# Catch
		except Exception, e:
			print str(e)
			return False, str(e)

	def DeletePerson(self,uid):

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
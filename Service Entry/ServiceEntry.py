import sys
sys.path.append("..")
from flask import Flask, jsonify, json, request
from flask.ext.cors import cross_origin
from Module_Classes_1 import DisplayServiceEntry
import pyodbc
import binascii
import iso8601
import pytz

app = Flask(__name__)

# CONFIGURATION
# Convert Datetime Function
def convertdatetime(timevalue):
	parsevalue = iso8601.parse_date(timevalue)
	correcttime = parsevalue.astimezone(pytz.utc)
	correcttime = str(correcttime)
	correcttime = correcttime.split("+")
	correcttime = correcttime[0]
	correcttime = correcttime.replace(' ', 'T')
	correcttime = correcttime[:-3]
	return correcttime

# Convert Photo Function
def convertphoto(Photovalue):
	correctPhoto = binascii.a2b_base64(Photovalue)
	correctPhoto = correctPhoto.encode("ISO-8859-1")
	return correctPhoto

# View for All
@app.route('/service_entries/')
@cross_origin()
def index():
	try:
		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected to VIEW ALL"

		# Table Creation Section
		cursor = cnxn.cursor()

		# Create array of service entries
		service_entries = []

		# Database call
		cursor.execute("SELECT [Service Entry], [Unique Identifier], Name, Notes, Date, Operation, [Creation Date], [Modification Date], Project, Creator, System, Component, \
		Photo FROM [Infrastructure].[Service Entries]")

		# Grab the information for the first deployment
		entry = cursor.fetchone()

		# Iterate while there is information in the deployments object
		while entry is not None:

			# Decode Photo
			if entry[12] is not None:

				# Set Value to Binary Array
				entry[12] = binascii.a2b_base64(entry[12])

			# Create a new Service Entry from the class with the data from the database
			newentry = DisplayServiceEntry(entry[0],entry[1],entry[2],entry[3],entry[4],entry[5],entry[6], entry[7], entry[8], entry[9], entry[10], entry[11], entry[12])

			# Add it to Service Entry array
			service_entries.append(newentry)

			# Grab the next Service Entry
			entry = cursor.fetchone()
	
		# Return the Service Entry JSON
		return jsonify(ServiceEntries = [se.serialize() for se in service_entries])

	except Exception, e:
		print str(e)
		return False, str(e)

# View for Specific
@app.route('/service_entries/<serviceentry_id>')
def specific(serviceentry_id):
	try:
		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected to VIEW SPECIFIC"

		# Table Creation Section
		cursor = cnxn.cursor()

		# Database call
		cursor.execute("SELECT [Service Entry], [Unique Identifier], Name, Notes, Date, Operation, [Creation Date], [Modification Date], Project, Creator, System, Component, \
		Photo FROM [Infrastructure].[Service Entries] WHERE [Unique Identifier] = ?", serviceentry_id)

		# Grab the information for the first person
		service_entry = cursor.fetchone()

		# Decode Photo
		if entry[12] is not None:

			# Set Photo Value to Binary Array
			entry[12] = binascii.a2b_base64(entry[12])

		# Create a new person from the class with the data from the database
		new_service_entry = DisplayServiceEntry(entry[0],entry[1],entry[2],entry[3],entry[4],entry[5],entry[6], entry[7], entry[8], entry[9], entry[10], entry[11], entry[12])

		# Return information
		return jsonify(new_service_entry.serialize()) 

	except Exception, e:
		print str(e)
		return False, str(e)

# Service Entries From Modules
@app.route('/service_entries/system/<systemid>/component/<componentid>')
def serviceentriesfrommodules(systemid,componentid):
	try:
		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected to VIEW FROM MODULES"

		# Table Creation Section
		cursor = cnxn.cursor()

		# Database call
		cursor.execute("SELECT [Service Entry], [Unique Identifier], Name, Notes, Date, Operation, [Creation Date], [Modification Date], Project, Creator, System, Component, \
		Photo FROM [Infrastructure].[Service Entries] WHERE [System] = ? AND [Component] = ?",systemid,componentid)

		# Create array of service entries
		service_entries = []

		# Grab the information for the first person
		service_entry = cursor.fetchone()

		# Iterate while there is information in the deployments object
		while service_entry is not None:

			# Decode Photo
			if service_entry[12] is not None:

				# Set Value to Binary Array
				service_entry[12] = binascii.a2b_base64(service_entry[12])

			# Create a new Service Entry from the class with the data from the database
			newentry = DisplayServiceEntry(service_entry[0],service_entry[1],service_entry[2],service_entry[3],service_entry[4],service_entry[5],service_entry[6],service_entry[7],service_entry[8],service_entry[9],service_entry[10],service_entry[11],service_entry[12])

			# Add it to Service Entry array
			service_entries.append(newentry)

			# Grab the next Service Entry
			service_entry = cursor.fetchone()
	
		# Return the Service Entry JSON
		return jsonify(ServiceEntries = [se.serialize() for se in service_entries])

	except Exception, e:
		print str(e)
		return False, str(e)

# Create Service Entry
@app.route('/service_entries/', methods=['POST'])
def create():
	try:
		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are now successfully connected to CREATE SERVICE ENTRY"

		# Table Creation Section
		cursor = cnxn.cursor()

		# Grab JSON from the request
		try:	
			JSON = request.get_json()
		except Exception as e:
			print "assignment failed"
			print e

		# Grab values from the JSON
		Uniqueid = JSON['Unique Identifier']
		Name = JSON['Name']
		Notes = JSON['Notes']
		Date = JSON['Date']
		Operation = JSON['Operation']
		CreationDate = JSON['Creation Date']
		ModificationDate = JSON['Modification Date']
		Project = JSON['Project']
		Creator = JSON['Creator']
		System = JSON['System']
		Component = JSON['Component']
		Photo = JSON['Photo']
		
		# Type Checking
		try:

			# Photo
			if Photo is None: 
				Photo = pyodbc.BinaryNull
			elif type(Photo) is str:
				Photo = convertphoto(Photo)
			else:
				print "Invalid Photo Type : Must be a base64 string"
				raise Exception

			# Date
			if convertdatetime(Date):
				Date = convertdatetime(Date)
			else:
				print "Invalid Date Type: Must be a Datetime string"
				raise Exception

			# Creation Date
			if convertdatetime(CreationDate):
				CreationDate = convertdatetime(CreationDate)
			else:
				print "Invalid Creation Date Type : Must be a Datetime string"
				raise Exception

			# Modification Date
			if convertdatetime(ModificationDate):
				ModificationDate = convertdatetime(ModificationDate)
			else:
				print "Invalid Modification Date Type : Must be a Datetime string"
				raise Exception

		except Exception, e:
			print str(e)
			return False, str(e)
			
		# UpDate user information from the JSON
		cursor.execute("INSERT INTO [Infrastructure].[Service Entries] ([Unique Identifier], Name, Notes, Date, Operation, [Creation Date], [Modification Date], Project, Creator, System, Component, \
		Photo) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", Uniqueid, Name, Notes, Date, Operation, CreationDate, ModificationDate, Project, Creator, System, Component, Photo)

		# Commit
		cnxn.commit()

		# Return success
		return "Successfully Created"

	except Exception, e:
		print str(e)
		return False, str(e)

# UpDate Service Entry
@app.route('/service_entries/', methods=['PUT'])
def update():
	try:
		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are now successfully connected"

		# Table Creation Section
		cursor = cnxn.cursor()

		# Grab JSON from the request
		try:	
			JSON = request.get_json()
		except Exception as e:
			print "assignment failed"
			print e

		# Grab values from the JSON
		Uniqueid = JSON['Unique Identifier']
		Name = JSON['Name']
		Notes = JSON['Notes']
		Date = JSON['Date']
		Operation = JSON['Operation']
		CreationDate = JSON['Creation Date']
		ModificationDate = JSON['Modification Date']
		Project = JSON['Project']
		Creator = JSON['Creator']
		System = JSON['System']
		Component = JSON['Component']
		Photo = JSON['Photo']
		
		# Type Checking
		try:

			# Photo
			if Photo is None: 
				Photo = pyodbc.BinaryNull
			elif type(Photo) is str:
				Photo = convertphoto(Photo)
			else:
				print "Invalid Photo Type : Must be a base64 string"
				raise Exception

			# Date
			if convertdatetime(Date):
				Date = convertdatetime(Date)
			else:
				print "Invalid Date Type: Must be a Datetime string"
				raise Exception

			# Creation Date
			if convertdatetime(CreationDate):
				CreationDate = convertdatetime(CreationDate)
			else:
				print "Invalid Creation Date Type : Must be a Datetime string"
				raise Exception

			# Modification Date
			if convertdatetime(ModificationDate):
				ModificationDate = convertdatetime(ModificationDate)
			else:
				print "Invalid Modification Date Type : Must be a Datetime string"
				raise Exception

		except Exception, e:
			print str(e)
			return False, str(e)

		# UpDate user information from the JSON
		cursor.execute("UPDate [Infrastructure].[Service Entries] SET [Unique Identifier] = ?, [Name] = ?, [Notes] = ?, [Date] = ?, [Operation] = ?, [Creation Date] = ?, [Modification Date] = ?, \
		[Project] = ?, [Creator] = ?, [Component] = ?, Photo = ? WHERE [Unique Identifier]= ?", Uniqueid, Name, Notes, Date, Operation, CreationDate, ModificationDate, Project, Creator, System, Component, Photo, Uniqueid)

		# Commit
		cnxn.commit()

		# Return success
		return "Successfully UpDated"

	except Exception, e:
		print str(e)
		return False, str(e)

# Delete Service Entry
@app.route('/service_entries/<serviceentry_id>', methods=['DELETE'])
def delete(serviceentry_id):
	try:
		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "Connected"

		# Table Creation Section
		cursor = cnxn.cursor()

		# Delete found user
		cursor.execute("DELETE from [Infrastructure].[Service Entries] WHERE [Unique Identifier] = ?", serviceentry_id)

		# Commit
		cnxn.commit()	

		# Return the json (testing purposes)
		return "Successfully Deleted"

	except Exception, e:
		print str(e)
		return False, str(e)

# Run Main
if __name__ == '__main__':
	app.debug = False
	app.run(host='127.0.0.1', port=8084)

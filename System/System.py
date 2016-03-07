import sys
sys.path.append("..")
from flask import Flask, jsonify, json, request
from flask.ext.cors import cross_origin
from Module_Classes_1 import DisplaySystem
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
def convertPhoto(Photovalue):
	correctPhoto = binascii.a2b_base64(Photovalue)
	correctPhoto = correctPhoto.encode("ISO-8859-1")

# View for All
@app.route('/systems/')
@cross_origin()
def index():
	try:

		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected now"

		# Table Creation Section
		cursor = cnxn.cursor()

		# Create array of Project
		Systems = []

		# Database call of first, last, and email from the PROJECT table
		cursor.execute("SELECT System, [Unique Identifier], Name, Details, Power, [Installation Date], [Installation Location], [Creation Date], [Modification Date], \
		Manager, Site, Photo FROM Infrastructure.Systems")

		# Grab the information for the first person
		System = cursor.fetchone()

		# Iterate while there is information in the person object
		while System is not None:

			# Decode Photo
			if System[11] is not None:

				# Convert to a binary array
				System[11] = binascii.a2b_base64(System[11]) 

			# Create a new person from the class with the data from the database
			newSystem = DisplaySystem(System[0],System[1],System[2],System[3],System[4],System[5],System[6],System[7],System[8],System[9],System[10],System[11])

			# Add it to Project array
			Systems.append(newSystem)

			# Grab the next person
			System = cursor.fetchone()
	
		# Return the Project JSON
		return jsonify(Systems = [s.serialize() for s in Systems])

	except Exception, e:
		print str(e)
		return False, str(e)

# View for Specific
@app.route('/systems/<System_id>')
@cross_origin()
def specific(System_id):
	try:

		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected now"

		# Table Creation Section
		cursor = cnxn.cursor()

		# Database call of first, last, and email from the PROJECT table
		cursor.execute("SELECT System, [Unique Identifier], Name, Details, Power, [Installation Date], [Installation Location], [Creation Date], [Modification Date], \
		Manager, Site, Photo FROM Infrastructure.Systems WHERE [Unique Identifier] = ?", System_id)

		# Grab the information for the first person
		System = cursor.fetchone()

		# Convert Photo
		if System[11] is not None:

			# Convert to a binary array
			System[11] = binascii.a2b_base64(System[11]) 

		# Create a new person from the class with the data from the database
		newSystem = DisplaySystem(System[0],System[1],System[2],System[3],System[4],System[5],System[6],System[7],System[8],System[9],System[10],System[11])

		# Return JSON
		return jsonify(newSystem.serialize())

	except Exception, e:
		print str(e)
		return False, str(e)

# View Systems From A Site
@app.route('/systems/site/<Site_id>', methods=['GET'])
def systemsofsite(Site_id):
	try:

		# Connect to database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected"

		# Table Creation Section
		cursor = cnxn.cursor()

		# Database call of all systems that include the Site_id
		cursor.execute("SELECT System, [Unique Identifier], Name, Details, Power, [Installation Date], [Installation Location], [Creation Date], [Modification Date], \
		Manager, Site, Photo FROM Infrastructure.Systems WHERE [Site] = ?", Site_id)

		# Create array of Project
		Systems = []

		# Grab the information for the first system
		System = cursor.fetchone()

		# Iterate while there is information in the person object
		while System is not None:

			# Decode Photo
			if System[11] is not None:

				# Convert to a binary array
				System[11] = binascii.a2b_base64(System[11]) 

			# Create a new person from the class with the data from the database
			newSystem = DisplaySystem(System[0],System[1],System[2],System[3],System[4],System[5],System[6],System[7],System[8],System[9],System[10],System[11])

			# Add it to Project array
			Systems.append(newSystem)

			# Grab the next person
			System = cursor.fetchone()

		# Return the Project JSON
		return jsonify(Systems = [s.serialize() for s in Systems])

	except Exception, e:
		print str(e)
		return False, str(e)

# Create System
@app.route('/systems/', methods=['POST'])
def create():
	try:

		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected now"

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
		Detail = JSON['Details']
		Power = JSON['Power']
		InstallationDate = JSON['Installation Date']
		InstallationLocation = JSON['Installation Location']
		CreationDate = JSON['Creation Date']
		ModificationDate = JSON['Modification Date']
		Manager = JSON['Manager']
		Site = JSON['Site']
		Photo = JSON['Photo']

		# Type Checking
		try:

			# Photo
			if Photo is None: 
				Photo = pyodbc.BinaryNull
			elif type(Photo) is str:
				Photo = convertPhoto(Photo)
			else:
				print "Invalid Photo Type : Must be a base64 string"
				raise Exception

			# Installation Date
			if convertdatetime(InstallationDate):
				InstallationDate = convertdatetime(InstallationDate)
			else:
				print "Invalid Installation Date Type : Must be a datetime string"
				raise Exception

			# Creation Date
			if convertdatetime(CreationDate):
				CreationDate = convertdatetime(CreationDate)
			else:
				print "Invalid Creation Date Type : Must be a datetime string"
				raise Exception

			# Modification Date
			if convertdatetime(ModificationDate):
				ModificationDate = convertdatetime(ModificationDate)
			else:
				print "Invalid Modification Date Type : Must be a datetime string"
				raise Exception

		except Exception, e:
			print str(e)
			return False, str(e)

		# Update user information from the JSON
		cursor.execute("INSERT INTO Infrastructure.Systems ([Unique Identifier], [Name], [Details], [Power], [Installation Date], [Installation Location], [Creation Date], [Modification Date], \
		[Manager], [Site], [Photo]) VALUES (?,?,?,?,?,?,?,?,?,?,?)", Uniqueid, Name, Detail, Power, InstallationDate, InstallationLocation, CreationDate, ModificationDate, Manager, Site, Photo)

		# Commit
		cnxn.commit()

		# Return success
		return "Successfully Created"

	except Exception, e:
		print str(e)
		return False, str(e)


# Update System
@app.route('/systems/', methods=['PUT'])
def update():
	try:

		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected now"

		# Table Creation Section
		cursor = cnxn.cursor()

		# Grab JSON from the request
		try:	
			JSON = request.get_json()
			print "Got JSON"
		except Exception as e:
			print "assignment failed"
			print e
	
		# Grab values from the JSON
		System = JSON['System']
		Uniqueid = JSON['Unique Identifier']
		Name = JSON['Name']
		Detail = JSON['Details']
		Power = JSON['Power']
		InstallationDate = JSON['Installation Date']
		InstallationLocation = JSON['Installation Location']
		CreationDate = JSON['Creation Date']
		ModificationDate = JSON['Modification Date']
		Manager = JSON['Manager']
		Site = JSON['Site']
		Photo = JSON['Photo']

		# Type Checking
		try:

			# Photo
			if Photo is None: 
				Photo = pyodbc.BinaryNull
			elif type(Photo) is str:
				Photo = convertPhoto(Photo)
			else:
				print "Invalid Photo Type : Must be a base64 string"
				raise Exception

			# Installation Date
			if convertdatetime(InstallationDate):
				InstallationDate = convertdatetime(InstallationDate)
			else:
				print "Invalid Installation Date Type : Must be a datetime string"
				raise Exception

			# Creation Date
			if convertdatetime(CreationDate):
				CreationDate = convertdatetime(CreationDate)
			else:
				print "Invalid Creation Date Type : Must be a datetime string"
				raise Exception

			# Modification Date
			if convertdatetime(ModificationDate):
				ModificationDate = convertdatetime(ModificationDate)
			else:
				print "Invalid Modification Date Type : Must be a datetime string"
				raise Exception

		except Exception, e:
			print str(e)
			return False, str(e)

		# Update user information from the JSON
		cursor.execute("UPDATE Infrastructure.Systems SET, [Unique Identifier] = ?, [Name] = ?, [Details] = ?, [Power] = ?, [Installation Date] = ?, [Installation Location] = ?, [Creation Date] = ?, \
		[Modification Date] = ?, [Manager] = ?, [Site] = ?, [Photo] = ? WHERE [Unique Identifier] = ?", Uniqueid, Name, Detail, Power, InstallationDate, InstallationLocation, CreationDate, ModificationDate, Manager, Site, Photo, Uniqueid)

		# Commit
		cnxn.commit()

		# Return success
		return "Successfully Updated"

	except Exception, e:
		print str(e)
		return False, str(e)


# Delete System
@app.route('/systems/<System_id>', methods=['DELETE'])
def delete(System_id):
	try:

		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected now"

		# Table Creation Section
		cursor = cnxn.cursor()

		# Delete found user
		cursor.execute("DELETE FROM Infrastructure.Systems WHERE [Unique Identifier] = ?", System_id)

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
	app.run(host='127.0.0.1', port=8083)
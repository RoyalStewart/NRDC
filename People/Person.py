import sys
sys.path.append("..")
from flask import Flask, jsonify, json, request
from flask.ext.cors import cross_origin
from Module_Classes_1 import DisplayPerson
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

# View for All
@app.route('/people/')
@cross_origin()
def index():
	try:
		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected now"

		# Table Creation Section
		cursor = cnxn.cursor()

		# Create array of people
		people = []

		# Database call of first, last, and email from the PERSON table
		cursor.execute("SELECT Person, [Unique Identifier], [First Name], [Last Name], Phone, Email, Organization, [Creation Date], [Modification Date], Photo FROM Infrastructure.People")

		# Grab the information for the first person
		person = cursor.fetchone()

		# Iterate while there is information in the person object
		while person is not None:

			if person[9] is not None: # <-----------------Updates

				person[9] = binascii.a2b_base64(person[9]) # <-----------------Updates

			# Create a new person from the class with the data from the database
			newperson = DisplayPerson(person[0],person[1],person[2],person[3],person[4],person[5],person[6], person[7], person[8],person[9])

			# Add it to people array
			people.append(newperson)

			# Grab the next person
			person = cursor.fetchone()
	
		# Return the People JSON
		return jsonify(People = [p.serialize() for p in people])
	except Exception, e:
		print str(e)
		return str(e)

# View for Specific
@app.route('/people/<person_id>')
def specific(person_id):
	try:
		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected now"

		# Table Creation Section
		cursor = cnxn.cursor()

		# Database call of first, last, and email from the PERSON table
		cursor.execute("SELECT Person, [Unique Identifier], [First Name], [Last Name], Phone, Email, Organization, [Creation Date], [Modification Date], Photo \
		from Infrastructure.People WHERE [Unique Identifier] = ?", person_id)

		# Grab the information for the first person
		person = cursor.fetchone()

		# Decode Photo
		if person[9] is not None: # <-----------------Updates

			person[9] = binascii.a2b_base64(person[9]) # <-----------------Updates

		# Create a new person from the class with the data from the database
		newperson = DisplayPerson(person[0],person[1],person[2],person[3],person[4],person[5],person[6],person[7],person[8],person[9])

		# Return information
		return jsonify(newperson.serialize()) 

	except Exception, e:
		print str(e)
		return str(e)

# Create Person
@app.route('/people/', methods=['POST'])
def create():
	try:
		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected now'"

		# Table Creation Section
		cursor = cnxn.cursor()

		# Grab JSON from the request
		try:	
			JSON = request.get_json()
		except Exception as e:
			print "assignment failed"
			print e

		# Grab values from the JSON
		UniqueID = JSON['Unique Identifier']
		FirstName = JSON['First Name']
		LastName =	JSON['Last Name']
		Phone = JSON['Phone']
		Email = JSON['Email']
		Organization = JSON['Organization']
		CreationDate = JSON['Creation Date']
		ModificationDate = JSON['Modification Date']
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
		cursor.execute("INSERT INTO Infrastructure.People ([Unique Identifier], [First Name], [Last Name], Phone, Email, Organization, [Creation Date], [Modification Date], Photo)\
		VALUES (?,?,?,?,?,?,?,?,?)", UniqueID, FirstName, LastName, Phone, Email, Organization, CreationDate, ModificationDate, Photo)

		# Commit
		cnxn.commit()

		# Return success
		return "Successfully Created"

	except Exception, e:
		print str(e)
		return str(e)

# Update Person
@app.route('/people/', methods=['PUT'])
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
		except Exception as e:
			print "assignment failed"
			print e
			return False, str(e)

		# Grab values from the JSON
		UniqueID = JSON['Unique Identifier']
		FirstName = JSON['First Name']
		LastName =	JSON['Last Name']
		Phone = JSON['Phone']
		Email = JSON['Email']
		Organization = JSON['Organization']
		CreationDate = JSON['Creation Date']
		ModificationDate = JSON['Modification Date']
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
		cursor.execute("UPDATE Infrastructure.People SET [Unique Identifier] = ?, [First Name] = ?, [Last Name] = ?, [Phone] = ?, Email = ?, [Organization] = ?, [Creation Date] = ?, \
		[Modification Date] = ?, [Photo] = ? WHERE [Unique Identifier] = ?", UniqueID, FirstName, LastName, Phone, Email, Organization, CreationDate, ModificationDate, Photo, UniqueID)

		# Commit
		cnxn.commit()

		# Return success
		return "Successfully Updated"

	except Exception, e:
		print str(e)
		return False, str(e)

# Delete Project
@app.route('/people/<person_id>', methods=['DELETE'])
def delete(person_id):
	try:
		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected now"

		# Table Creation Section
		cursor = cnxn.cursor()

		# Delete found user
		cursor.execute("DELETE FROM Infrastructure.People WHERE [Unique Identifier] = ?", person_id)

		# Commit
		cnxn.commit()	

		# Return the json (testing purposes)
		return "Successfully Deleted"

	except Exception, e:
		print str(e)
		return str(e)

# View Projects from a Person
@app.route('/people/<person_id>/projects/')
def projectrelation(person_id):
	try:
		# Connect to Test database
		cnxn = pyodbc.connect("DSN=ASGARD-LOKI;DATABASE=NRDC;UID=SENSOR\\royals;PWD=Sl@yer23")
		print "You are successfully connected now, man"

		# Table Creation Section
		cursor = cnxn.cursor()

		# Create projects array
		projects = []

		# Join the Project, People, and the PeopleProjectRelation tables and get first project
		cursor.execute("SELECT Projects.Project, Projects.Name, Projects.[Creation Date], Projects.[Grant Number], Projects.[Institution Name],Projects.[Modification Date], Projects.[Original Funding Agency], Projects.[Started Date], \
		FROM PeopleProjectRelation AS R\
		JOIN Projects AS Projects ON R.Project = Projects.Project\
		JOIN People AS People ON R.Person = People.Person\
		WHERE R.Person = ?", person_id)
		project = cursor.fetchone()

		# Itterate through projects
		while project is not None:

			# Serialize new project
			project = displayProject(project[0],project[1],project[2],project[3],project[4],project[5],project[6])

			# Append
			projects.append(project)

			# Grab next project
			project = cursor.fetchone()

		# Return
		return jsonify(Projects = [p.serialize() for p in projects])

	except Exception, e:
		print str(e)
		return str(e)

# People Systems Relation
@app.route('/people/<person_id>/systems/')
def systemrelation(person_id):
	try:
		# Connect to Test database
		cnxn = pyodbc.connect("DSN=ASGARD-LOKI;DATABASE=NRDC;UID=SENSOR\\royals;PWD=Sl@yer23")
		print "You are successfully connected now, man"

		# Table Creation Section
		cursor = cnxn.cursor()

		# Create systems array
		systems = []

		# Join the People, Systems and the PeopleSystemRelation tables and get first project
		cursor.execute("SELECT Systems.System, Systems.[Creation Date], Systems.Name, Systems.Details, Systems.[Modification Date], Systems.[Installation Date], Systems.[Installation Location] \
		Systems.Latitude, Systems.Longitude, Systems.Photo, Systems.Power \
		FROM PeopleSystemRelation AS R\
		JOIN Systems AS Systems ON R.Systems = Systems.System\
		JOIN People AS People ON R.Person = People.Person\
		WHERE R.Person = ?", person_id)
		system = cursor.fetchone()

		# Itterate through system
		while system is not None:

			# Serialize new project
			system = displaySystem(system[0],system[1],system[2],system[3],system[4],system[5],system[6],system[7],system[8],system[9],system[10])

			# Append
			systems.append(system)

			# Grab next project
			system = cursor.fetchone()

		# Return
		return jsonify(Systems = [s.serialize() for s in systems])

	except Exception, e:
		print str(e)
		return str(e)

# People Service Entries Relation
@app.route('/people/<person_id>/service_entries/')
def servicerelation(person_id):
	try:
		# Connect to Test database
		cnxn = pyodbc.connect("DSN=ASGARD-LOKI;DATABASE=NRDC;UID=SENSOR\\royals;PWD=Sl@yer23")
		print "You are successfully connected now, man"

		# Table Creation Section
		cursor = cnxn.cursor()

		# Create service entries array
		service_entries = []

		# Join the People, Service Entries and the PeopleServiceEntriesRelation tables and get first service entry
		cursor.execute("SELECT [Service Entries].[Service Entry], [Service Entries].[Creation Date], [Service Entries].Date, \
		[Service Entries].Name, [Service Entries].[Modification Date], [Service Entries].Notes, \
		[Service Entries].Operation, [Service Entries].Photo \
		FROM PeopleServiceEntriesRelation AS R\
		JOIN [Service Entries] AS Service Entries ON R.[Service Entries] = [Service Entries].[Service Entry]\
		JOIN People AS People ON R.Person = People.Person\
		WHERE R.Person = ?", person_id)
		service_entry = cursor.fetchone()

		# Itterate through service entry
		while service_entry is not None:

			# Serialize new service entry
			service_entry = displaySystem(service_entry[0],service_entry[1],service_entry[2],service_entry[3],service_entry[4],service_entry[5],service_entry[6],service_entry[7])

			# Append
			service_entries.append(service_entry)

			# Grab next service entry
			service_entry = cursor.fetchone()

		# Return
		return jsonify(Service_Entries = [s.serialize() for s in service_entries])

	except Exception, e:
		print str(e)
		return str(e)
	
# Run Main
if __name__ == '__main__':
	app.debug = False
	app.run(host='127.0.0.1', port=8081, threaded=True)
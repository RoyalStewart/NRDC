import sys
sys.path.append("..")
from flask import Flask, jsonify, json, request
from flask.ext.cors import cross_origin
from Module_Classes_1 import DisplayProject
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

# View for All
@app.route('/projects/')
@cross_origin()
def index():
	# Try
	try:

		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected now"

		# Table Creation Section
		cursor = cnxn.cursor()

		# Create array of Project
		projects = []

		# Database call of first, last, and email from the PROJECT table
		cursor.execute("SELECT Project, [Unique Identifier], [Name], [Institution Name], [Original Funding Agency], [Grant Number String], [Started Date], [Creation Date], [Modification Date], \
		[Principal Investigator] FROM Infrastructure.Projects")

		# Grab the information for the first person
		project = cursor.fetchone()

		# Iterate while there is information in the person object
		while project is not None:

			# Create a new person from the class with the data from the database
			newproject = DisplayProject(project[0],project[1],project[2],project[3],project[4],project[5],project[6],project[7],project[8],project[9])

			# Add it to Project array
			projects.append(newproject)

			# Grab the next person
			project = cursor.fetchone()
	
		# Return the Project JSON
		return jsonify(Projects = [p.serialize() for p in projects])

	# Except
	except Exception, e:
		print str(e)
		return False, str(e)

# View for Specific
@app.route('/projects/<project_id>')
def specific(project_id):
	# Try
	try:

		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected now"

		# Table Creation Section
		cursor = cnxn.cursor()

		# Database call of first, last, and email from the PROJECT table
		cursor.execute("SELECT Project, [Unique Identifier], [Name], [Institution Name], [Original Funding Agency], [Grant Number String], [Started Date], [Creation Date], [Modification Date], \
		[Principal Investigator] FROM Infrastructure.Projects	WHERE [Unique Identifier] = ?", project_id)

		# Grab the information for the first person
		project = cursor.fetchone()

		# Create a new person from the class with the data from the database
		newproject = DisplayProject(project[0],project[1],project[2],project[3],project[4],project[5],project[6],project[7],project[8],project[9])

		# Return JSON
		return jsonify(newproject.serialize())

	# Except 
	except Exception, e:
		print str(e)
		return False, str(e)

# Create Project
@app.route('/projects/', methods=['POST'])
def create():
	# Try
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
		Institution = JSON['Institution Name']
		Agency = JSON['Original Funding Agency']
		GrantNumber = JSON['Grant Number String']
		StartedDate = JSON['Started Date']
		CreationDate = JSON['Creation Date']
		ModificationDate = JSON['Modification Date']
		PrincipalInvestigator = JSON['Principal Investigator']

		try:

			if convertdatetime(CreationDate):
				CreationDate = convertdatetime(CreationDate)
			else:
				print "Invalid Creation Date Type : Must be a datetime string"
				raise Exception

			if convertdatetime(ModificationDate):
				ModificationDate = convertdatetime(ModificationDate)
			else:
				print "Invalid Modification Date Type : Must be a datetime string"
				raise Exception
				
			if convertdatetime(StartedDate):
				StartedDate = convertdatetime(StartedDate)
			else:
				print "Invalid Started Date Type : Must be a datetime string"
				raise Exception

		except Exception, e:
			print str(e)
			return False, str(e)

		# Update user information from the JSON
		cursor.execute("INSERT INTO Infrastructure.Projects ([Unique Identifier], [Name], [Institution Name], [Original Funding Agency], [Grant Number String], [Started Date], [Creation Date], [Modification Date], \
		[Principal Investigator]) VALUES (?,?,?,?,?,?,?,?,?)", Uniqueid, Name, Institution, Agency, GrantNumber, StartedDate, CreationDate, ModificationDate, PrincipalInvestigator)

		# Commit
		cnxn.commit()

		# Return success
		return "Successfully Created"

	# Except
	except Exception, e:
		print str(e)
		return False, str(e)


# Update Project
@app.route('/projects/', methods=['PUT'])
def update():
	# Try
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
		Uniqueid = JSON['Unique Identifier']
		Name = JSON['Name']
		Institution = JSON['Institution Name']
		Agency = JSON['Original Funding Agency']
		GrantNumber = JSON['Grant Number String']
		StartedDate = JSON['Started Date']
		CreationDate = JSON['Creation Date']
		ModificationDate = JSON['Modification Date']
		PrincipalInvestigator = JSON['Principal Investigator']

		try:

			if convertdatetime(CreationDate):
				CreationDate = convertdatetime(CreationDate)
			else:
				print "Invalid Creation Date Type : Must be a datetime string"
				raise Exception

			if convertdatetime(ModificationDate):
				ModificationDate = convertdatetime(ModificationDate)
			else:
				print "Invalid Modification Date Type : Must be a datetime string"
				raise Exception
				
			if convertdatetime(StartedDate):
				StartedDate = convertdatetime(StartedDate)
			else:
				print "Invalid Started Date Type : Must be a datetime string"
				raise Exception

		except Exception, e:
			print str(e)
			return False, str(e)

		# Update user information from the JSON
		cursor.execute("UPDATE Infrastructure.Projects SET [Name] = ?, [Institution Name] = ?, [Original Funding Agency] = ?, [Grant Number String] = ?, [Started Date] = ?, [Creation Date] = ?, [Modification Date] = ?, \
		[Principal Investigator] = ? WHERE [Unique Identifier] = ?", Name, Institution, Agency, GrantNumber, StartedDate, CreationDate, ModificationDate, PrincipalInvestigator, Uniqueid )

		# Commit
		cnxn.commit()

		# Return success
		return "Successfully Updated"

	# Except
	except Exception, e:
		print str(e)
		return False, str(e)

# Delete Project
@app.route('/projects/<project_id>', methods=['DELETE'])
def delete(project_id):
	# Try
	try:

		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected now"

		# Table Creation Section
		cursor = cnxn.cursor()

		# Delete found user
		cursor.execute("DELETE FROM Infrastructure.Projects WHERE [Unique Identifier] = ?", project_id)

		# Commit
		cnxn.commit()	

		# Return
		return "Successfully Deleted"

	# Except
	except Exception, e:
		print str(e)
		return False, str(e)

# Project Document Relation
@app.route('/projects/<project_id>/documents/')
def projectdocumentrelation(project_id):
	# Try
	try:

		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected now, man"

		# Table Creation Section
		cursor = cnxn.cursor()

		# Create Document array
		documents = []

		# Project Document Relation Join
		cursor.execute("SELECT Documents.[Creation Date], Documents.[Modification Date], Documents.[Name], Documents.[Notes], Documents.[Path], Documents.[Document] \
		FROM ProjectDocumentsRelation AS R \
		JOIN Documents as Documents ON R.Documents = Documents.Document \
		JOIN Projects as Projects ON R.Projects = Projects.Project \
		WHERE R.Project = ?", project_id)
		document = cursor.fetchone()

		# Itterate through documents
		while document is not None:

			# Serialize new documents
			document = displayDocument(document[0],document[1],document[2],document[3],document[4],document[5])

			# Append
			documents.append(document)

			# Grab next document
			document = cursor.fetchone()

		# Return
		return jsonify(Documents = [d.serialize() for d in documents])

	# Except
	except Exception, e:
		print str(e)
		return False, str(e)

# Project Service Entries Relation
@app.route('/projects/<project_id>/service_entries/')
def projectserviceentries(project_id):
	# Try
	try:

		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected now, man"

		# Table Creation Section
		cursor = cnxn.cursor()

		# Create Service Entries array
		service_entries = []

		# Project Service Entries Join
		cursor.execute("SELECT [Service Entries].[Creation Date], [Service Entries].[Date],[Service Entries].[Modification Date],[Service Entries].[Name],[Service Entries].[Notes], \
		[Service Entries].[Operation],[Service Entries].[Photo],[Service Entries].[Service Entry] \
		FROM ProjectServiceEntriesRelation AS R \
		JOIN [Service Entries] AS Service Entries ON R.[Service Entries] = [Service Entries].[Service Entry] \
		JOIN Projects AS Projects ON R.Projects = Projects.Project \
		WHERE R.Project = ?", project_id)
		service_entry = cursor.fetchone()

		# Itterate through service entries
		while service_entry is not None:
				
			# Serialize new Service Entry
			service_entry =  displayServiceEntry(service_entry[0],service_entry[1],service_entry[2],service_entry[3],service_entry[4],service_entry[5],service_entry[6],service_entry[7])

			# Append
			service_entries.append(service_entry)

			# Grab next service entry
			service_entry = cursor.fetchone()

		# Return
		return jsonify(Service_Entries = [s.serialize() for s in service_entries])

	# Except
	except Exception, e:
		print str(e)
		return False, str(e)

# Project Systems Relation
@app.route('/projects/<project_id>/systems/')
def projectsystemsrelation(project_id):
	# Try
	try:

		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected now, man"

		# Table Creation Section
		cursor = cnxn.cursor()

		# Create Systems array
		systems = []

		# Project Systems Relation
		cursor.execute("SELECT Systems.[Creation Date], Systems.Details, Systems.[Installation Date], Systems.[Installation Location], Systems.[Latitude], Systems.[Longitude], \
		Systems.[Modification Date], Systems.[Name],Systems.[Photo],Systems.[Power],Systems.[System] \
		FROM ProjectSystemsRelation AS R \
		JOIN Systems AS Systems ON R.Systems = Systems.System \
		JOIN Projects as Projects ON R.Projects = Projects.Project \
		WHERE R.Project = ?", project_id)
		system = cursor.fetchone()

		# Itterate through systems
		while system is not None:

			# Serialize new System
			system = displaySystem(system[0],system[1],system[2],system[3],system[4],system[5],system[6],system[7],system[8],system[9],system[10])

			# Append
			systems.append(system)

			# Grab next system
			system = cursor.fetchone()

		# Return
		return jsonify(Systems = [s.serialize() for s in systems])

	# Except
	except Exception, e:
		print str(e)
		return False, str(e)

# Run Main
if __name__ == '__main__':
	app.debug = False
	app.run(host='127.0.0.1', port=8082)
import sys
sys.path.append("..")
from flask import Flask, jsonify, json, request
from flask.ext.cors import cross_origin
from Module_Classes_1 import DisplayDocument
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
@app.route('/documents/')
@cross_origin()
def index():
	try:
		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected now, man"

		# Table Creation Section
		cursor = cnxn.cursor()

		# Create array of documents
		documents = []

		# Database call of information from the DOCUMENTS table
		cursor.execute("SELECT Document, [Unique Identifier], Name, Notes, Path, [Creation Date], [Modification Date], Project, Site, Deployment, Component, [Service Entry] FROM Infrastructure.Documents")

		# Grab the information for the first document
		document = cursor.fetchone()

		# Iterate while there is information in the person object
		while document is not None:

			# Create a new document from the class with the data from the database
			newdocument = DisplayDocument(document[0],document[1],document[2],document[3],document[4],document[5],document[6],document[7],document[8],document[9],document[10],document[11])

			# Add it to document array
			documents.append(newdocument)

			# Grab the next document
			document= cursor.fetchone()
	
		# Return the People JSON
		return jsonify(Documents = [d.serialize() for d in documents])
	except Exception, e:
		print str(e)
		return False, str(e)

# View for Specific
@app.route('/documents/<document_id>')
@cross_origin()
def specific(document_id):
	try:
		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected now, man"

		# Table Creation Section
		cursor = cnxn.cursor()

		# Database call of information from the DOCUMENTS table
		cursor.execute("SELECT Document, [Unique Identifier], Name, Notes, Path, [Creation Date], [Modification Date], Project, Site, Deployment, Component, [Service Entry] \
		FROM Infrastructure.Documents WHERE [Unique Identifier] = ?", document_id)

		# Grab the information for the first document
		document = cursor.fetchone()

		# Create a new person from the class with the data from the database
		newdocument = DisplayDocument(document[0],document[1],document[2],document[3],document[4],document[5],document[6],document[7],document[8],document[9],document[10],document[11])

		return jsonify(newdocument.serialize()) 

	except Exception, e:
		print str(e)
		return False, str(e)

# Document From Multiple Modules
@app.route('/documents/site/<siteid>/service_entry/<serviceentryid>/deployment/<deploymentid>/component/<componentid>')
@cross_origin()
def documentfrommultiplemodules(siteid,serviceentryid,deploymentid,componentid):
	try:
		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected now, man"

		# Table Creation Section
		cursor = cnxn.cursor()

		print "inside document module"

		# Database call of information from the DOCUMENTS table
		cursor.execute("SELECT Document, [Unique Identifier], Name, Notes, Path, [Creation Date], [Modification Date], Project, Site, Deployment, Component, [Service Entry] \
		FROM Infrastructure.Documents WHERE [Site] = ? AND [Service Entry] = ? AND [Deployment] = ? AND [Component] = ?", siteid,serviceentryid,deploymentid,componentid)

		print "past database call"

		# Create array of documents
		documents = []

		# Grab the information for the first document
		document = cursor.fetchone()

		print "before while loop"

		# Iterate while there is information in the person object
		while document is not None:

			print "before new document"

			# Create a new document from the class with the data from the database
			newdocument = DisplayDocument(document[0],document[1],document[2],document[3],document[4],document[5],document[6],document[7],document[8],document[9],document[10],document[11])

			print "after new document"

			# Add it to document array
			documents.append(newdocument)

			# Grab the next document
			document= cursor.fetchone()
	
		# Return the People JSON
		return jsonify(Documents = [d.serialize() for d in documents])

	except Exception, e:
		print str(e)
		return False, str(e)

# Create Document
@app.route('/documents/', methods=['POST'])
def create():
	try:
		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected now, man"

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
		Name = JSON['Name']
		Notes = JSON['Notes']
		Path = JSON['Path']
		CreationDate = JSON['Creation Date']
		ModificationDate = JSON['Modification Date']
		Project = JSON['Project']
		Site = JSON['Site']
		Deployment = JSON['Deployment']
		Component = JSON['Component']
		ServiceEntry = JSON['Service Entry']

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

		except Exception, e:
			print str(e)
			return False, str(e)
			
		# Update user information from the JSON
		cursor.execute("INSERT INTO Infrastructure.Documents ([Unique Identifier], Name, Notes, Path, [Creation Date], [Modification Date], Project, Site, Deployment, [Component], [Service Entry]) \
		VALUES (?,?,?,?,?,?,?,?,?,?,?)", UniqueID, Name, Notes, Path, CreationDate, ModificationDate, Project, Site, Deployment, Component, ServiceEntry)

		# Commit
		cnxn.commit()

		# Return success
		return "Successfully Created"

	except Exception, e:
		print str(e)
		return False, str(e)

# Update Document
@app.route('/documents/', methods=['PUT'])
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

		# Grab values from the JSON
		UniqueID = JSON['Unique Identifier']
		Name = JSON['Name']
		Notes = JSON['Notes']
		Path = JSON['Path']
		CreationDate = JSON['Creation Date']
		ModificationDate = JSON['Modification Date']
		Project = JSON['Project']
		Site = JSON['Site']
		Deployment = JSON['Deployment']
		Component = JSON['Component']
		ServiceEntry = JSON['Service Entry']

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

		except Exception, e:
			print str(e)
			return False, str(e)
			
		# Update user information from the JSON
		cursor.execute("UPDATE Infrastructure.Documents SET [Unique Identifier] = ?, Name = ?, Notes = ?, Path = ?, [Creation Date] = ?, [Modification Date] = ?, \
		Project = ?, Site = ?, Deployment = ?, Component = ?, [Service Entry] = ? WHERE [Unique Identifier] = ?", UniqueID, Name, Notes, Path, CreationDate, ModificationDate, Project, Site, Deployment, Component, ServiceEntry, UniqueID)

		# Commit
		cnxn.commit()

		# Return success
		return "Successfully Updated"

	except Exception, e:
		print str(e)
		return False, str(e)

# Delete Document
@app.route('/documents/<document_id>', methods=['DELETE'])
def delete(document_id):
	try:
		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected now, man"

		# Table Creation Section
		cursor = cnxn.cursor()

		# Delete found
		cursor.execute("DELETE FROM Infrastructure.Documents WHERE [Unique Identifier] = ?", document_id)

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
	app.run(host='127.0.0.1', port=8086)

import sys
sys.path.append("..")
from flask import Flask, jsonify, json, request
from flask.ext.cors import cross_origin
from Module_Classes_1 import DisplayComponent
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
@app.route('/components/')
@cross_origin()
def index():
	# Try
	try:

		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected"

		# Table Creation Section
		Cursor = cnxn.cursor()

		# Create array of components
		Components = []

		# Database call all information of the COMPONENT table
		Cursor.execute("SELECT [Component], [Unique Identifier], Name, Manufacturer, Model, [Serial Number], Vendor, Supplier, [Installation Date], [Installation Details], \
		[Last Calibrated Date], [Wiring Notes], [Creation Date], [Modification Date], Deployment, Photo from Infrastructure.Components")

		# Grab the information for the first component
		Component = Cursor.fetchone()

		# Iterate while there is information in the component object
		while Component is not None:

			if Component[15] is not None: # <-----------------Updates

				Component[15] = binascii.a2b_base64(Component[15]) # <-----------------Updates

			# Create a new component from the class with the data from the database
			NewComponent = DisplayComponent(Component[0],Component[1],Component[2],Component[3],Component[4],Component[5],Component[6],Component[7],Component[8],Component[9],Component[10],Component[11],Component[12],Component[13],Component[14], Component[15])

			# Add it to components array
			Components.append(NewComponent)

			# Grab the next person
			Component = Cursor.fetchone()
	
		# Return the People JSON
		return jsonify(Components = [c.serialize() for c in Components])

	# Except
	except Exception, e:
		print str(e)
		return str(e)

# View for Specific
@app.route('/components/<uniqueid>')
def specific(uniqueid):
	# Try
	try:

		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected now, man"

		# Table Creation Section
		Cursor = cnxn.cursor()

		# Database call all information from COMPONENT table
		Cursor.execute("SELECT [Component], [Unique Identifier], Name, Manufacturer, Model, [Serial Number], Vendor, Supplier, [Installation Date], [Installation Details], \
		[Last Calibrated Date], [Wiring Notes], [Creation Date], [Modification Date], Deployment, Photo from Infrastructure.Components WHERE [Unique Identifier] = ?", uniqueid)

		# Grab the information for the component
		Component = Cursor.fetchone()

		if Component[15] is not None: # <-----------------Updates

			Component[15] = binascii.a2b_base64(Component[15]) # <-----------------Updates

		# Create a new person from the class with the data from the database
		NewComponent = DisplayComponent(Component[0],Component[1],Component[2],Component[3],Component[4],Component[5],Component[6],Component[7],Component[8],Component[9],Component[10],Component[11],Component[12],Component[13],Component[14], Component[15])

		# Return
		return jsonify(NewComponent.serialize())

	# Except
	except Exception, e:
		print str(e)
		return str(e)

# Components From Deployment
@app.route('/components/deployment/<deployment_id>')
def componentsfromdeployment(deployment_id):
	# Try
	try:

		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected now, man"

		# Table Creation Section
		Cursor = cnxn.cursor()

		# Database call all information from COMPONENT table
		Cursor.execute("SELECT [Component], [Unique Identifier], Name, Manufacturer, Model, [Serial Number], Vendor, Supplier, [Installation Date], [Installation Details], \
		[Last Calibrated Date], [Wiring Notes], [Creation Date], [Modification Date], Deployment, Photo from Infrastructure.Components WHERE [Deployment] = ?", deployment_id)

		# Create array of components
		Components = []

		# Grab the information for the first component
		Component = Cursor.fetchone()

		# Iterate while there is information in the component object
		while Component is not None:

			if Component[15] is not None: # <-----------------Updates

				Component[15] = binascii.a2b_base64(Component[15]) # <-----------------Updates

			# Create a new component from the class with the data from the database
			NewComponent = DisplayComponent(Component[0],Component[1],Component[2],Component[3],Component[4],Component[5],Component[6],Component[7],Component[8],Component[9],Component[10],Component[11],Component[12],Component[13],Component[14], Component[15])

			# Add it to components array
			Components.append(NewComponent)

			# Grab the next person
			Component = Cursor.fetchone()
	
		# Return the People JSON
		return jsonify(Components = [c.serialize() for c in Components])

	# Except
	except Exception, e:
		print str(e)
		return str(e)

# Create Component
@app.route('/components/', methods=['POST'])
def create():
	# Try
	try:

		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected"

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
		Manufacturer = JSON['Manufacturer']
		Model = JSON['Model']
		SerialNumber = JSON['Serial Number']
		Vendor = JSON['Vendor']
		Supplier = JSON['Supplier']
		InstallationDate = JSON['Installation Date']
		InstallationDetails = JSON['Installation Details']
		LastCalibratedDate = JSON['Last Calibrated Date']
		WiringNotes = JSON['Wiring Notes']
		CreationDate = JSON['Creation Date']
		ModificationDate = JSON['Modification Date']
		Deployment = JSON['Deployment']
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

			# Installation Date
			if convertdatetime(InstallationDate):
				InstallationDate = convertdatetime(InstallationDate)
			else:
				print "Invalid Installation Date Type : Must be a datetime string"
				raise Exception

			# Last Calibrated Date
			if convertdatetime(LastCalibratedDate):
				LastCalibratedDate = convertdatetime(LastCalibratedDate)
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
		cursor.execute("INSERT INTO Infrastructure.Components ([Unique Identifier], Name, Manufacturer, Model, [Serial Number], Vendor, Supplier, [Installation Date], \
		[Installation Details], [Last Calibrated Date], [Wiring Notes], [Creation Date], [Modification Date], Deployment, Photo) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", UniqueID, Name, Manufacturer, Model, SerialNumber, Vendor, Supplier, InstallationDate, InstallationDetails, LastCalibratedDate, WiringNotes, CreationDate, ModificationDate, Deployment, Photo)

		# Commit
		cnxn.commit()

		# Return
		return "Successfully Created"

	# Except
	except Exception, e:
		print str(e)
		return str(e)

# Update Component
@app.route('/components/', methods=['PUT'])
def update():
	# Try
	try:

		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected"

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
		Manufacturer = JSON['Manufacturer']
		Model = JSON['Model']
		SerialNumber = JSON['Serial Number']
		Vendor = JSON['Vendor']
		Supplier = JSON['Supplier']
		InstallationDate = JSON['Installation Date']
		InstallationDetails = JSON['Installation Details']
		WiringNotes = JSON['Wiring Notes']
		CreationDate = JSON['Creation Date']
		ModificationDate = JSON['Modification Date']
		Deployment = JSON['Deployment']
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

			# Installation Date
			if convertdatetime(InstallationDate):
				InstallationDate = convertdatetime(InstallationDate)
			else:
				print "Invalid Installation Date Type : Must be a datetime string"
				raise Exception

			# Last Calibrated Date
			if convertdatetime(LastCalibratedDate):
				LastCalibratedDate = convertdatetime(LastCalibratedDate)
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
		cursor.execute("UPDATE Infrastructure.Components SET [Unique Identifier] = ?, Name = ?, Manufacturer = ?, Model = ?, [Serial Number] = ?, Vendor = ?, Supplier = ?, \
		[Installation Date] = ?,[Installation Details] = ?, [Wiring Notes] = ?, [Creation Date] = ?, [Modification Date] = ?, Deployment = ?, Photo = ? \
		WHERE [Unique Identifier] = ?", UniqueID, Name, Manufacturer, Model, SerialNumber, Vendor, Supplier, InstallationDate, InstallationDetails, WiringNotes, CreationDate, ModificationDate, Deployment, Photo, UniqueID)

		# Commit
		cnxn.commit()

		# Return
		return "Successfully Updated"

	# Except
	except Exception, e:
		print str(e)
		return str(e)

# Delete Component
@app.route('/components/<component_id>', methods=['DELETE'])
def delete(component_id):
	# Try
	try:

		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected now"

		# Table Creation Section
		cursor = cnxn.cursor()

		# Delete found user
		cur.execute("DELETE FROM Infrastructure.Components WHERE [Unique Identifier] = ?", component_id)

		# Commit
		cnxn.commit()	

		# Return
		return "Successfully Deleted"

	# Except
	except Exception, e:
		print str(e)
		return str(e)

# Component Document Relation
@app.route('/components/<component_id>/documents/')
def componentdocumentrelation(component_id):
	# Try
	try:

		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected now, man"

		# Table Creation Section
		cursor = cnxn.cursor()

		# Create Documents array
		documents = []

		# Join Table
		cursor.execute("SELECT Documents.[Creation Date], Documents.[Modification Date], Documents.[Name], Documents.[Notes], Documents.[Path], Documents.[Document] \
		FROM ComponentDocumentsRelation AS R \
		JOIN Documents AS Documents ON R.Documents = Documents.Document \
		JOIN Componets AS Components ON R.Components = Components.Component \
		WHERE R.Component = ?", component_id)
		document = cursor.fetchone()

		# Itterate through Documents
		while document is not None:
				
			# Serialize new Document
			document =  displayDocument(document[0],document[1],document[2],document[3],document[4],document[5])

			# Append
			documents.append(document)

			# Grab next Document
			document = cursor.fetchone()

		# Return
		return jsonify(Documents = [d.serialize() for d in documents])

	# Except
	except Exception, e:
		print str(e)
		return str(e)

# Run Main
if __name__ == '__main__':
	app.debug = False
	app.run(host='127.0.0.1', port=8085)
import sys
sys.path.append("..")
from flask import Flask, jsonify, json, request
from flask.ext.cors import cross_origin
from Module_Classes_1 import DisplayDeployment
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
@app.route('/deployments/')
@cross_origin()
def index():
	# Try
	try:

		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected"

		# Table Creation Section
		Cursor = cnxn.cursor()

		# Create array of deployments
		deployments = []

		# Database call all information of the DEPLOYMENT table
		Cursor.execute("SELECT [Deployment], [Unique Identifier], [Name], [Purpose], [Center Offset], [Location].Lat, [Location].Long, [Location].Z, \
		[Location].STSrid ,[Height From Ground], [Parent Logger], [Established Date], [Abandoned Date], \
		[Creation Date], [Modification Date], [System] FROM Infrastructure.Deployments")

		# Grab the information for the first deployment
		Deployment = Cursor.fetchone()

		# Iterate while there is information in the deployment object
		while Deployment is not None:

			# Clean Location
			Deployment[5] = str(Deployment[5])
			Deployment[6] = str(Deployment[6])
			Deployment[7] = str(Deployment[7])
			Deployment[8] = str(Deployment[8])

			# Create a new deployment from the class with the data from the database
			NewDeployment = DisplayDeployment(Deployment[0],Deployment[1],Deployment[2],Deployment[3],Deployment[4],Deployment[5],Deployment[6],Deployment[7],Deployment[8],Deployment[9],Deployment[10],Deployment[11],Deployment[12],Deployment[13],Deployment[14],Deployment[15])

			# Add it to deployment array
			deployments.append(NewDeployment)

			# Grab the next deployment
			Deployment = Cursor.fetchone()
	
		# Return the Deployment JSON
		return jsonify(Deployments = [d.serialize() for d in deployments])

	# Except
	except Exception, e:
		print str(e)
		return False, str(e)

# View for Specific
@app.route('/deployments/<deployment_id>')
def specific(deployment_id):
	# Try
	try:

		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected now, man"

		# Table Creation Section
		Cursor = cnxn.cursor()

		# Database call all information from DEPLOYMENT table
		Cursor.execute("SELECT Deployment, [Unique Identifier], Name, Purpose, [Center Offset], [Location].Lat, [Location].Long, [Location].Z, \
		[Location].STSrid, [Height From Ground], [Parent Logger], [Established Date], [Abandoned Date] \
		[Creation Date], [Modification Date], System FROM Infrastructure.Deployments WHERE [Unique Identifier] = ?", deployment_id)

		# Grab the information for the deployment
		Deployment = Cursor.fetchone()

		# Clean Location
		Deployment[5] = str(Deployment[5])
		Deployment[6] = str(Deployment[6])
		Deployment[7] = str(Deployment[7])
		Deployment[8] = str(Deployment[8])

		# Create a new deployment from the class with the data from the database
		NewDeployment = DisplayDeployment(Deployment[0],Deployment[1],Deployment[2],Deployment[3],Deployment[4],Deployment[5],Deployment[6],Deployment[7],Deployment[8],Deployment[9],Deployment[10],Deployment[11],Deployment[12],Deployment[13],Deployment[14],Deployment[15])

		# Return
		return jsonify(NewDeployment.serialize())

	# Except
	except Exception, e:
		print str(e)
		return False, str(e)

# Deployments From System
@app.route('/deployments/system/<system_id>', methods = ['GET'])
def deploymentsfromsystem(system_id):
	# Try
	try:

		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected now, man"

		# Table Creation Section
		Cursor = cnxn.cursor()

		# Database call all information from DEPLOYMENT table
		Cursor.execute("SELECT Deployment, [Unique Identifier], Name, Purpose, [Center Offset], [Location].Lat, [Location].Long, [Location].Z, \
		[Location].STSrid, [Height From Ground], [Parent Logger], [Established Date], [Abandoned Date], \
		[Creation Date], [Modification Date], System FROM Infrastructure.Deployments WHERE [System] = ?", system_id)

		# Create array of deployments
		deployments = []

		# Grab the information for the deployment
		Deployment = Cursor.fetchone()

		# Iterate while there is information in the deployment object
		while Deployment is not None:

			Deployment[5] = str(Deployment[5])
			Deployment[6] = str(Deployment[6])
			Deployment[7] = str(Deployment[7])
			Deployment[8] = str(Deployment[8])

			# Create a new deployment from the class with the data from the database
			NewDeployment = DisplayDeployment(Deployment[0],Deployment[1],Deployment[2],Deployment[3],Deployment[4],Deployment[5],Deployment[6],Deployment[7],Deployment[8],Deployment[9],Deployment[10],Deployment[11],Deployment[12],Deployment[13],Deployment[14],Deployment[15])

			# Add it to deployment array
			deployments.append(NewDeployment)

			# Grab the next deployment
			Deployment = Cursor.fetchone()
	
		# Return the Deployment JSON
		return jsonify(Deployments = [d.serialize() for d in deployments])

	# Except
	except Exception, e:
		print str(e)
		return False, str(e)

# Create Deployment
@app.route('/deployments/', methods=['POST'])
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
		Purpose = JSON['Purpose']
		CenterOffset = JSON['Center Offset']
		Location = JSON['Location']
		HeightFromGround = JSON['Height From Ground']
		ParentLogger = JSON['Parent Logger']
		EstablishedDate = JSON['Established Date']
		AbandonedDate = JSON['Abandoned Date']
		CreationDate = JSON['Creation Date']
		ModificationDate = JSON['Modification Date']
		System = JSON['System']

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

			if convertdatetime(EstablishedDate):
				EstablishedDate = convertdatetime(EstablishedDate)
			else:
				print "Invalid Established Date Type : Must be a datetime string"
				raise Exception

			if AbandonedDate is not None:
				if convertdatetime(AbandonedDate):
					AbandonedDate = convertdatetime(AbandonedDate)
				else:
					print "Invalid Abandoned Date Type : Must be a datetime string"
					raise Exception

		except Exception, e:
			print str(e)
			return False, str(e)

		# Update user information from the JSON
		cursor.execute("INSERT INTO Infrastructure.Deployments ([Unique Identifier], Name, Purpose, [Center Offset], Location, [Height From Ground], [Parent Logger], \
		[Established Date], [Abandoned Date], [Creation Date], [Modification Date], System)	VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", UniqueID, Name, Purpose, CenterOffset, Location, HeightFromGround, ParentLogger, EstablishedDate, AbandonedDate, CreationDate, ModificationDate, System)

		# Commit
		cnxn.commit()

		# Return
		return "Successfully Created"

	# Except
	except Exception, e:
		print str(e)
		return False, str(e)

# Update Deployment
@app.route('/deployments/', methods=['PUT'])
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
		Purpose = JSON['Purpose']
		CenterOffset = JSON['Center Offset']
		Location = JSON['Location']
		HeightFromGround = JSON['Height From Ground']
		ParentLogger = JSON['Parent Logger']
		EstablishedDate = JSON['Established Date']
		AbandonedDate = JSON['Abandoned Date']
		CreationDate = JSON['Creation Date']
		ModificationDate = JSON['Modification Date']
		System = JSON['System']

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
				
			if convertdatetime(EstablishedDate):
				EstablishedDate = convertdatetime(EstablishedDate)
			else:
				print "Invalid Established Date Type : Must be a datetime string"
				raise Exception

			if convertdatetime(AbandonedDate):
				AbandonedDate = convertdatetime(AbandonedDate)
			else:
				print "Invalid Abandoned Date Type : Must be a datetime string"
				raise Exception

		except Exception, e:
			print str(e)
			return False, str(e)
			
		# Update user information from the JSON
		cursor.execute("UPDATE Infrastructure.Deployments SET [Unique Identifier] = ?, Name = ?, Purpose = ?, [Center Offset] = ?, Location = ?, [Height From Ground] = ?, \
		[Parent Logger] = ?,	[Established Date] = ?, [Abandoned Date] = ?, [Creation Date] = ?, [Modification Date] = ?, System = ?	WHERE [Unique Identifier] = ?", UniqueID, Name, Purpose, CenterOffset, Location,	HeightFromGround, ParentLogger, EstablishedDate, AbandonedDate, CreationDate, ModificationDate, System, UniqueID)

		# Commit
		cnxn.commit()

		# Return
		return "Successfully Updated"

	# Except
	except Exception, e:
		print str(e)
		return False, str(e)

# Delete Deployment
@app.route('/deployments/<deployment_id>', methods=['DELETE'])
def delete(deployment_id):
	# Try
	try:

		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected now"

		# Table Creation Section
		cursor = cnxn.cursor()

		# Delete found user
		cursor.execute("DELETE FROM Infrastructure.Deployments WHERE [Unique Identifier] = ?", deployment_id)

		# Commit
		cnxn.commit()	

		# Return
		return "Successfully Deleted"

	# Except
	except Exception, e:
		print str(e)
		return False, str(e)

# Run Main
if __name__ == '__main__':
	app.debug = False
	app.run(host='127.0.0.1', port=8088)
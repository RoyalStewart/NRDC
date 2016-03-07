import sys
sys.path.append("..")
from flask import Flask, jsonify, json, request
from flask.ext.cors import cross_origin
from Module_Classes_1 import DisplaySite
import pyodbc
import binascii
import iso8601
import pytz

app = Flask(__name__)

# CONFIGURATION
# Convert Photo Function
def convertphoto(Photovalue):
	correctPhoto = binascii.a2b_base64(Photovalue)
	correctPhoto = correctPhoto.encode("ISO-8859-1")

# View for All
@app.route('/sites/')
@cross_origin()
def index():
	try:
		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected now"

		# Table Creation Section
		cursor = cnxn.cursor()

		# Create array of sites
		sites = []

		# Database call of first, last, and email from the PERSON table
		cursor.execute("SELECT Site, [Unique Identifier], [Name], [Notes], [Alias], [Location].Lat, [Location].Long, [Location].Z, [Location].STSrid, \
			[Land Owner], [Permit Holder], [Time Zone Name], [Time Zone Abbreviation], [Time Zone Offset], \
			[Project], [GPS Landmark], [Landmark Photo] FROM Infrastructure.Sites")

		# Grab the information for the first site
		site = cursor.fetchone()

		# Clean Location
		site[5] = str(site[5])
		site[6] = str(site[6])
		site[7] = str(site[7])
		site[8] = str(site[8])

		# Iterate while there is information in the person object
		while site is not None:

			if site[16] is not None:

				site[16] = binascii.a2b_base64(site[16])

			# Create a new person from the class with the data from the database
			newsite = DisplaySite(site[0],site[1],site[2],site[3],site[4],site[5],site[6],site[7],site[8],site[9],site[10],site[11],site[12],site[13],site[14],site[15],site[16])

			# Add it to sites array
			sites.append(newsite)

			# Grab the next site
			site = cursor.fetchone()
	
		# Return the Site JSON
		return jsonify(Sites = [s.serialize() for s in sites])
	except Exception, e:
		print str(e)
		return False, str(e)

# View for Specific
@app.route('/sites/<site_id>')
def specific(site_id):
	try:
		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected now"

		# Table Creation Section
		cursor = cnxn.cursor()

		# Database call
		cursor.execute("SELECT Site, [Unique Identifier], Name, Notes, Alias, [Location].Lat, [Location].Long, [Location].Z, [Location].STSrid, \
		[Land Owner], [Permit Holder], [Time Zone Name], [Time Zone Abbreviation], [Time Zone Offset], \
		Project, [GPS Landmark], [Landmark Photo]	from Infrastructure.Sites WHERE [Unique Identifier] = ?", site_id)

		# Grab the information for the site
		site = cursor.fetchone()

		# Clean Location
		site[5] = str(site[5])
		site[6] = str(site[6])
		site[7] = str(site[7])
		site[8] = str(site[8])

		# Decode Photo
		if site[16] is not None:

			site[13] = binascii.a2b_base64(site[16])

		# Create a new site from the class with the data from the database
		newsite = DisplaySite(site[0],site[1],site[2],site[3],site[4],site[5],site[6],site[7],site[8],site[9],site[10],site[11],site[12],site[13],site[14],site[15],site[16])

		# Return information
		return jsonify(newsite.serialize()) 

	except Exception, e:
		print str(e)
		return False, str(e)

# Create Site
@app.route('/sites/', methods=['POST'])
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
		Name = JSON['Name']
		Notes = JSON['Notes']
		Alias = JSON['Alias']
		Location = JSON['Location']
		LandOwner = JSON['Land Owner']
		PermitHolder = JSON['Permit Holder']
		TimeZoneName = JSON['Time Zone Name']
		TimeZoneAbbreviation = JSON['Time Zone Abbreviation']
		TimeZoneOffset = JSON['Time Zone Offset']
		Project = JSON['Project']
		GPSLandmark = JSON['GPS Landmark']
		LandmarkPhoto = JSON['Landmark Photo']

		print Location

		# Type Checking
		try:

			# Photo
			if LandmarkPhoto is None: 
				LandmarkPhoto = pyodbc.BinaryNull
			elif type(LandmarkPhoto) is str:
				LandmarkPhoto = convertphoto(LandmarkPhoto)
			else:
				print "Invalid Photo Type : Must be a base64 string"
				raise Exception

		except Exception, e:
			print str(e)
			return False, str(e)

		# Update user information from the JSON
		cursor.execute("INSERT INTO Infrastructure.Sites ([Unique Identifier], [Name], [Notes], [Alias], [Location], [Land Owner], [Permit Holder], [Time Zone Name], [Time Zone Abbreviation], \
		[Time Zone Offset], [Project], [GPS Landmark], [Landmark Photo]) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", UniqueID, Name, Notes, Alias, Location, LandOwner, PermitHolder, TimeZoneName, TimeZoneAbbreviation, TimeZoneOffset, Project, GPSLandmark,LandmarkPhoto)

		# Commit
		cnxn.commit()

		# Return success
		return "Successfully Created"

	except Exception, e:
		print str(e)
		return False, str(e)

# Update Site
@app.route('/sites/', methods=['PUT'])
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
		Alias = JSON['Alias']
		Location = JSON['Location']
		PermitHolder = JSON['Permit Holder']
		TimeZoneName = JSON['Time Zone Name']
		TimeZoneAbbreviation = JSON['Time Zone Abbreviation']
		TimeZoneOffset = JSON['Time Zone Offset']
		Project = JSON['Project']
		GPSLandmark = JSON['GPS Landmark']
		LandmarkPhoto = JSON['Landmark Photo']
		
		# Type Checking
		try:

			# Photo
			if LandmarkPhoto is None: 
				LandmarPhoto = pyodbc.BinaryNull
			elif type(LandmarkPhoto) is str:
				LandmarkPhoto = convertphoto(LandmarkPhoto)
			else:
				print "Invalid Photo Type : Must be a base64 string"
				raise Exception

		except Exception, e:
			print str(e)
			return False, str(e)

		# Update user information from the JSON
		cursor.execute("UPDATE Infrastructure.Sites SET [Unique Identifier] = ?, [Name] = ?, [Notes] = ?, [Alias] = ?, Location = ?, [Permit Holder] = ?, [Time Zone Name] = ?, \
		[Time Zone Abbreviation] = ?, [Time Zone Offset] = ?, Project = ?, [GPS Landmark] = ?, [Landmark Photo] = ? WHERE [Unique Identifier] = ?", UniqueID, Name, Notes, Alias, Location, PermitHolder, TimeZoneName, TimeZoneAbbreviation, TimeZoneOffset, Project, GPSLandmark,LandmarkPhoto, UniqueID)

		# Commit
		cnxn.commit()

		# Return success
		return "Successfully Updated"

	except Exception, e:
		print str(e)
		return False, str(e)

# Delete Site
@app.route('/sites/<site_id>', methods=['DELETE'])
def delete(site_id):
	try:
		# Connect to Test database
		cnxn = pyodbc.connect("DSN=dsn;DATABASE=dbase;UID=uname;PWD=pword")
		print "You are successfully connected now"

		# Table Creation Section
		cursor = cnxn.cursor()

		# Delete found user
		cursor.execute("DELETE FROM Infrastructure.Sites WHERE [Unique Identifier] = ?", site_id)

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
	app.run(host='127.0.0.1', port=8087)
import sys
sys.path.append("../People")
sys.path.append("../Projects")
sys.path.append("../Sites")
sys.path.append("../Systems")
sys.path.append("../Deployments")
sys.path.append("../Components")
sys.path.append("../Documents")
sys.path.append("../ServiceEntries")
from flask import Flask, jsonify, json, render_template, request
from flask.ext.cors import cross_origin
import pprint
from PersonProxy import Person, People
from ProjectProxy import Project, Projects
from SiteProxy import Site, Sites
from SystemProxy import System, Systems
from DeploymentProxy import Deployment, Deployments
from ComponentProxy import Component, Components
from DocumentProxy import Document, Documents
from ServiceEntryProxy import ServiceEntry, ServiceEntries
app = Flask(__name__)

# CONFIGURATION

"""
Andriod Edge application for the Nevada Research Data Center.
Creators:
Royal Stewart
Vinh Le
"""

# Create Method
"""
A POST request is sent to the server. This request can contain information from any module, as long as the formatting is correct, as a JSON. This JSON is broken into it's
components and then sent to their respected module's proxy servers. The create method can accept one Person but as many of the other modules as wanted.
The information is sent to the database in the correct order, and shouldn't create issues when creating relations.
"""

@app.route('/edge/', methods=['POST'])
def create():
	# Grab JSON from the request
	try:
		JSON = request.get_json()
	except Exception as e:
		print str(e)
		return e

	# Person
	if 'Person' in JSON:
		for i in JSON['People']:
			try:
				# Make PersonJSON of type Person
				PersonJSON = Person(i)
				PersonSend = People()

				# Send the JSON with PersonSend
				PersonSend.CreatePerson(PersonJSON)
			except Exception, e:
				print str(e)
				return False, str(e)

	# Project
	if 'Projects' in JSON:

		# Itterate through Project section
		for i in JSON['Projects']:
			try:

				# Make ProjectJSON of type Project
				ProjectJSON = Project(i)
				ProjectSend = Projects()

				# Send the JSON with ProjectSend
				ProjectSend.CreateProject(ProjectJSON)
			except Exception, e:
				return False, str(e)

	# Check for SITE
	if 'Sites' in JSON:

		# Itterate through Stie section
		for i in JSON['Sites']:

			# Try to send request
			try:
				# Make SiteJSON of type Site, utilize proxy servers
				SiteJSON = Site(i)
				SiteSend = Sites()

				# Send the JSON with SiteSend
				SiteSend.CreateSite(SiteJSON)
			except Exception, e:
				return False, str(e)

	# Check for SYSTEM
	if 'Systems' in JSON:

		# Itterate through System section
		for i in JSON['Systems']:

			# Try to send request
			try:
				# Make SystemJSON of type System, utilize proxy servers
				SystemJSON = System(i)
				SystemSend = Systems()

				# Send the JSON with SystemSend
				SystemSend.CreateSystem(SystemJSON)
			except Exception, e:
				return False, str(e)

	# Check for DEPLOYMENT
	if 'Deployments' in JSON:

		# Itterate through Deployment
		for i in JSON['Deployments']:

			# Try to send request
			try:
				# Make DeploymentJSON of type Deployment, utilize proxy servers
				DeploymentJSON = Deployment(i)
				DeploymentSend = Deployments()

				# Send the JSON with DeploymentSend
				DeploymentSend.CreateDeployment(DeploymentJSON)
			except Exception, e:
				return False, str(e)

	# Check for COMPONENTS
	if 'Components' in JSON:

		# Itterate through Components
		for i in JSON['Components']:

			# Try to send request
			try:
				# Make ComponentJSON of type Component, utilize proxy servers
				ComponentJSON = Component(i)
				ComponentSend = Components()

				# Send the JSON with ComponentSend
				ComponentSend.CreateComponent(ComponentJSON)
			except Exception, e:
				print str(e)
				return False, str(e)

	# Check for SERVICE ENTRIES
	if 'Service Entries' in JSON:

		# Itterate through ServiceEntries
		for i in JSON['ServiceEntries']:

			# Try to send request
			try:
				# Make ServiceEntryJSON of type ServiceEntry, utilize proxy servers
				ServiceEntriesJSON = ServiceEntry(i)
				ServiceEntriesSend = ServiceEntries()

				# Send the JSON with ServiceEntriesSend
				ServiceEntriesSend.CreateServiceEntry(ServiceEntriesJSON)
			except Exception, e:
				print str(e)
				return False, str(e)

	# Check for DOCUMENTS
	if 'Documents' in JSON:

		# Itterate through Documents
		for i in JSON['Documents']:

			# Try to send request
			try:
				# Make DocumentJSON of type Document, utilize proxy servers
				DocumentJSON = Document(i)
				DocumentSend = Documents()

				# Send the JSON with DocumentSend
				DocumentSend.CreateDocument(DocumentJSON)
			except Exception, e:
				print str(e)
				return False, str(e)

	# Return Hate so much Hate. Like the kind of hate that makes babies ugly. Really need to change this in VERY near future
	return jsonify(JSON)

# All Projects
@app.route('/edge/projects/', methods=['GET'])
def allprojects():
	try:

		GetProjects = Projects().GetAllProjects()

	except Exception, e:
		print str(e)
		return False, str(e)

	return json.dumps(GetProjects)

# All People In Project
@app.route('/edge/people/project/<projectid>', methods=['GET'])
def allpeoplein(projectid):
	try:

		GetPeople = People().GetAllPeople()

	except Exception, e:
		print str(e)
		return False, str(e)

	return json.dumps(GetPeople)

# All Sites In Project
@app.route('/edge/sites/project/<projectid>', methods=['GET'])
def allsitesin(projectid):
	try:

		GetSites = Sites().GetAllSites()

	except Exception, e:
		print str(e)
		return False, str(e)

	return json.dumps(GetSites)

# All Systems In Site and Project
@app.route('/edge/systems/project/<projectid>/site/<siteid>', methods=['GET'])
def allsystemsin(projectid,siteid):
	try:

		GetSystems = Systems().GetAllSystemsWithSite(siteid)

	except Exception, e:
		print str(e)
		return False, str(e)

	return json.dumps(GetSystems)

# All Deployments In System and Project
@app.route('/edge/deployments/project/<projectid>/system/<systemid>', methods=['GET'])
def alldeploymentsin(projectid,systemid):
	try:

		GetDeployments = Deployments().GetAllDeploymentsWithSystem(systemid)

	except Exception, e:
		print str(e)
		return False, str(e)

	return json.dumps(GetDeployments)

# All Components In Deployment and Project
@app.route('/edge/components/project/<projectid>/deployment/<deploymentid>', methods=['GET'])
def allcomponentsin(projectid,deploymentid):
	try:

		GetComponents = Components().GetAllComponentsWithDeployment(deploymentid)

	except Exception, e:
		print str(e)
		return False, str(e)

	return json.dumps(GetComponents)

# All Documents Associated With All Modules
@app.route('/edge/documents/project/<projectid>/site/<siteid>/service_entry/<serviceentryid>/deployment/<deploymentid>/component/<componentid>', methods=['GET'])
def alldocumentsin(projectid,siteid,serviceentryid,deploymentid,componentid):
	try:

		GetDocuments = Documents().GetAllDocumentsWithModules(siteid,serviceentryid,deploymentid,componentid)

	except Exception, e:
		print str(e)
		return False, str(e)

	return json.dumps(GetDocuments)		

# All Service Entries With All Modules
@app.route('/edge/serviceentries/project/<projectid>/system/<systemid>/component/<componentid>', methods=['GET'])
def allserviceentriesin(projectid,systemid,componentid):
	try:

		GetServiceEntries = ServiceEntries().GetAllServiceEntriesWithModules(systemid,componentid)

	except Exception, e:
		print str(e)
		return False, str(e)

	return json.dumps(GetServiceEntries)		

# Update Method
"""
A PUT request is sent to the respected modules. A full JSON of information per module must be included in the call. Any changes from what's on the database
to what's in the JSON will be reflected on the database. Handled VERY similiar to the create method.
"""

@app.route('/edge/', methods=['PUT'])
def update():

	# Grab JSON from the request
	try:
		JSON = request.get_json()
	except Exception as e:
		print e
		return e

	# Person
	if 'People' in JSON:

		# Loop
		for i in JSON['People']:

			# Try to send request
			try:
				# Make PersonJSON of type Person
				PersonJSON = Person(i)
				PersonSend = People()

				# Send the JSON with PersonSend
				PersonSend.UpdatePerson(PersonJSON)
			except Exception, e:
				print str(e)
				return False, str(e)

	# Project
	if 'Projects' in JSON:

		# Itterate through Project section
		for i in JSON['Projects']:

			# Try to send request
			try:
				# Make ProjectJSON of type Project
				ProjectJSON = Project(i)
				ProjectSend = Projects()

				# Send the JSON with ProjectSend
				ProjectSend.UpdateProject(ProjectJSON)
			except Exception, e:
				return False, str(e)

	# Check for SITE
	if 'Sites' in JSON:

		# Itterate through Stie section
		for i in JSON['Sites']:

			# Try to send request
			try:
				# Make SiteJSON of type Site, utilize proxy servers
				SiteJSON = Site(i)
				SiteSend = Sites()

				# Send the JSON with SiteSend
				SiteSend.UpdateSite(SiteJSON)
			except Exception, e:
				return False, str(e)

	# Check for SYSTEM
	if 'Systems' in JSON:

		# Itterate through System section
		for i in JSON['Systems']:

			# Try to send request
			try:
				# Make SystemJSON of type System, utilize proxy servers
				SystemJSON = System(i)
				SystemSend = Systems()

				# Send the JSON with SystemSend
				SystemSend.UpdateSystem(SystemJSON)
			except Exception, e:
				return False, str(e)

	# Check for DEPLOYMENT
	if 'Deployments' in JSON:

		# Itterate through Deployment
		for i in JSON['Deployments']:

			# Try to send request
			try:
				# Make DeploymentJSON of type Deployment, utilize proxy servers
				DeploymentJSON = Deployment(i)
				DeploymentSend = Deployments()

				# Send the JSON with DeploymentSend
				DeploymentSend.UpdateDeployment(DeploymentJSON)
			except Exception, e:
				return False, str(e)

	# Check for COMPONENTS
	if 'Components' in JSON:

		# Itterate through Components
		for i in JSON['Components']:

			# Try to send request
			try:
				# Make ComponentJSON of type Component, utilize proxy servers
				ComponentJSON = Component(i)
				ComponentSend = Components()

				# Send the JSON with ComponentSend
				ComponentSend.UpdateComponent(ComponentJSON)
			except Exception, e:
				print str(e)
				return False, str(e)

	# Check for SERVICE ENTRIES
	if 'Service Entries' in JSON:

		# Itterate through ServiceEntries
		for i in JSON['ServiceEntries']:

			# Try to send request
			try:
				# Make ServiceEntryJSON of type ServiceEntry, utilize proxy servers
				ServiceEntriesJSON = ServiceEntry(i)
				ServiceEntriesSend = ServiceEntries()
				# Send the JSON with ServiceEntriesSend

				ServiceEntriesSend.UpdateServiceEntry(ServiceEntriesJSON)
			except Exception, e:
				print str(e)
				return False, str(e)

	# Check for DOCUMENTS
	if 'Documents' in JSON:

		# Itterate through Documents
		for i in JSON['Documents']:

			# Try to send request
			try:
				# Make DocumentJSON of type Document, utilize proxy servers
				DocumentJSON = Document(i)
				DocumentSend = Documents()

				# Send the JSON with DocumentSend
				DocumentSend.UpdateDocument(DocumentJSON)
			except Exception, e:
				print str(e)
				return False, str(e)

	return "Successful Update Of Instance(s)"

# Delete Method
@app.route('/edge/', methods=['DELETE'])
def delete():

	# Grab JSON from the request
	try:
		JSON = request.get_json()
	except Exception as e:
		print e
		return e

	# Person
	if 'People' in JSON:

		# Loop
		for i in JSON['People']:

			# Try to send request
			try:
				# Acquire Unique Identifier value
				PersonDelete = People()
				UniqueID = i['Unique Identifier']

				# Send the JSON with the Unique Identifier
				PersonDelete.DeletePerson(UniqueID)
			except Exception, e:
				print str(e)
				return False, str(e)

	# Project
	if 'Projects' in JSON:

		# Itterate through Project section
		for i in JSON['Projects']:

			# Try to send request
			try:
				# Acquire Unique Identifier value
				ProjectDelete = Projects()
				UniqueID = i['Unique Identifier']

				# Send the JSON with the Unique Identifier
				ProjectDelete.DeleteProject(UniqueID)
			except Exception, e:
				return False, str(e)

	# Check for SITE
	if 'Sites' in JSON:

		# Itterate through Stie section
		for i in JSON['Sites']:

			# Try to send request
			try:
				# Acquire Unique Identifier value
				SiteDelete = Sites()
				UniqueID = i['Unique Identifier']

				# Send the JSON with the Unique Identifier
				SiteDelete.DeleteSite(UniqueID)
			except Exception, e:
				return False, str(e)

	# Check for SYSTEM
	if 'Systems' in JSON:

		# Itterate through System section
		for i in JSON['Systems']:

			# Try to send request
			try:
				# Acquire Unique Identifier value
				SystemDelete = Systems()
				UniqueID = i['Unique Identifier']

				# Send the JSON with the Unique Identifier
				SystemDelete.DeleteSystem(UniqueID)
			except Exception, e:
				return False, str(e)

	# Check for DEPLOYMENT
	if 'Deployments' in JSON:

		# Itterate through Deployment
		for i in JSON['Deployments']:

			# Try to send request
			try:
				# Acquire Unique Identifier value
				DeploymentDelete = Deployments()
				UniqueID = i['Unique Identifier']

				# Send the JSON with the Unique Identifier
				DeploymentDelete.DeleteDeployment(UniqueID)
			except Exception, e:
				return False, str(e)

	# Check for COMPONENTS
	if 'Components' in JSON:

		# Itterate through Components
		for i in JSON['Components']:

			# Try to send request
			try:
				# Acquire Unique Identifier value
				ComponentDelete = Components()
				UniqueID = i['Unique Identifier']				

				# Send the JSON with the Unique Identifier
				ComponentDelete.DeleteComponent(UniqueID)
			except Exception, e:
				print str(e)
				return False, str(e)

	# Check for SERVICE ENTRIES
	if 'Service Entries' in JSON:

		# Itterate through ServiceEntries
		for i in JSON['ServiceEntries']:

			# Try to send request
			try:
				# Acquire Unique Identifier value
				ServiceEntriesDelete = ServiceEntries()
				UniqueID = i['Unique Identifier']

				# Send the JSON with the Unique Identifier
				ServiceEntriesDelete.DeleteServiceEntry(UniqueID)
			except Exception, e:
				print str(e)
				return False, str(e)

	# Check for DOCUMENTS
	if 'Documents' in JSON:

		# Itterate through Documents
		for i in JSON['Documents']:

			# Try to send request
			try:
				# Acquire Unique Identifier value
				DocumentDelete = Documents()
				UniqueID = i['Unique Identifier']

				# Send the JSON with DocumentSend
				DocumentDelete.DeleteDocument(UniqueID)
			except Exception, e:
				print str(e)
				return False, str(e)

	return "Successful Deletion Of Instance(s)"

# Run Main
if __name__ == '__main__':
	app.run(host='127.0.0.1',port=8089, debug= False, threaded = True)
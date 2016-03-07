# Person Class
class DisplayPerson:
	Person = ""
	UniqueID = ""
	FirstName = ""
	LastName = ""
	Phone = ""
	Email = ""
	Organization = ""
	CreationDate = ""
	ModificationDate = ""
	Photo = ""

	def __init__(self, person, uniqueid, firstname, lastname, phone, email, organization, creationdate, modificationdate, photo):
		self.Person = person
		self.UniqueID = uniqueid
		self.FirstName = firstname
		self.LastName = lastname
		self.Phone = phone
		self.Email = email
		self.Organization = organization
		self.CreationDate = creationdate
		self.ModificationDate = modificationdate
		self.Photo = photo	

	def serialize(self):
		return {
			'Person': self.Person,
			'Unique Identifier': self.UniqueID,
			'First Name': self.FirstName,
			'Last Name': self.LastName,
			'Phone': self.Phone,
			'Email': self.Email,
			'Organization': self.Organization,
			'Creation Date': self.CreationDate, 
			'Modification Date': self.ModificationDate,
			'Photo': self.Photo 
		}

# Project Class
class DisplayProject:
	Project = ""
	UniqueIdentifier = ""
	Name = ""
	InstitutionName = ""
	OriginalFundingAgency = ""
	GrantNumberString = ""
	StartedDate = ""
	CreateDate = ""
	ModificationDate = ""
	PrincipalInvestigator = ""


	def __init__(self, project, uniqueid, name, institutionname, originalfundingagency, grantnumberstring, starteddate, createdate, modificationdate, Principalinvestigator):
		self.Project = project
		self.UniqueIdentifier = uniqueid
		self.Name = name
		self.InstitutionName = institutionname
		self.OriginalFundingAgency = originalfundingagency
		self.GrantNumberString = grantnumberstring
		self.StartedDate = starteddate
		self.CreateDate = createdate
		self.ModificationDate = modificationdate
		self.PrincipalInvestigator = Principalinvestigator

	def serialize(self):
		return {
			'Project': self.Project,
			'Unique Identifier': self.UniqueIdentifier,
			'Name': self.Name,
			'Institution Name': self.InstitutionName,
			'Original Funding Agency': self.OriginalFundingAgency,
			'Grant Number String': self.GrantNumberString,
			'Started Date': self.StartedDate,
			'Create Date': self.CreateDate,
			'Modification Date': self.ModificationDate,
			'Principal Investigator': self.PrincipalInvestigator
		}

# System Class
class DisplaySystem:
	System = ""
	UniqueIdentifier = ""
	Name = ""
	Details = ""
	Power = ""
	InstallationDate = ""
	InstallationLocation = ""
	CreationDate = ""
	ModificationDate = ""
	Manager = ""
	Site = ""
	Photo = ""

	def __init__(self, system, uniqueid, name, details, power, installationdate, installationlocation, creationdate, modificationdate, manager, site, photo):
		self.UniqueIdentifier = uniqueid
		self.System = system
		self.Name = name
		self.Details = details
		self.Power = power
		self.InstallationDate = installationdate
		self.InstallationLocation = installationlocation
		self.CreationDate = creationdate
		self.ModificationDate = modificationdate
		self.Manager = manager
		self.Site = site
		self.Photo = photo

	def serialize(self):
		return {
			'Unique Identifier': self.UniqueIdentifier,
			'System': self.System,
			'Name': self.Name,
			'Details': self.Details,
			'Power': self.Power,
			'Installation Date': self.InstallationDate,
			'Installation Location': self.InstallationLocation,
			'Creation Date': self.CreationDate,
			'Modification Date': self.ModificationDate,
			'Manager': self.Manager,
			'Site': self.Site,
			'Photo': self.Photo
		}

# Document Class
class DisplayDocument:
	Document= ""
	UniqueID = ""
	Name = ""
	Notes = ""
	Path = ""
	CreationDate = ""
	ModificationDate = ""
	Project = ""
	Site = ""
	Deployment = ""
	Component = ""
	ServiceEntry = ""

	def __init__(self, document, uniqueid, name, notes, path, creationdate, modificationdate, project, site, deployment, component, serviceentry):
		self.Document = document
		self.UniqueID = uniqueid
		self.Name = name
		self.Notes = notes
		self.Path = path
		self.CreationDate = creationdate
		self.ModificationDate = modificationdate
		self.Project = project
		self.Site = site
		self.Deployment = deployment
		self.Component = component
		self.ServiceEntry = serviceentry

	def serialize(self):
		return {
			'Document': self.Document,
			'Unique Identifier': self.UniqueID,
			'Name': self.Name,
			'Notes': self.Notes,
			'Path': self.Path,
			'Creation Date': self.CreationDate,
			'Modification Date': self.ModificationDate,
			'Project': self.Project,
			'Site': self.Site,
			'Deployment': self.Deployment,
			'Component': self.Component,
			'Service Entry': self.ServiceEntry
		}
# Deployment Class
class DisplayDeployment:
	Deployment = ""
	UniqueID = ""
	Name = ""
	Purpose = ""
	CenterOffset = ""
	Latitude = ""
	Longitude = ""
	Altitude = ""
	SRID = ""
	HeightFromGround = ""
	ParentLogger = ""
	EstablishedDate = ""
	AbandonedDate = ""
	CreationDate = ""
	ModificationDate = ""
	System = ""

	def __init__(self, deployment, uniqueid, name, purpose, centeroffset, latitude, longitude, altitude, srid, heightfromground, parentlogger, establisheddate, abandoneddate, creationdate, modificationdate, system):
		self.Deployment = deployment
		self.UniqueID = uniqueid
		self.Name = name
		self.Purpose = purpose
		self.CenterOffset = centeroffset
		self.Latitude = latitude
		self.Longitude = longitude
		self.Altitude = altitude
		self.SRID = srid
		self.HeightFromGround = heightfromground
		self.ParentLogger = parentlogger
		self.EstablishedDate = establisheddate
		self.AbandonedDate = abandoneddate
		self.CreationDate = creationdate
		self.ModificationDate = modificationdate
		self.System = system

	def serialize(self):
		return{
			'Deployment': self.Deployment,
			'Unique Identifier': self.UniqueID,
			'Name': self.Name,
			'Purpose': self.Purpose,
			'CenterOffset': self.CenterOffset,
			'Latitude': self.Latitude,
			'Longitude': self.Longitude,
			'Altitude': self.Altitude,
			'SRID': self.SRID,
			'Height From Ground': self.HeightFromGround,
			'Parent Logger': self.ParentLogger,
			'Established Date': self.EstablishedDate,
			'Abandoned Date': self.AbandonedDate,
			'Creation Date': self.CreationDate,
			'Modification Date': self.ModificationDate,
			'System': self.System 
		}

# Service Entries Class
class DisplayServiceEntry:
	ServiceEntry = ""
	UniqueIdentifier = ""
	Name = ""
	Notes = ""
	Date = ""
	Operation = ""
	CreationDate = ""
	ModificationDate = ""
	Project = ""
	Creator = ""
	System = ""
	Component = ""
	Photo = ""

	def __init__(self, serviceentry, uniqueID, name, notes, date, operation, creationdate, modificationdate, project, creator, system, component, photo):
		self.ServiceEntry = serviceentry
		self.UniqueIdentifier = uniqueID
		self.Name = name
		self.Notes = notes
		self.Date = date
		self.Operation = operation
		self.CreationDate = creationdate
		self.ModificationDate = modificationdate
		self.Project = project
		self.Creator = creator
		self.System = system
		self.Component = component
		self.Photo = photo

	def serialize(self):
		return {
			'Service Entry': self.ServiceEntry,
			'Unique Identifier': self.UniqueIdentifier,
			'Name': self.Name,
			'Notes': self.Notes,
			'Date': self.Date,
			'Operation': self.Operation,
			'Creation Date': self.CreationDate,
			'Modification Date': self.ModificationDate,
			'Project': self.Project,
			'Creator': self.Creator,
			'System': self.System,
			'Component': self.Component,
			'Photo': self.Photo
		}

# Component Class
class DisplayComponent:
	Component = ""
	UniqueID = ""
	Name = ""
	Manufacturer = ""
	Model = ""
	SerialNumber = ""
	Vendor = ""
	Supplier = ""
	InstallationDate = ""
	InstallationDetails = ""
	LastCalibratedDate = ""
	WiringNotes = ""
	CreationDate = ""
	ModificationDate = ""
	Deployment = ""
	Photo = ""

	def __init__(self, component, uniqueid, name, manufacturer, model, serialnumber, vendor, supplier, installationdate, installationdetails, lastcalibrateddate, wiringnotes, creationdate, modificationdate, deployment, photo):
		self.Component = component
		self.UniqueID = uniqueid
		self.Name = name
		self.Manufacturer = manufacturer
		self.Model = model
		self.SerialNumber = serialnumber
		self.Vendor = vendor
		self.Supplier = supplier
		self.InstallationDate = installationdate
		self.InstallationDetails = installationdetails
		self.LastCalibratedDate = lastcalibrateddate
		self.WiringNotes = wiringnotes
		self.CreationDate =  creationdate
		self.ModificationDate = modificationdate
		self.Deployment = deployment
		self.Photo = photo

	def serialize(self):
		return{
			'Component': self.Component,
			'Unique Identifier': self.UniqueID,
			'Name': self.Name,
			'Manufacturer': self.Manufacturer,
			'Model': self.Model,
			'Serial Number': self.SerialNumber,
			'Vendor': self.Vendor,
			'Supplier': self.Supplier,
			'Installation Date': self.InstallationDate,
			'Installation Details': self.InstallationDetails,
			'Last Calibrated Date': self.LastCalibratedDate,
			'Wiring Notes': self.WiringNotes,
			'Creation Date': self.CreationDate,
			'Modification Date': self.ModificationDate,
			'Deployment': self.Deployment,
			'Photo': self.Photo,
		}

# Site Class
class DisplaySite:
	Site = ""
	UniqueID =""
	Name = ""
	Notes = ""
	Alias = ""
	Latitude = ""
	Longitude = ""
	Altitude = ""
	SRID = ""
	LandOwner = ""
	PermitHolder = ""
	TimeZoneName = ""
	TimeZoneAbbreviation = ""
	TimeZoneOffset = ""
	Project = ""
	GPSLandmark = ""
	LandmarkPhoto = ""

	def __init__(self, site, uniqueid, name, notes, alias, latitude, longitude, altitude, srid, landowner, permitholder, timezonename, timezoneabbreviation, timezoneoffset, project, gpslandmark, landmarkphoto):
		self.Site = site
		self.UniqueID = uniqueid
		self.Name = name
		self.Notes = notes
		self.Alias = alias
		self.Latitude = latitude
		self.Longitude = longitude
		self.Altitude = altitude
		self.SRID = srid
		self.LandOwner = landowner
		self.PermitHolder = permitholder
		self.TimeZoneName = timezonename
		self.TimeZoneAbbreviation = timezoneabbreviation
		self.TimeZoneOffset = timezoneoffset
		self.Project = project
		self.GPSLandmark = gpslandmark
		self.LandmarkPhoto = landmarkphoto

	def serialize(self):
		return{
			'Site': self.Site,
			'Unique Identifer': self.UniqueID,
			'Name': self.Name,
			'Notes': self.Notes,
			'Alias': self.Alias,
			'Latitude': self.Latitude,
			'Longitude': self.Longitude,
			'Altitude': self.Altitude,
			'SRID': self.SRID,
			'Land Owner': self.LandOwner,
			'Permit Holder': self.PermitHolder,
			'Time Zone Name': self.TimeZoneName,
			'Time Zone Abbreviation': self.TimeZoneAbbreviation,
			'Time Zone Offset': self.TimeZoneOffset,
			'Project': self.Project,
			'GPS Landmark': self.GPSLandmark,
			'Landmark Photo': self.LandmarkPhoto
		}

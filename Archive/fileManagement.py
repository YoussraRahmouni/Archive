import requests
import zipfile
import io
import tarfile
import datetime
import os
import time
import logging
from mattermost import buildPayload 
from mattermost import notifyMattermost
import shutil

#defining syntax for log file 
logging.basicConfig(filename='log.log', filemode='w', level=logging.INFO, format='%(levelname)s:%(asctime)s:%(message)s')

def getFileLink(LINK,webHook,NOTIFY):
	try:
		logging.info(' Trying to connect...')
		fileLink=requests.get(LINK)
		logging.info(' Connection successful')
		if NOTIFY:
			payload=buildPayload('File retrieval','Done')
			notifyMattermost(payload,webHook)
		return fileLink
	except requests.exceptions.RequestException as e:
		logging.error(e.strerror)
		if NOTIFY:
			payload=buildPayload('File retrieval','ERROR, review log')
			notifyMattermost(payload,webHook)

def extractFile(fileLink,webHook,NOTIFY):
	logging.info(" FUNCTION FOR FILE EXTRACTION RUNNING")
	#Create an instance of zip file 
	z=zipfile.ZipFile(io.BytesIO(fileLink.content))
	now=datetime.datetime.now()
	name=now.strftime("%Y%d%m")
	pathFolder="./"+name+"/"
	#Check if a zip folder already exists
	if os.path.exists(pathFolder):
		logging.info(' AN ARCHIVED FOR THIS FILE ALREADY EXISTS, NO FILE CREATED')
		SQL_FILE=None
	else:
		z.extractall(path=pathFolder)
		#print(z.infolist()[0].filename)
		#Extract the sql file from the zip folder
		SQL_FILE=z.infolist()[0].filename
		logging.info(' EXTRACTION SUCCESSFUL'+'filename'+SQL_FILE)
		if NOTIFY:
			payload=buildPayload('File extraction','Done')
			notifyMattermost(payload,webHook)
	return SQL_FILE

def archiveFile(SQL_FILE,webHook,NOTIFY):
	if SQL_FILE is None:
		print("Empty")
	else:
		logging.info(' ARCHIVING FILE')
		#print("ARCHIVING FILE ")
		now=datetime.datetime.now()
		#Specify the name of the zip file as YYYYDDMM
		name=now.strftime("%Y%d%m")
		logging.info("The archive name"+name)
		archiveName="/mnt/dav/"+name+".tgz"
		file_obj=tarfile.open(archiveName,"w")
		file_obj.add("./"+name+"/"+SQL_FILE)
		file_obj.close()
		logging.info( 'ARCHIVE SUCCESSFULL')
		shutil.rmtree("./"+name, ignore_errors=True)
		if NOTIFY:
			payload=buildPayload('File archive','Done')
			notifyMattermost(payload,webHook)

def manageFile(Duration,durationType,webHook,NOTIFY):
	print("looking for files")
	files=os.listdir("/mnt/dav/")
	for f in files:
		if f.endswith('.tgz'):
			print(f)
			try:
				dateCreation=datetime.datetime.strptime(time.ctime(os.path.getctime("/mnt/dav/"+f)),"%c")
				now=datetime.datetime.now()
				#Compare the date of creation of the archive with the duration from configuration file
				if dateCreation+datetime.timedelta(**{durationType: Duration})<now:
					print("should be deleted")
					print("-----------------")
					try:
						os.remove("/mnt/dav/"+f)
						logging.info( 'FILES EXCEEDING DURATION DELETED')
						if NOTIFY:
							payload=buildPayload('Files management','Done')
							notifyMattermost(payload,webHook)
					except OSError as e:
						logging.error(e.strerror)
						if NOTIFY:
							payload=buildPayload('Files management','ERROR, review log')
							notifyMattermost(payload,webHook)
			except OSError:
				logging.error("Path does not exist")
				if NOTIFY:
					payload=buildPayload('File management','ERROR, review log')
					notifyMattermost(payload,webHook)
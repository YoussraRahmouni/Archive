import requests
import json
import logging

logging.basicConfig(filename='log.log', filemode='w', level=logging.INFO, format='%(levelname)s:%(asctime)s:%(message)s')

def buildPayload(task,state):
	payload="|	Task	|	State	| \n"+"| ------------|---------------| \n"+"|	"+ task + "|	" + state +"|  \n"
	formatedPayload={'text':payload}
	return json.dumps(formatedPayload)
def notifyMattermost(message,webHook):
	try:
		headers={'Content-Type' : 'application/json'}
		#Build the request and put message in header
		r=requests.post(webHook, data=message, headers=headers)
		logging.info(r.status_code)
	except requests.exceptions.RequestException as e:
		logging.info(e.strerror)
import tools.autodialer_dev as dialer
import tools.outreach_sequencer_dev as sequencer
import tools.contact_transfer as transfer
import tools.dais_sequencer as dais
import time
import pandas as pd
import login as lg
import threading
import os


import tkinter as tk
from tkinter import *

import tkinter as tk

'''
TO DO:
1. Hook up the rest of the buttons
2. Debug the shit out of everything
2.5. Setup multithreading 
3. Set autodialer daily limits
4. Integrate the contact transferer  
5. Try REST API call to refresh databricks job for lead data
6. Make the GUI prettier
7. Build an auto-opp creator for partner submitted leads
8. Build an auto-sequener for partner submitted leads (should be pretty easy- would require an update to databricks job)
9. Run selenium headlessly 
10. Integrate dependencies and try to package/compile for cross-compatability
11. Maybe?? build a web app with UI/API and host on AWS


'''
#### CONFIG ###

chromedriver_path = "/Users/nigel.silvadallenbach/Documents/GitHub/AutoSDR_dev/chromedriver"

#Login Information: 
sfdc_username = lg.sfdc_username
sfdc_password = lg.sfdc_password

outreach_username = lg.outreach_username
outreach_password = lg.outreach_password


#Google Sheet Data Sources:
sheet_url = 'https://docs.google.com/spreadsheets/d/1Ky14MXXYyIwhan9IILfeGz2TcjXqHKuM-QKaySMwlp4/edit#gid=0'


#Autosequencer Preferences:
mql_check_cadence = 15


#Autodialer Preferences: 

calls_per_hour = 15
calls_per_day = 45
call_frequency = 3600 #seconds

titles_to_connect_on = []
max_calls_per_day = 100

def leadDataRefresh():
    lead_url = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
    leadData = pd.read_csv(lead_url)
    return leadData


'''
def dataRefresh():

	url_1 = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
	dais_url = sheet_url.replace('/edit#gid=0', '/export?format=csv&gid=917355881')


	global leadData
	global daisLeadData
	leadData = pd.read_csv(url_1)
	daisLeadData = pd.read_csv(dais_url)


	global leadEmail
	global leadCampaign
	global daisLeadEmail
	global daisLeadCampaign
	global daisLeadTemplate
	leadEmail = leadData['email']
	leadCampaign = leadData['OutreachCampaign']
	daisLeadEmail = daisLeadData['Email']
	daisLeadCampaign = daisLeadData['OutreachCampaign']
	daisLeadTemplate = daisLeadData['OutreachTemplate']

	transfer_url = sheet_url.replace('/edit#gid=0', '/export?format=csv&gid=545159304')
	sequence_url = sheet_url.replace('/edit#gid=0', '/export?format=csv&gid=1016929719')

	global contactTransfer
	global contactSequence
	
	try:
		contactTransfer = pd.read_csv(transfer_url)
		contactSequence = pd.read_csv(sequence_url)
	except Exception as e: 
		print(e)
		print('Error connecting to gsheet- check your internet connection')


	


	global contactTransferList
	
	try:
		contactTransferList = contactTransfer['Id'].values.tolist()
		print(contactTransferList)

	except Exception as e:
		print(e)

		
	global numLeads
	global numContactsSeq
	
	try:
		numLeads = len(leadData['email'].values.tolist())
		numContactsSeq = len(contactSequence['email'].values.tolist())

		prospectCountText.set(f"Number of leads: {numLeads}\nNumber of contacts: {numContactsSeq}")

	except Exception as e:
		print(e)

    return
'''
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
openProspectQueue = 'https://docs.google.com/spreadsheets/d/1Ky14MXXYyIwhan9IILfeGz2TcjXqHKuM-QKaySMwlp4/edit#gid=0'


#Autosequencer Preferences:
mql_check_cadence = 15


#Autodialer Preferences: 

calls_per_hour = 15
calls_per_day = 45
call_frequency = 3600 #seconds

titles_to_connect_on = []
max_calls_per_day = 100






#DEFINE FUNCTIONS 

def createList(r1, r2):
    return list(range(r1, r2+1))
      
# Driver Code
r1, r2 = 0, 12
gridCount = createList(r1, r2)


def leadAndContactRefresh():

	sheet_url = openProspectQueue
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

def sequenceLogic():
	try: 
		if numLeads > numContactsSeq or numLeads == numContactsSeq:
			print('Sequencing leads')
			sequencer.autoSequencer(outreach_username, outreach_password, leadEmail, leadCampaign, chromedriver_path, prospectCountText, numLeads, numContactsSeq, window)
			numLeads.pop(0)
			print(numLeads)
			prospectCountText.set(f"Number of leads: {numLeads}\nNumber of contacts: {numContactsSeq}")
			window.update

		elif numLeads < numContactsSeq:
			print('Sequencing contacts')
			sequencer.autoSequencer(outreach_username, outreach_password, contactSequenceEmail, contactSequenceCampaign, chromedriver_path)
			numContactsSeq.pop(0)
			print(numContactsSeq)
			prospectCountText.set(f"Number of leads: {numLeads}\nNumber of contacts: {numContactsSeq}")
			window.update

		else: 
			print('All leads and contacts have been sequenced')

	except Exception as e:
		print(e)


def startAutoDialer():
	dialer.autodialer(outreach_username, outreach_password, max_calls_per_day)

def startContactTransferFunc():
	transfer.contactTransferTool(sfdc_username, sfdc_password, contactTransferList)


def autopilot():
	print('Under development')

def daisSequenceFunc():
	dais.autoSequencer(outreach_username, outreach_password, daisLeadEmail, daisLeadCampaign, daisLeadTemplate, chromedriver_path, numLeads)


def main():

	#DRAW GUI

	window = tk.Tk(className = ' AutoSDR Development Version (v2.01)')
	window.columnconfigure(gridCount, minsize=10)
	window.rowconfigure(gridCount, minsize=10)

	#Draw labels

	prospectCountText = StringVar()
	prospectCountText.set("Number of leads: --\nNumber of contacts: --")

	header = tk.Label(text="AutoSDR - Tool Box", font=("Arial", 25))
	header.grid(row=0, column=1, sticky="se", pady=5)

	prospectCount = tk.Label(textvariable=prospectCountText, justify='left')
	prospectCount.grid(row=1, column=0)

	dailyCallCountText = StringVar()
	dailyCallCountText.set("Number of calls (day):\nNumber of calls (week):")

	dailyCallCount = tk.Label(textvariable=dailyCallCountText, justify='left')
	dailyCallCount.grid(row=1, column=1)

	actionCountText = StringVar()
	actionCountText.set("Current Action:\nNext Action:")

	actionCount = tk.Label(textvariable=actionCountText, justify='left')
	actionCount.grid(row=1, column=2)


	#create buttons 
	sequenceButton = tk.Button(
		text="Sequence Prospects",
		width=15,
		height=5,
		fg="black",
		command=sequenceLogic,
	)

	sequenceButton.grid(row=3, column=0)

	callButton = tk.Button(
		text="Call Prospects",
		width=15,
		height=5,
		fg="black",
		command=startAutoDialer,
	)

	callButton.grid(row=3, column=1)

	transferButton = tk.Button(
		text="Transfer Contacts",
		width=15,
		height=5,
		fg="black",
		command=startContactTransferFunc,
	)

	transferButton.grid(row=3, column=2)

	refreshButton = tk.Button(
		text="Manually Refresh Data",
		width=15,
		height=5,
		fg="black",
		command=leadAndContactRefresh,
	)

	refreshButton.grid(row=4, column=0)

	autoPilotButton = tk.Button(
		text="Autopilot",
		width=15,
		height=5,
		fg="black",
		command=autopilot,
	)

	autoPilotButton.grid(row=4, column=1)

	sequencePartnerLeads = tk.Button(
		text="Sequence Partner Leads",
		width=15,
		height=5,
		fg="black",
	)

	sequencePartnerLeads.grid(row=4, column=2)

	partnerOppCreator = tk.Button(
		text="Create Partner Opps",
		width=15,
		height=5,
		fg="black",
	)

	partnerOppCreator.grid(row=4, column=3)

	daisSequencer = tk.Button(
		text="Sequence DAIS Leads",
		width=15,
		height=5,
		fg="black",
		command=daisSequenceFunc,
	)

	daisSequencer.grid(row=3, column=3)

	#Call refresh to populate initial data
	#leadAndContactRefresh()

	window.update
	window.mainloop()


if __name__ == '__main__':
	main()









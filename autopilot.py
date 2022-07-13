import tools.autodialer_dev as dialer
import tools.outreach_sequencer_dev_functions as sq
import tools.contact_transfer as transfer
import time
import pandas as pd
import login as lg

#Login Information: 
sfdc_username = lg.sfdc_username
sfdc_password = lg.sfdc_password

outreach_username = lg.outreach_username
outreach_password = lg.outreach_password

def autopilot():

	try:
		sq.outreachLogin(outreach_username, outreach_password)
	except Exception as e:
		print(f'Error occurred during outreachLogin sequence:\n{e}')

	try:	
		sq.outreachSequenceProfile(campaign)
	except Exception as e:
		print(f'Error occurred during outreachLogin sequence:\n{e}')
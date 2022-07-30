import tools.autodialer_dev as dialer
import tools.outreach_sequencer_dev as sequencer
import tools.contact_transfer as transfer
import tools.dais_sequencer as dais
import time
import pandas as pd
import login as lg
import threading
import os, logging
from databricks import sql


import tkinter as tk
from tkinter import *

import tkinter as tk


# --------------------------------- TO-DO ---------------------------------
# Debug the shit out of everything
# Integrate the contact transferer  
# Try REST API call to refresh databricks job for lead data
# Build an auto-opp creator for partner submitted leads
# Run selenium headlessly 
# Integrate dependencies and try to package/compile for cross-compatability



# --------------------------------- CONFIGURATION ---------------------------------

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


def startAutoDialer():
	dialer.autodialer(outreach_username, outreach_password, max_calls_per_day)


# --------------------------------- DATABRICKS SQL CONNECTOR ---------------------------------

def dbsql_init():
    connection = sql.connect(server_hostname = lg.DATABRICKS_SERVER_HOSTNAME,
                            http_path = lg.DATABRICKS_HTTP_PATH,
                            access_token = lg.DATABRICKS_TOKEN)
    return connection

def dbsql_kill(cursor, connection):
    cursor.close()
    connection.close()


# --------------------------------- DATA FUNCTIONS ---------------------------------

"""
class leadData():
    def __init__(self, email, campaign):
        self.email = email
        self.campaign = campaign
"""

def dbsql_leadrefresh(window):

    print('Initializing DB SQL Connection...')
    connection = dbsql_init()
    cursor = connection.cursor()
    
    print('Executing SQL Query...')
    cursor.execute('SELECT * FROM nigel.openleadqueue')
    
    result = cursor.fetchall()
    
    email = [row.email for row in result]
    campaign = [row.OutreachCampaign for row in result]

#    leadResult = {email[i]: campaign[i] for i in range(len(email))} - Need to refactor code to accept a dict instead of two lists

    window['-LEAD LIST-'].update(email)
    window['lenLeadList'].update(f'Number of Leads: {len(email)}')

    print('Terminating DB SQL Connection')
    dbsql_kill(cursor, connection)

    return email, campaign



def dbsql_contactrefresh(window):

    print('Initializing DB SQL Connection...')
    connection = dbsql_init()


    cursor = connection.cursor()
    
    print('Executing SQL Query...')
    cursor.execute('SELECT * FROM nigel.OpenContactQueue')
    
    result = cursor.fetchall()
    
    contactEmails = [row.email for row in result]

    print(contactEmails)

    window['-CONTACT LIST-'].update(contactEmails)
    window['lenContactList'].update(f'Number of Leads: {len(contactEmails)}')

    print('Executing 2nd Contact SQL Query...')
    cursor.execute('SELECT * FROM nigel.contactTransferList')
    
    result = cursor.fetchall()
    
    contactEmails = [row.Email for row in result]

    print(contactEmails)

    window['-CONTACT TRANSFER LIST-'].update(contactEmails)
    window['lenContactTransferList'].update(f'Number of Leads: {len(contactEmails)}')

    print('Terminating DB SQL Connection')

    dbsql_kill(cursor, connection)



def dbsql_daisrefresh(window):

    print('Initializing DB SQL Connection...')
    connection = dbsql_init()


    cursor = connection.cursor()
    
    print('Executing SQL Query...')
    cursor.execute('SELECT * FROM nigel.OpenDAISQueue')
    
    result = cursor.fetchall()
    
    daisEmails = [row.Email for row in result]

    print(daisEmails)

    window['-DAIS LIST-'].update(daisEmails)
    window['lenDaisList'].update(f'Number of Leads: {len(daisEmails)}')

    print('Terminating DB SQL Connection')

    dbsql_kill(cursor, connection)



def dbsql_suspectrefresh(window):

    print('Initializing DB SQL Connection...')
    connection = dbsql_init()


    cursor = connection.cursor()
    
    print('Executing SQL Query...')
    cursor.execute('SELECT * FROM nigel.suspectLeadQueue limit 100')
    
    result = cursor.fetchall()
    
    suspectEmails = [row.Email for row in result]

    print(suspectEmails)

    window['-SUSPECT LIST-'].update(suspectEmails)
    window['lenSuspectList'].update(f'Number of Leads: {len(suspectEmails)}')

    print('Terminating DB SQL Connection')

    dbsql_kill(cursor, connection)



def dbsql_refresh_all(window):
    dbsql_leadrefresh(window)
    dbsql_contactrefresh(window)
    dbsql_suspectrefresh(window)
    dbsql_daisrefresh(window)
    print('All lists have been refreshed.')


def testfunction(window):
    pass

def sequence_leads(window):
    email, campaign = dbsql_leadrefresh(window)
    sequencer.autoSequencer(outreach_username, outreach_password, email, campaign, chromedriver_path)

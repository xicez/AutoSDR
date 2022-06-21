# TO-DO:
# - SET UP EMAIL/TEXT ALERTS WHEN THE RUN FAILS
# - LOAD LOG DATA BACK INTO GSHEET, CREATE A DELTA TABLE LOG AND JOB TO CROSS-CHECK FOR CORRECTNESS
# - FIX NIGEL - BUSY ISSUE
# - TURN INTO MODULE AND BUILD A CONTROL FILE TO MANAGE TIME AND TASKS



from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

import time
from time import perf_counter
import clock
import getpass
import pandas as pd


# INITIALIZE VARIABLES

delay = 0
time_left = 60
x = 0
actionLog = []
totalTime = []

# COLLECT SFDC USERNAME/PASSWORD - REMOVE PASS BEFORE POSTING TO GITHUB

email = 'nigel.silvadallenbach@databricks.com'
password = ''


# COLLECT DATA FROM GSHEET FOR LATEST OPEN LEAD QUEUE 

sheet_url = "https://docs.google.com/spreadsheets/d/1Ky14MXXYyIwhan9IILfeGz2TcjXqHKuM-QKaySMwlp4/edit#gid=0"
url_1 = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')

df = pd.read_csv(url_1)

leadEmails = df['email']
print(leadEmails)


# INITIALIZE BROWSER DRIVER

def launchBrowser():
	chrome_options = Options()
	chrome_options.binary_location="C:/Program Files/Google/Chrome/Application/chrome.exe"
	chrome_options.add_argument("start-maximized");
	chrome_options.add_argument("--use-fake-device-for-media-stream");
	chrome_options.add_argument("--use-fake-ui-for-media-stream")
	driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="C:/Users/nigel/OneDrive/Desktop/AutoSDR/chromedriver.exe")

	driver.get('https://app1a.outreach.io/360')

	driver.title #=> "Google"

	driver.implicitly_wait(5)
	return driver

driver = launchBrowser()
print('Webdriver launched')


#Log in to Outreach
email_input = driver.find_element(By.XPATH, '//input[@id="user_email"]')
email_input.send_keys(email)
ActionChains(driver).move_to_element(email_input).key_down(Keys.RETURN).key_up(Keys.RETURN).perform()

password_input = driver.find_element(By.XPATH, '//input[@id="user_password"]')
password_input.send_keys(password)
ActionChains(driver).move_to_element(password_input).key_down(Keys.RETURN).key_up(Keys.RETURN).perform()

#Sequence leads in the lead list

for lead in leadEmails:
	
	print(x)
	print(lead)
	campaign = df['OutreachCampaign'][x]
	print(campaign)

	start_time = perf_counter()

	driver.switch_to.default_content()

#	for i in range(0,3):
#		try:
	search_button = driver.find_element(By.XPATH, "//i[@class='_3XP4tseTH1-F62Cg-zWwDx _2fZKQSDZC30Tb9NpVwNcBc _13bB5RjyTUrFyaxtvHghsD']")
	search_button.click()

	search_input = driver.find_element(By.XPATH, "//input[@placeholder='Search']")
	search_input.send_keys(lead)
	ActionChains(driver).move_to_element(search_input).key_down(Keys.RETURN).key_up(Keys.RETURN).perform()

	prospect_name = driver.find_element(By.XPATH, "//div[@class='_3H5qkVK0pC9Dnnch1YhgKI']")
	ActionChains(driver).move_to_element(prospect_name).click().perform()

	sequence_button = driver.find_element(By.XPATH, "//button[@class='sequence icon-button _1ylTesnUFCUoPnsDHUtF0P _2bFSp1_3O05dzYHWllrXO0 IEU0ZeP2iAN3PQHapRWyS _1R80yfDPFuM38JpsKWXGAb _2cnlnJABAd45c0XvaZNlQY']")
	sequence_button.click()

	time.sleep(3)
#		except:
#			print('Trying again..')
#			continue
#		break

	try:	
		#iframe switch for modal popup:
		iframe_modal = driver.find_element(By.XPATH, "//iframe[contains(@title,'Outreach modal')]")
		driver.switch_to.frame(iframe_modal)

		time.sleep(3)
	except:
		continue


#	for i in range(0,3):
#		try:
	sequenceFilter = driver.find_element(By.XPATH, "//input[@aria-label='Filter sequences']")
	sequenceFilter.click()

	time.sleep(2)
	ActionChains(driver).move_to_element(sequenceFilter).send_keys(campaign).perform()
	time.sleep(1)

	selectedSequence = driver.find_element(By.XPATH, "//span[@class='MuiTypography-root MuiTypography-displayBlock']")
	selectedSequenceTitle = selectedSequence.get_attribute('title')
	selectedSequenceClick = driver.find_element(By.XPATH, "//div[@class='MuiListItemText-root MuiListItemText-multiline']")
	print(f"Sequenced displayed: {selectedSequenceTitle}")
	print(campaign)

	if campaign.lower() == selectedSequenceTitle.lower():
			print('Sequence is correct, continuing')
			selectedSequenceClick.click()
	else:
		while campaign.lower() != selectedSequenceTitle.lower():
			print('Sequence filter error, retrying')
			sequenceFilter.click()
			ActionChains(driver).move_to_element(sequenceFilter).key_down(Keys.CONTROL).key_down('A').key_up(Keys.CONTROL).key_up('A').send_keys(Keys.DELETE).perform()
			time.sleep(1)
			ActionChains(driver).move_to_element(sequenceFilter).send_keys(campaign).perform()

		selectedSequenceClick.click()

	time.sleep(3)

	try:

		addToSequenceButton = driver.find_element(By.XPATH, "//p[text()='Add to sequence']")
		addToSequenceButton.click()

		time.sleep(3)

	except Exception as e:
		print(e)
		break

	try:
		final_message = driver.find_element(By.XPATH, "//p[@class='MuiTypography-root MuiTypography-body1 MuiTypography-colorTextSecondary MuiTypography-alignCenter']")
		stop_time = perf_counter()
		elapsedTime = stop_time-start_time
		prospectLog = (f"LEAD: {lead} | RESULT: {final_message.text}, | TIME ELAPSED: {elapsedTime}")
		print(prospectLog)
		actionLog.append(prospectLog)
		totalTime.append(elapsedTime)
	except NoSuchElementException as e: 
		print(e)
		print("LEAD: "+lead+" | RESULT: UNKNOWN ERROR, SKIPPED")
		actionLog.append("LEAD: "+lead+" | RESULT: UNKNOWN ERROR, SKIPPED")

	time.sleep(1.5)

	ActionChains(driver).key_down(Keys.ESCAPE).key_up(Keys.ESCAPE).perform()

	x += 1


for a in actionLog:
	print(a)

print(f"Total elapsed time: {sum(totalTime)}")

time.sleep(1000)
'''
okta_username = driver.find_element(By.NAME, 'username')
okta_password_field = driver.find_element(By.NAME, 'password')
okta_login_button = driver.find_element(By.ID, 'okta-signin-submit')

okta_username.send_keys(sfdc_username_input)
okta_password_field.send_keys(password)
okta_login_button.click()

okta_push_button = driver.find_element(By.XPATH, '//*[@value="Send Push"]')
okta_push_button.click()

print('Okta notification sent. Press any key to continue...')
skip = input()


'''


# CONTACT TRANSFERS #

# LOOP THROUGH ALL CONTACTS AND CREATE A LIST WITH THE NAMES OF EACH CONTACT
'''
print('Opening all contacts in the list in a new tab')
sfdc_contacts_grid = driver.find_elements(By.XPATH, '//div[@class="x-grid3-cell-inner x-grid3-col-FULL_NAME"]')

contacts = []
for contact in sfdc_contacts_grid:
	contacts.append(contact.text)
	print('Adding ' + str(contact.text) + ' to list.')
print('Done verifying contact names..opening contacts')

# OPEN EACH CONTACT IN A NEW TAB

for i in contacts:
	contact_name_link = driver.find_element(By.XPATH, '//a[normalize-space()="' + i + '"]')
	print('Opening ' + i)
	ActionChains(driver).move_to_element(contact_name_link).key_down(Keys.COMMAND).click(contact_name_link).key_up(Keys.COMMAND).perform()
	time.sleep(2)

print('Done opening contacts.. pausing for pageload')
time.sleep(10) 




# SWITCH TO NEXT WINDOW AND GRAB THE MATCHED ACCOUNT SDR, IF NONE GRAB THE MATCHED ACCOUNT AE 
windows = driver.window_handles
driver.switch_to.window(windows[1])

def closeTab():
	driver.find_element(By.ID, 'AppBodyHeader').send_keys(Keys.COMMAND + 'w') 

var = 1
actions_taken = []

for window in windows:
	try:

		driver.switch_to.window(windows[var])

		time.sleep(5)
		close_sfdc_bullshit = driver.find_element(By.ID, 'tryLexDialogX')
		close_sfdc_bullshit.click()
			
		matched_account_sdr = driver.find_element(By.XPATH, '//div[@id="00N6100000IJnrJ_ileinner"]').text
		matched_account_ae = driver.find_element(By.XPATH, '//div[@id="00N6100000IRSgp_ileinner"]').text

		print('Matched account SDR is: ' + matched_account_sdr)
		print('Matched Account Executive is: ' + matched_account_ae)

		change_owner = driver.find_element(By.XPATH, '//a[normalize-space()="[Change]"]')
		change_owner.click()
		time.sleep(3)

		change_owner_input = driver.find_element(By.XPATH, '//input[@id="newOwn"]')
		change_owner_confirm = driver.find_element(By.XPATH, "//input[@title='Save']")
		
		if matched_account_sdr != '':

			# TRANSFER CONTACT TO THE SDR
			change_owner_input.send_keys(matched_account_sdr)
			change_owner_confirm.click()
			
			# TODO - ERROR HANDLING/VALIDATION:

			actions_taken.append('ACTION: TRANSFER CONTACT TO SDR | ' + 'SDR: ' + matched_account_sdr + ' | STATUS: SUCCESS')
			

			time.sleep(5)
			var = var + 1
			driver.close()
			continue

		elif matched_account_ae != '':

			# TRANSFER CONTACT TO THE AE
			change_owner_input.send_keys(matched_account_ae)
			change_owner_confirm.click()

			# TODO - ERROR HANDLING/VALIDATION:

			actions_taken.append('ACTION: TRANSFER CONTACT TO AE | ' + 'AE: ' + matched_account_ae + ' | STATUS: SUCCESS')

			time.sleep(5)
			var = var + 1
			driver.close()

			continue
		else:
			print('This contact does not have an SDR or AE')
			var = var + 1
			driver.close()
			continue
	except IndexError:
		print('All contacts have been transferred.')

		print('The following actions were performed:')
		for i in actions_taken:
			index = 0
			print(actions_taken[index])
			index = index + 1

'''
'''
'''

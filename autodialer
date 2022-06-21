# SELENIUM IMPORTS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


# OTHER IMPORTS
import time
import getpass
import pandas as pd


# INITIALIZE VARIABLES

delay = 0
time_left = 60


# COLLECT SFDC USERNAME/PASSWORD - REMOVE PASS BEFORE POSTING TO GITHUB

email = 'nigel.silvadallenbach@databricks.com'
password = ''


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


startTasks = driver.find_element(By.XPATH, "//span[@class='button-component__label']")
startTasks.click()

time.sleep(1)


i = 0
s = 0

while True: 

	print('Starting loop')
	time.sleep(1)
	prospectTitle = driver.find_element(By.XPATH, "//p[@class='_1FT0XN4xrzF8j9wPq1IqDO _3u0Wl3UJGUK9nrLY-1xojN _2XsPmEmzO0oSdPWsbZQeSO']")
	print(f'Prospect title identified as: {prospectTitle.text}')

	badNum = False

#check if a number exists, if not skip the task
	try:
	
		print('Calling prospect')
		callButton = driver.find_element(By.XPATH, "//i[@class='_3IgMsURK-3b6bjwARPmD2_ _3XP4tseTH1-F62Cg-zWwDx Z8ma2hjVe2tPmJQ3Ppmmi _13bB5RjyTUrFyaxtvHghsD']")
		callButton.click()

	except NoSuchElementException:	
		s = s + 1
		print(f'Skipping Call | Total Skipped: {s}')
		nextTask = driver.find_element(By.XPATH, "//button[@class='caret-dropdown-button _1ylTesnUFCUoPnsDHUtF0P _22hSpbFmuiQ8R9QbO4ZqTX _1Ay9MEQX3iXqrw2cxxIbzo _1gXXlmROaFHLoEi6CKsXd6 _6HZaoxWJnRcfE95dytvs_ dropdown-button _10WN_uTvYhxSNagSvGB4n8']//i[@class='_3ExX8qM26_trEsvweUZWmM _3XP4tseTH1-F62Cg-zWwDx _1-DCZzScVz9s0VMOIYyDg2 _13bB5RjyTUrFyaxtvHghsD']")
		nextTask.click()
		try:
			skipStep = driver.find_element(By.XPATH, "//span[normalize-space()='Skip Step']")
			skipStep.click()
		except NoSuchElementException:
			print('Deleting Step')
			delStep = driver.find_element(By.XPATH, "//span[normalize-space()='Delete']")
			delStep.click() 
		continue


	time.sleep(3)

	print('Switching to iFrame')
	#iframe switch for modal popup:
	dialerFrame = driver.find_element(By.XPATH, "//iframe[contains(@title,'Outreach dialer')]")
	driver.switch_to.frame(dialerFrame)

	try:
		print('Checking for bad number')
		callAnyway = driver.find_element(By.XPATH, "//button[@aria-label='Call anyway']")
		callAnyway.click()
		badNum = True

		time.sleep(3)
	except: 
		print('No bad number, passing')
		pass

	try:
		print('Trying to hang up on prospect')
		endCallButton = driver.find_element(By.XPATH, "//button[@aria-label='Hangup']")
		endCallButton.click()
	except (NoSuchElementException, StaleElementReferenceException) as error: 
		print('No hangup button, passing')


	time.sleep(1)

	print('Debug: switching to default content')
	driver.switch_to.default_content()

	print(f'Checking for badNum = {badNum}')
	if badNum == True:
		print(f'badNum = {badNum} | Logging Call - Bad Number')
		dropdown = driver.find_element(By.XPATH, "//div[@data-test-id='autocomplete-component_callDisposition_value']//input[@id='model-autocomplete-input-element']")
		dropdown.click()
		time.sleep(0.75)
		dropdown.send_keys('Call - Bad Number')
		time.sleep(0.75)
		dropdown.send_keys(Keys.RETURN)

		time.sleep(0.5)
	elif 'student' in prospectTitle.text: 
		print('Student | Logging Call - Connect')
		dropdown = driver.find_element(By.XPATH, "//div[@data-test-id='autocomplete-component_callDisposition_value']//input[@id='model-autocomplete-input-element']")
		dropdown.click()
		time.sleep(0.75)
		dropdown.send_keys('Call - Connect')
		time.sleep(0.75)
		dropdown.send_keys(Keys.RETURN)

		time.sleep(0.5)
	else:
		print('Logging Call - No Answer')
		dropdown = driver.find_element(By.XPATH, "//div[@data-test-id='autocomplete-component_callDisposition_value']//input[@id='model-autocomplete-input-element']")
		dropdown.click()
		time.sleep(0.75)
		dropdown.send_keys('Call No Answer')
		time.sleep(0.75)
		dropdown.send_keys(Keys.RETURN)

		time.sleep(0.5)			

	i = i +1
	print(f'Logged Call | Total Calls: {i}')

	logCall = driver.find_element(By.XPATH, "//span[contains(text(),'Log Call & Complete')]")
	logCall.click()
	time.sleep(0.75)


'''
#Sequence leads in the lead list

for lead in leads:

	driver.get('https://app1a.outreach.io/prospects?search='+lead)
	time.sleep(3)

#	for i in range(0,3):
#		try:
	print('Grabbing prospect link')
	prospect_name = driver.find_element(By.XPATH, "//a[contains(@href, '/prospects/')]")
	prospectLink = prospect_name.get_attribute('href')
	print(prospectLink)

'''
'''
	try:	
		#iframe switch for modal popup:
		iframe_modal = driver.find_element(By.XPATH, "//iframe[contains(@title,'Outreach modal')]")
		driver.switch_to.frame(iframe_modal)

		time.sleep(3)
	except:
		continue

	for i in range(0,3):
		try:
			sequenceFilter = driver.find_element(By.XPATH, "//div[@class='MuiAutocomplete-root jss51 jss42 MuiAutocomplete-hasClearIcon']")
			sequenceFilter.click()

			print('Pausing 2 seconds')
			time.sleep(2)
			ActionChains(driver).move_to_element(sequenceFilter).send_keys(leads[lead]).perform()
			time.sleep(1)

			selectedSequence = driver.find_element(By.XPATH, "//div[@class='MuiListItemText-root MuiListItemText-multiline']")
		except:
			print('Retrying code block')
			continue
		break


	try:
		if leads[lead] in selectedSequence.text is True:
				print('Sequence is correct, continuing')
				selectedSequence.click()
		else:
			while leads[lead] in selectedSequence.text is False:
				print('Sequence filter error, retrying')
				sequenceFilter.click()
				ActionChains(driver).move_to_element(sequenceFilter).send_keys(leads[lead]).perform()
				continue
			selectedSequence.click()

		time.sleep(3)
	except:
		continue

	try:

		addToSequenceButton = driver.find_element(By.XPATH, "//button[@class='MuiButtonBase-root MuiButton-root jss28 MuiButton-contained MuiButton-containedPrimary MuiButton-disableElevation']")
		addToSequenceButton.click()

		time.sleep(3)

	except:
		continue

	try:
		final_message = driver.find_element(By.XPATH, "//p[@class='MuiTypography-root MuiTypography-body1 MuiTypography-colorTextSecondary MuiTypography-alignCenter']")
		print("LEAD: "+lead+" | RESULT: "+final_message.text)
	except: 
		print("LEAD: "+lead+" | RESULT: ERROR, SKIPPED")

	time.sleep(1.5)

'''
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
'''
'''

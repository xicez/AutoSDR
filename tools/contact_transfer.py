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
import getpass

# INITIALIZE VARIABLES

delay = 0
time_left = 60


# INITIALIZE BROWSER DRIVER
def contactTransferTool(sfdc_username_input, password, contactTransferList):
	def launchBrowser():
		chrome_options = Options()
		chrome_options.binary_location="../Google Chrome"
		chrome_options.add_argument("start-maximized");
		driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

		driver.get("https://databricks.my.salesforce.com/")

		driver.title #=> "Google"

		driver.implicitly_wait(5)
		return driver

	driver = launchBrowser()
	print('Webdriver launched')

	#OKTA VERIFICATION 

	okta_button = driver.find_element(By.XPATH, '//button[@class="button mb24 secondary wide"]')
	okta_button.click()

	okta_username = driver.find_element(By.NAME, 'username')
	okta_password_field = driver.find_element(By.NAME, 'password')
	okta_login_button = driver.find_element(By.ID, 'okta-signin-submit')

	okta_username.send_keys(sfdc_username_input)
	okta_password_field.send_keys(password)
	okta_login_button.click()

	okta_push_button = driver.find_element(By.XPATH, '//*[@value="Send Push"]')
	okta_push_button.click()

	print('Okta notification sent. Pausing')
	skip = input()


	# CONTACT TRANSFERS #

	# LOOP THROUGH ALL CONTACTS AND CREATE A LIST WITH THE NAMES OF EACH CONTACT

	for contactId in contactTransferList:
		try:
			driver.get(f'https://databricks.my.salesforce.com/{contactId}')

			try:
				time.sleep(5)
				close_sfdc_bullshit = driver.find_element(By.ID, 'tryLexDialogX')
				close_sfdc_bullshit.click()
			except NoSuchElementException:
				continue

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


				time.sleep(5)
				driver.close()
				continue

			elif matched_account_ae != '':

				# TRANSFER CONTACT TO THE AE
				change_owner_input.send_keys(matched_account_ae)
				change_owner_confirm.click()

				# TODO - ERROR HANDLING/VALIDATION:


				time.sleep(5)
				driver.close()

				continue
			else:
				print('This contact does not have an SDR or AE')
				driver.close()
				continue
		except IndexError:
			print('All contacts have been transferred.')

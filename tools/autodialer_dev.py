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

def take_screenshot(driver):
	print('Taking Screenshot')
	driver.get_screenshot_as_file("autodialer_latest.png")



def autodialer(email, password, max_calls_hour):
	i = 0
	s = 0
	while i < max_calls_hour:

		# INITIALIZE BROWSER DRIVER

		def launchBrowser():
			chrome_options = Options()
			chrome_options.binary_location="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
			chrome_options.add_argument("start-maximized");
			chrome_options.add_argument("--use-fake-device-for-media-stream");
			chrome_options.add_argument("--use-fake-ui-for-media-stream")
			driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="/Users/nigel.silvadallenbach/Documents/GitHub/AutoSDR_dev/chromedriver")

			driver.get('https://app1a.outreach.io/360')

			driver.title #=> "Google"

			driver.implicitly_wait(5)
			return driver

		driver = launchBrowser()
		print('Webdriver launched')

		#Log in to Outreach
		take_screenshot(driver)
		email_input = driver.find_element(By.XPATH, '//input[@id="user_email"]')
		email_input.send_keys(email)
		ActionChains(driver).move_to_element(email_input).key_down(Keys.RETURN).key_up(Keys.RETURN).perform()

		password_input = driver.find_element(By.XPATH, '//input[@id="user_password"]')
		password_input.send_keys(password)
		ActionChains(driver).move_to_element(password_input).key_down(Keys.RETURN).key_up(Keys.RETURN).perform()


		startTasks = driver.find_element(By.XPATH, "//span[@class='button-component__label']")
		startTasks.click()

		time.sleep(1)


		while True: 

			take_screenshot(driver)
			print('Starting loop')
			time.sleep(1)
			prospectTitle = driver.find_element(By.XPATH, "//p[@class='_1FT0XN4xrzF8j9wPq1IqDO _3u0Wl3UJGUK9nrLY-1xojN _2XsPmEmzO0oSdPWsbZQeSO']")
			print(f'Prospect title identified as: {prospectTitle.text}')

			badNum = False

		#check if a number exists, if not skip the task
			try:
				take_screenshot(driver)
				print('Calling prospect')
				callButton = driver.find_element(By.XPATH, "//i[@class='_3IgMsURK-3b6bjwARPmD2_ _3XP4tseTH1-F62Cg-zWwDx Z8ma2hjVe2tPmJQ3Ppmmi _13bB5RjyTUrFyaxtvHghsD']")
				callButton.click()

			except NoSuchElementException:
				take_screenshot(driver)	
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
			take_screenshot(driver)
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

			i += 1
			print(f'Logged Call | Total Calls: {i}')
			take_screenshot(driver)
			logCall = driver.find_element(By.XPATH, "//span[contains(text(),'Log Call & Complete')]")
			logCall.click()
			time.sleep(0.75)
	print('---- Max hourly call limit reached ----')	


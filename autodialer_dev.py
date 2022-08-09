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
from selenium.webdriver.support.color import Color


# OTHER IMPORTS
import time
import getpass
import pandas as pd


# INITIALIZE VARIABLES

delay = 0
time_left = 60


def autodialer(email, password, max_calls_hour):
	i = 0
	s = 0
	while i < max_calls_hour:

		# INITIALIZE BROWSER DRIVER

		def launchBrowser():
			chrome_options = Options()
			chrome_options.binary_location="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
			chrome_options.add_argument("start-maximized");
			#chrome_options.add_argument("--use-fake-device-for-media-stream");
			#chrome_options.add_argument("--use-fake-ui-for-media-stream")
			chrome_options.add_argument("user-data-dir=//Applications/tmp/Google Chrome Dev"); # 
		
			driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="/Users/hosea.kidane/Downloads/AutoSDR-main/chromedriver")

			driver.get('https://app1a.outreach.io/360')

			driver.title #=> "Google"

			driver.implicitly_wait(20) 
			return driver

		driver = launchBrowser()
		print('Webdriver launched')

		#Log in to Outreach (not needed if using chrome instance with a saved profile)
		# email_input = driver.find_element(By.XPATH, '//input[@id="user_email"]')
		# email_input.send_keys(email)
		# ActionChains(driver).move_to_element(email_input).key_down(Keys.RETURN).key_up(Keys.RETURN).perform()

		# password_input = driver.find_element(By.XPATH, '//input[@id="user_password"]')
		# password_input.send_keys(password)
		# ActionChains(driver).move_to_element(password_input).key_down(Keys.RETURN).key_up(Keys.RETURN).perform()
		
		time.sleep(2)
		driver.implicitly_wait(30) # HK changed from time.sleep to implicit wait 

		startTasks = driver.find_element(By.CLASS_NAME, "button-component__label")
		startTasks.click()

		driver.implicitly_wait(30) # HK changed from time.sleep to implicit wait


		while True: 

			print('Starting loop')
			time.sleep(1)
			prospectTitle = driver.find_element(By.XPATH, "//p[@class='_1FT0XN4xrzF8j9wPq1IqDO _3u0Wl3UJGUK9nrLY-1xojN _2XsPmEmzO0oSdPWsbZQeSO']")
			print(f'Prospect title identified as: {prospectTitle.text}')
			
			# splitting title in list for double call feature later
			titlestring = prospectTitle.text.lower()
			titlelist = titlestring.split(" ")
			print(titlestring)
			print(titlelist)

			badNum = False
		# skip bad numbers
			
			try:

				callcolorelement = driver.find_element(By.XPATH, "//*[@id='task-flow-log-call-form']/div[3]/div/div/div/div[1]/div/label/div[2]/div/div/div/button")
				callcolor = callcolorelement.value_of_css_property("background-color")
				print(callcolor)
				hexcolor = Color.from_string(callcolor).hex
				print(hexcolor)
			
			
				if hexcolor == ('#eb7800') or ('#c13614'):
					print('Bad number skipping - call')
					nextTask = driver.find_element(By.XPATH, "//button[@class='caret-dropdown-button _1ylTesnUFCUoPnsDHUtF0P _22hSpbFmuiQ8R9QbO4ZqTX _1Ay9MEQX3iXqrw2cxxIbzo _1gXXlmROaFHLoEi6CKsXd6 _6HZaoxWJnRcfE95dytvs_ dropdown-button _10WN_uTvYhxSNagSvGB4n8']//i[@class='_3ExX8qM26_trEsvweUZWmM _3XP4tseTH1-F62Cg-zWwDx _1-DCZzScVz9s0VMOIYyDg2 _13bB5RjyTUrFyaxtvHghsD']")
					nextTask.click()
					try:
						skipStep = driver.find_element(By.XPATH, "//span[normalize-space()='Skip Step']")
						skipStep.click()
						continue
					except:
						rightarrow = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div/div/div/div[2]/div/div[1]/div[1]/div[1]/div[1]/button[2]/span/i')
						rightarrow.click()
						continue
				else:
					pass
			except NoSuchElementException:
				pass

			time.sleep(1)
			driver.implicitly_wait(10)
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


			time.sleep(15) #HK increased from 2-> 10 because calls were being cancelled
			driver.implicitly_wait(20) # HK added implicit wait

			print('Switching to iFrame')
			#iframe switch for modal popup:
			dialerFrame = driver.find_element(By.XPATH, "//iframe[contains(@title,'Outreach dialer')]")
			driver.switch_to.frame(dialerFrame)

			try:
				print('Checking for bad number')
				callAnyway = driver.find_element(By.XPATH, "//button[@aria-label='Call anyway']")
				callAnyway.click()
				badNum = True

				time.sleep(6) #HK increased from 2-> 6 because calls were being cancelled
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

		# double call good titles
			elif ('manager' in titlelist) or ('cto' in titlelist) or ('architect' in titlelist) or ('data' in titlelist) or\
			 ('senior' in titlelist) or ('ml' in titlelist) or ('ds' in titlelist) or ('de' in titlelist) or ('lead' in titlelist) or\
			  ('sr' in titlelist) or ('principal' in titlelist) or ('engineer' in titlelist) or ('vp' in titlelist) or\
			   ('director' in titlelist) or ('director' in titlelist) or ('analytics' in titlelist):
				
				# double call will not select disposition, so only one call will actually be logged, working on a fix 
				print('Calling Again')
				secondtry = driver.find_element(By.XPATH, "//*[@id='app']/div/div[1]/div/div/div/div[1]/div/div/div[1]/div/div[2]/div/div[2]/div/ul/li[2]/div[2]/a")
				secondtry.click()
				driver.implicitly_wait(20)

				print('switching to iframe')
				dialerFrame2 = driver.find_element(By.XPATH, "//iframe[contains(@title,'Outreach dialer')]")
				driver.switch_to.frame(dialerFrame2)
				time.sleep(15)

				try:
					print("Trying to hang up")
					endcall = driver.find_element(By.XPATH, "//*[@id='dialerBody']/div[2]/div[2]/div/div/div[2]/div/button/span[1]")
					endcall.click()
				except (NoSuchElementException, StaleElementReferenceException) as error: 
					print("Debug: no hang up button, passing")
			
				
				
				driver.switch_to.default_content()

				print('Logging 2nd Call - No Answer')
				dropdown = driver.find_element(By.XPATH, "//div[@data-test-id='autocomplete-component_callDisposition_value']//input[@id='model-autocomplete-input-element']")
				dropdown.click()
				time.sleep(0.75)
				dropdown.send_keys('Call No Answer')
				time.sleep(0.75)
				dropdown.send_keys(Keys.RETURN) 

				time.sleep(0.5)			
		# one call for non-good titles
			else: 
				print('Logging Call - No Answer')
				dropdown = driver.find_element(By.XPATH, "//div[@data-test-id='autocomplete-component_callDisposition_value']//input[@id='model-autocomplete-input-element']")
				dropdown.click()
				time.sleep(0.75)
				dropdown.send_keys('Call No Answer')
				time.sleep(0.75)
				dropdown.send_keys(Keys.RETURN) 

			i += 1
			print(f'Logged Call | Total Calls: {i}')

			logCall = driver.find_element(By.XPATH, "//span[contains(text(),'Log Call & Complete')]")
			logCall.click()
			time.sleep(0.75)
	print('---- Max hourly call limit reached ----')	


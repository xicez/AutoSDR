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
import pandas as pd


def autoSequencer(email, password, prospectEmail, prospectCampaign, chromedriver_path):

	# INITIALIZE VARS
	delay = 0
	time_left = 60
	x = 0 # X MUST BE 0 OR SEQUENCES WILL BE WRONG
	actionLog = []
	totalTime = []


	# INITIALIZE BROWSER DRIVER

	def launchBrowser():
		chrome_options = Options()
		chrome_options.binary_location="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
		chrome_options.add_argument("start-maximized");
		chrome_options.add_argument("--use-fake-device-for-media-stream");
		chrome_options.add_argument("--use-fake-ui-for-media-stream")
		driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chromedriver_path)

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

	try:

		for lead in prospectEmail:
			
			print(x)
			print(lead)
			campaign = prospectCampaign[x]
			print(campaign)

			start_time = perf_counter()

			driver.switch_to.default_content()

			#Search for the prospects email address in Outreach 
			
			search_button = driver.find_element(By.XPATH, "//i[@class='_3XP4tseTH1-F62Cg-zWwDx _2fZKQSDZC30Tb9NpVwNcBc _13bB5RjyTUrFyaxtvHghsD']")
			search_button.click()

			search_input = driver.find_element(By.XPATH, "//input[@placeholder='Search']")
			search_input.send_keys(lead)
			ActionChains(driver).move_to_element(search_input).key_down(Keys.RETURN).key_up(Keys.RETURN).perform()

			try:
				prospect_name = driver.find_element(By.XPATH, "//div[@class='_3H5qkVK0pC9Dnnch1YhgKI']")
				ActionChains(driver).move_to_element(prospect_name).click().perform()
				sequence_button = driver.find_element(By.XPATH, "//button[@class='sequence icon-button _1ylTesnUFCUoPnsDHUtF0P _2bFSp1_3O05dzYHWllrXO0 IEU0ZeP2iAN3PQHapRWyS _1R80yfDPFuM38JpsKWXGAb _2cnlnJABAd45c0XvaZNlQY']")
				sequence_button.click()

				time.sleep(3)
			except NoSuchElementException as e:
				print('Unable to locate prospect, continuing')
				continue

			

			try:	
				#iframe switch for modal popup:
				iframe_modal = driver.find_element(By.XPATH, "//iframe[contains(@title,'Outreach modal')]")
				driver.switch_to.frame(iframe_modal)

				time.sleep(3)
			except Exception as e:
				print(e)
				continue

			try:	
				sequenceFilter = driver.find_element(By.XPATH, "//input[@aria-label='Filter sequences']")
				sequenceFilter.click()

				time.sleep(2)
				ActionChains(driver).move_to_element(sequenceFilter).send_keys(campaign).perform()
				time.sleep(1)

			except NoSuchElementException as e:
				print('Skipping sequence filter')
				continue

			try:
				selectedSequence = driver.find_element(By.XPATH, "//span[@class='MuiTypography-root MuiTypography-displayBlock']")
				selectedSequenceTitle = selectedSequence.get_attribute('title')
				selectedSequenceClick = driver.find_element(By.XPATH, "//div[@class='MuiListItemText-root MuiListItemText-multiline']")
				print(f"Sequenced displayed: {selectedSequenceTitle}")
				print(campaign)

				corrSeq = False 
				while corrSeq == False:

					if campaign.lower() == selectedSequenceTitle.lower():
						print('Sequence is correct, continuing')
						selectedSequenceClick.click()
						corrSeq = True
					else:
						print('Sequence filter error, retrying')
						print('Closing sequence window')
						closeSequenceWindow = driver.find_element(By.XPATH, "//button[@aria-label='Close']")
						closeSequenceWindow.click()
						driver.switch_to.default_content()

						time.sleep(1.5)

						print('re-opening sequence window')
						sequence_button = driver.find_element(By.XPATH, "//button[@class='sequence icon-button _1ylTesnUFCUoPnsDHUtF0P _2bFSp1_3O05dzYHWllrXO0 IEU0ZeP2iAN3PQHapRWyS _1R80yfDPFuM38JpsKWXGAb _2cnlnJABAd45c0XvaZNlQY']")
						sequence_button.click()
						driver.switch_to.frame(iframe_modal)
						
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


				time.sleep(3)
			except NoSuchElementException as e:
				continue 

			try:

				addToSequenceButton = driver.find_element(By.XPATH, "//p[text()='Add to sequence']")
				addToSequenceButton.click()

				time.sleep(3)

			except Exception as e:
				print(e)
				continue

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
	except Exception as e:
		print(e)
		print('Something major went wrong! At this point the API should trigger a job refresh and then re-pull the latest data in a few minutes.')
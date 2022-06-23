from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys
import pandas as pd
from docx import Document
from Logging_system import Logging


start = time.perf_counter()

''' for BY class '''
ID = "id"
XPATH = "xpath"
LINK_TEXT = "link text"
PARTIAL_LINK_TEXT = "partial link text"
NAME = "name"
TAG_NAME = "tag name"
CLASS_NAME = "class name"
CSS_SELECTOR = "css selector"



log = Logging()
log.activate_logging()
log.program_expired()
log.credentials_check()
###### Driver object initialization ######
def Driver():
    print('Driver object initialization\n')
    log.logger.info('Driver object initialization\n')

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_path = ChromeDriverManager().install()
    driver=webdriver.Chrome(chrome_path,options=chrome_options)
    driver.maximize_window()
    driver.delete_all_cookies()
    time.sleep(3)
    return driver

'''Reads content in docx files'''
def read_docx(filename):

    document = Document(filename)
    text = []
    for paragraph in document.paragraphs:
        text.append(paragraph.text)
    return text

''' Switches to the new tab '''
def switch_tab(driver):


        driver.execute_script("window.open('');")
        chwd = driver.window_handles
 
        driver.switch_to.window(chwd[-1])
        time.sleep(5)


'''Removes earlier login and helps in switching account'''
def remove_login(driver):
    driver.find_element(By.XPATH,"//div[@class='tBJ dyH iFc sAJ xnr tg7 mWe']").click()
    time.sleep(2)
    btn = driver.find_element(By.XPATH,"//a[normalize-space()='Not you? Log in with a different account']")
    btn.click()

    return driver

''' Function handles the entire pinterest workflow '''
def pinterest_workflow(output_df=None):
    driver=Driver()
    driver.get('https://in.pinterest.com/login/')
      # Driver object initialization
    for itr in range(output_df.shape[0]):
        
        if itr !=0 : 
            driver=remove_login(driver)
            time.sleep(4)
            
        
        
        ############## Login ##############

        # driver.get(output_df.iloc[itr]['Portal Name'])   ## Gets the portal name
        
        print(f'\nAdding pin for username- {output_df.iloc[itr]["User Id"]}\n')
        log.logger.info(f'Adding pin for username- {output_df.iloc[itr]["User Id"]}\n')

        driver.find_element(By.XPATH,'//*[@id="email"]').send_keys(output_df.iloc[itr]['User Id'])  ## Sends user id
      
        driver.find_element(By.XPATH,'//*[@id="password"]').send_keys(output_df.iloc[itr]['Password'])  ## Sends password

        driver.find_element(By.CSS_SELECTOR,"button[type='submit'] div[class='zI7 iyn Hsu']").click()  ## Clicks login button
        time.sleep(5)

        driver.get('https://in.pinterest.com/pin-builder/')
        
       

        ## Uploading image
        img_path = os.getcwd()+'\\'+output_df.iloc[itr]['Image']
        drag_drop =  driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div[1]/div/div/div/input')
        drag_drop.send_keys(img_path)

        # title 
        driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div [2]/div/div[1]/div[1]/div/div/div[1]/textarea' ).send_keys(output_df.iloc[itr]['Title'])  

        #description 
        text = read_docx(output_df.iloc[itr]['Word document'] )  # Reads text from docx file 
            
        for t in text:
            driver.find_element(By.CSS_SELECTOR,'.public-DraftStyleDefault-block.public-DraftStyleDefault-ltr').send_keys(t)
        ## Save button
        save_btn = driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div/div/button[2]/div')
        save_btn.click()

        time.sleep(25)   
        drp_dwn_brn = driver.find_element(By.CSS_SELECTOR,"button[aria-label='Accounts and more options']")
        drp_dwn_brn.click()

        time.sleep(2)
        log_out_btn = driver.find_element(By.CSS_SELECTOR,"span[title='Log out']")
        log_out_btn.click()


        time.sleep(5)
        # switch_tab(driver)

try:       
    df=pd.read_excel('input.xlsx')      
    pinterest_workflow(df)
except Exception as e:
    exception_type, exception_object, exception_traceback = sys.exc_info()
    line_number = exception_traceback.tb_lineno

    print(f' {exception_type} error occurred at {line_number} while executing')
    log.logger.error(f' {exception_type} error occurred at {line_number} while executing')

finally:
    diff=round(time.perf_counter()-start,2)
    print('Time taken to complete the task is {} seconds'.format(diff))
    log.logger.info('Time taken to complete the task is {} seconds'.format(diff))
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

# Setting driver...
service = Service()
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Creating ActionChain object
act = ActionChains(driver)

# Creating list variables to hold results...
NAME = []
PHONE_NUMBER = []
EMAIL_ADDRESS = []
PHYSICAL_ADDRESS = []

# Loading site URL
driver.get('#################')
driver.maximize_window()

# Automating to click "Person"
driver.find_element(By.ID, "mega-menu-item-37").click()
time.sleep(5)

x = 4
while x < 36:

    # Automating "speciality" to "Industrial"
    speciality = driver.find_element(By.TAG_NAME, "select")
    select = Select(speciality)
    select.select_by_visible_text('Industrial')
        
    # Automating "Offices" to dynamic content
    office = driver.find_element(By.NAME, "office")
    select = Select(office)
    select.select_by_index(x)

    # Automating the "SUBMIT" button
    driver.find_element(By.XPATH, "/html/body/div[8]/main/div/div/div/div[1]/div/div[2]/div[1]/div/form/div/div[4]/input").click()

    time.sleep(10) # To allow the site load relevant element for program to use.

    # Narrowing down web elements to retrieve list of brokers displayed on webpage
    brokers = driver.find_element(By.ID, "brokers-list")

    # Retrieving id attribute of list of web element present in 'brokers' variable
    broker_ID = brokers.find_elements(By.CLASS_NAME, "broker")
    ATTRS = []
    for ids in broker_ID:
        ATTRS.append(ids.get_attribute('id'))

    # Iteration for the items on web page
    i = 0
    while i < len(ATTRS):

        # Action to open lightbox
        act.move_to_element(driver.find_element(By.ID, ATTRS[i])).click().perform()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'broker-detail-sidebar')))

        time.sleep(3)
            # Sending web elements to variable
        broker = driver.find_element(By.CLASS_NAME, 'broker-detail-sidebar')
        name = driver.find_element(By.CLASS_NAME, 'broker-right-content')

            # Getting the name of broker
        name = name.find_element(By.TAG_NAME, 'h2').text

            # Getting the phone number of broker
        number = broker.find_element(By.XPATH, f"//*[@id='{ATTRS[i]}']/div/div[1]/div[1]/div[5]/a").text.strip()

            # Getting the email of broker
        email = broker.find_element(By.CSS_SELECTOR, f'#{ATTRS[i]} > div > div.sidebar > div.broker-detail-sidebar > div.info.email > a').text.strip()

            # Getting the physical address of broker
        address = broker.find_element(By.CSS_SELECTOR, f'#{ATTRS[i]} > div > div.sidebar > div.broker-detail-sidebar > div.info.address').text.strip()

            # Closing lightbox
        driver.find_element(By.CLASS_NAME, "close").click()

            # Creating list to contain name, phone number, email and address
        NAME.append(name)
        PHONE_NUMBER.append(number)
        EMAIL_ADDRESS.append(email)
        PHYSICAL_ADDRESS.append(address)

        # Increment to monitor while loop
        i+=1
        
        if i >= len(ATTRS):
            pass
        else:
            if i == 4:
                driver.execute_script('arguments[0].scrollIntoView(true);',driver.find_element(By.ID, ATTRS[i]))
            if i == 8:
                driver.execute_script('arguments[0].scrollIntoView(true);',driver.find_element(By.ID, ATTRS[i]))
            if i == 12:
                driver.execute_script('arguments[0].scrollIntoView(true);',driver.find_element(By.ID, ATTRS[i]))
            if i == 16:
                driver.execute_script('arguments[0].scrollIntoView(true);',driver.find_element(By.ID, ATTRS[i]))
            if i == 20:
                driver.execute_script('arguments[0].scrollIntoView(true);',driver.find_element(By.ID, ATTRS[i]))
            if i == 24:
                driver.execute_script('arguments[0].scrollIntoView(true);',driver.find_element(By.ID, ATTRS[i]))
            if i == 28:
                driver.execute_script('arguments[0].scrollIntoView(true);',driver.find_element(By.ID, ATTRS[i]))
            if i == 30:
                driver.execute_script('arguments[0].scrollIntoView(true);',driver.find_element(By.ID, ATTRS[i]))
            if i == 34:
                driver.execute_script('arguments[0].scrollIntoView(true);',driver.find_element(By.ID, ATTRS[i]))
            if i == 38:
                driver.execute_script('arguments[0].scrollIntoView(true);',driver.find_element(By.ID, ATTRS[i]))
            if i == 42:
                driver.execute_script('arguments[0].scrollIntoView(true);',driver.find_element(By.ID, ATTRS[i]))
            if i == 46:
                driver.execute_script('arguments[0].scrollIntoView(true);',driver.find_element(By.ID, ATTRS[i]))
            if i == 50:
                driver.execute_script('arguments[0].scrollIntoView(true);',driver.find_element(By.ID, ATTRS[i]))
        
        time.sleep(2)


    driver.execute_script("window.scrollTo(0, 0);")
    
    # Increment to change office.
    x+=1
    time.sleep(2)

# Creating dataframe
data = {"Name": NAME,
        "Phone_Number": PHONE_NUMBER,
        "Email": EMAIL_ADDRESS,
        "Physical_Address": PHYSICAL_ADDRESS}


time.sleep(4)
driver.minimize_window()
driver.quit()

# Saving collected data in csv format
df = pd.DataFrame(data)
df.to_csv("df.csv")

# Cleaning csv file
clean_data = pd.read_csv('df.csv')
df['Physical_Address'] = df['Physical_Address'].str.replace("\n",", ")
df.to_csv('brokers_details.csv')

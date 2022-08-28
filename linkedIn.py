from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import parameters, csv, os.path, time, random




# Functions 
def search_and_send_request(location, keywords, writer):
        page = 0
        while True:
            page += 1
            LOCATION_NO = '?geoUrn=["' + location + '"]'
            KEYWORD = '&keywords=' + keywords
            ORIGINE = '&origin=GLOBAL_SEARCH_HEADER'
            PAGE = '&page=' + str(page)
            print('\nINFO: Checking on page ' + str(page))
            page_sleep()
            query_url = 'https://www.linkedin.com/search/results/people/' + LOCATION_NO + KEYWORD + ORIGINE + PAGE
            driver.get(query_url)
            time.sleep(random.uniform(3.0, 5.0))
            html = driver.find_element(By.TAG_NAME, 'html')
            html.send_keys(Keys.END)
            time.sleep(random.uniform(3.0, 5.0))
            linkedin_urls = driver.find_elements(By.CLASS_NAME, 'reusable-search__result-container')
            print('INFO: %s connections found on page %s' % (len(linkedin_urls), page))
            for index, result in enumerate(linkedin_urls, start=1):
                text = result.text.split('\n')[0]
                connection_action = result.find_elements(By.CLASS_NAME, 'artdeco-button__text')
                if connection_action:
                    connection = connection_action[0]
                else: 
                    print("%s ) CANT: %s" % (index, text))
                    continue
                if connection.text == 'Connect':
                    try:
                        coordinates = connection.location_once_scrolled_into_view # returns dict of X, Y coordinates
                        driver.execute_script("window.scrollTo(%s, %s);" % (coordinates['x'], coordinates['y']))
                        time.sleep(random.uniform(2.0, 6.0))
                        connection.click()
                        time.sleep(random.uniform(3.0, 5.0))
                        if driver.find_elements(By.CLASS_NAME, 'artdeco-button--primary')[0].is_enabled():
                            driver.find_elements(By.CLASS_NAME, 'artdeco-button--primary')[0].click()
                            writer.writerow([text])
                            print("%s ) SENT: %s" % (index, text))
                        else:
                            driver.find_elements(By.CLASS_NAME, 'artdeco-modal__dismiss')[0].click()
                            print("%s ) CANT: %s" % (index, text))
                    except Exception as e:
                        print('%s ) ERROR: %s' % (index, text))
                    time.sleep(random.uniform(4.0, 7.0))
                elif connection.text == 'Pending':
                        print("%s ) PENDING: %s" % (index, text))
                else:
                        if text : print("%s ) CANT: %s" % (index, text))
                        else: print("%s ) ERROR: You might have reached limit" % (index))



# Login
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.linkedin.com/login')
time.sleep(random.uniform(5, 10))
driver.find_element(By.ID, 'username').send_keys(parameters.linkedin_username)
driver.find_element(By.ID, 'password').send_keys(parameters.linkedin_password)
time.sleep(random.uniform(4, 7))
driver.find_element(By.XPATH, '//*[@type="submit"]').click()
# maximize window
#driver.maximize_window()
time.sleep(random.uniform(5, 10))

#name = driver.find_elements(By.CLASS_NAME, 'profile-rail-card__actor-link')[0].text.replace(' ', '')


def scroll_now():
    print("Page scroll")
    last_height = driver.execute_script("return document.body.scrollHeight")
    count = 0
    while (count < 15):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(random.uniform(2.1, 3.9))
        count = count + 1

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def page_sleep():
    sleeptime = random.uniform(5.0, 10.0)
    print("Page will sleep for", sleeptime, "seconds")
    time.sleep(sleeptime)


# CSV file loging
#file_name = name + '_' + parameters.file_name.capitalize()
file_name = parameters.file_name
file_exists =  os.path.isfile(file_name)
writer = csv.writer(open(file_name, 'a'))
if not file_exists: writer.writerow(['Connection Summary'])

# Scroll the page to avoid bot detection
scroll_now()

# Search
search_and_send_request(location=parameters.location, keywords=parameters.keywords, writer=writer)

# Close browser
driver.quit()

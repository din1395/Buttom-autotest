import requests
from bs4 import BeautifulSoup, SoupStrainer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import contextlib
import time

url= "https://www.selenium.dev/selenium/docs/api/py/index.html"

#URL scraping <a href=***> and saving to file do work with it
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser", parse_only=SoupStrainer('a'))

with open('autoButtomTest/links', 'w') as file:
    for tag in soup.findAll('a', href=True):
        item="//*[@href='"+(str(tag['href']))+"']"
        #exceptions for links
        dontNeed= ".jpg" or ".png" or ".pdf"
        if dontNeed in item:
            print (item, "deleteted")
        else:
            file.write("%s\n" % item)

#exclude dublicates from file

file ='autoButtomTest/links'
uniqlines = set(open(file,'r', encoding='utf-8').readlines())
noDuplicate = open(file,'w', encoding='utf-8').writelines(set(uniqlines))


chrome_driver=webdriver.Chrome('/Users/pavelkozlovskij/python/chromedriver')

def openBrowser():
    chrome_driver.maximize_window()
    chrome_driver.get(url)

#checking site(tab) status
def checkStatus(website):
    with contextlib.nullcontext(chrome_driver) as driver:
        driver.get(website)
        for request in driver.requests:
            if request.response:
                print(request.response.status_code,website,request.path)
            else:
                print(website,"fail", request.path)


with open('autoButtomTest/tabsUrl','r') as tabsUrl:
    tab= tabsUrl.readlines
    for tab in tabsUrl:
        checkStatus(tab)
                
openBrowser()

with open('autoButtomTest/links', 'r') as links:
    for link in links:
        elements=chrome_driver.find_elements_by_xpath(link)
        for element in elements:
            with open ('autoButtomTest/visabilityOfLinks','a') as f:
                if element.is_displayed():
                    ActionChains(chrome_driver) \
                     .move_to_element(element)\
                     .key_down(Keys.COMMAND) \
                     .click(element) \
                     .key_up(Keys.COMMAND) \
                     .perform()
                
                    ti=('\n',link,"like an element on location",'\n',element.rect,'\n',"is visible and usable",'\n')
                    for item in ti:
                     s = str(item)
                     f.writelines(s)
                    
                    
        
                else:
                    ti= ('\n',link,"like an element on location",'\n',element.rect,'\n',"is not visible", '\n')
                    for item in ti:
                     s = str(item)
                     f.writelines(s)



def copyBarsUrl ():#counting number of tabs
    tabsUrl=[]
    tabsNumber= len(chrome_driver.window_handles)
    i=0
    while i < tabsNumber:
        #listOfURL.append(chrome_driver.current_url)
        chrome_driver.switch_to.window(chrome_driver.window_handles[-1])
        tabsUrl.append(chrome_driver.current_url)
        chrome_driver.close()
        i+=1
    else:
        chrome_driver.quit()
    with open ('/Users/pavelkozlovskij/python/autoButtomTest/tabsUrl','w') as tabs:
        for tab in tabsUrl:
            tabs.write("%s\n" % tab)

copyBarsUrl()
chrome_driver.quit()

file ='autoButtomTest/tabsUrl'
uniqlines = set(open(file,'r', encoding='utf-8').readlines())
noDuplicate = open(file,'w', encoding='utf-8').writelines(set(uniqlines))

def checkStatus(website):
    from seleniumwire import webdriver
    chrome_driver=webdriver.Chrome('/Users/pavelkozlovskij/python/chromedriver')
    with contextlib.nullcontext(chrome_driver) as driver:
        driver.get(website)
        with open ('autoButtomTest/logs','a') as logs:
            logs.writelines(website)
            logs.writelines('\n')
            for request in driver.requests:
                if request.response:
                    ti= (request.path,request.response.status_code) 
                    for item in ti:
                     s = str(item) + '\n'
                     logs.write(s)
                else:
                    pass
                #надо донастроить исключения и переработать цикл проверки


with open('autoButtomTest/tabsUrl','r') as tabsUrl:
    tab= tabsUrl.readlines
    for tab in tabsUrl:
        checkStatus(tab)
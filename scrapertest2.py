from requests_html import HTMLSession
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import numpy as np

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("/usr/bin/chromedriver", options=options)


session = HTMLSession()

URL = 'https://cooper.campuslabs.com/engage/organizations'
driver.get(URL)
# more_buttons = driver.find_element_by_xpath("//button[@class='outlinedButton']")

more_buttons = driver.find_element_by_xpath('//*[@id="react-app"]/div/div/div/div[2]/div/div[2]/div/div[2]/div[2]/button')
# print(more_buttons.get_attribute('innerHTML'))
while (driver.find_elements_by_xpath('//*[@id="react-app"]/div/div/div/div[2]/div/div[2]/div/div[2]/div[2]/button')):
	driver.execute_script("arguments[0].click();", more_buttons)
	time.sleep(1)
page_source = driver.page_source
clubs_source = driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div[2]/div/div[2]/div/div/div/div')
# print(clubs_source.get_attribute('innerHTML'))
soup = BeautifulSoup(clubs_source.get_attribute('innerHTML'), 'html.parser')
results = soup.find_all("a", href=True)
clubs_info = []




for result in results:
	divs = result.find_all("div")
	counter = 0
	club_info = []
	rawclubdesc = divs[1].text.strip()
	clubdesc = rawclubdesc.replace('"', "")
	namedivs = divs[4].find_all("div")
	clubname = namedivs[-1].text.strip()
	club_info.append(clubname)
	club_info.append(clubdesc)
	image = divs[4].find("img")
	if(image is not None):
		imageSrc = image['src'].strip()
		club_info.append(imageSrc)
	clubs_info.append(club_info)


# for club in clubs_info:
# 	print()
# 	print(club)
# 	print()

np.savetxt("clubInfo.csv", clubs_info, delimiter =", ", fmt = "% s")



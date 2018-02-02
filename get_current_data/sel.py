from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from run_filters import *

driver = webdriver.Chrome()

config = read_config("packet_config.ini")
username = config.get('credentials','username')
password = config.get('credentials','password')
# Sign In credentials along with nacc url
str = "http://"+username+":"+password+"@www.alz.washington.edu/MEMBER/sitesub.htm"
driver.get(str)
# Get the uds project url
nacc_project_elem = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[1]/td[2]/font/ul[1]/li[5]/a")
nacc_link = nacc_project_elem.get_attribute('href')
# Navigate to uds link
driver.get(nacc_link)
# Get the Url of 1Florida ADRC
uds_project = driver.find_element_by_xpath("//*[@id='m_3subsystem_graphicC']/area[1]")
uds_link = uds_project.get_attribute('href')
# Navigate to 1Florida ADRC project Link
driver.get(uds_link)
uds_nacc_results = driver.find_element_by_xpath("//*[@id='bodytable']/form/font/b/button").click()
elem = driver.find_element_by_name("FINCHK_X")
# Above element is Hidden. To click the hidden element we are making use of Js
driver.execute_script("(arguments[0]).click();", elem)
driver.execute_script(open("./getpacket.js").read())
assert "No results found." not in driver.page_source
driver.close()

import ConfigParser
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def read_config(config_path):
    config = ConfigParser.ConfigParser()
    config.read(config_path)
    return config

def upload_file(driver,filepath):
    elem1 = driver.find_element_by_name("UPLOADR_X")
    driver.execute_script("(arguments[0]).click();", elem1)
    driver.find_element_by_name("FILEUP").send_keys(filepath)
    driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[2]/td[2]/font/center/button").click()
    if "There are errors click the button below" in driver.page_source:
        print "errors upload new file"
    else:
        print "file uploaded Succesfully"
    return

def get_nacc_data(driver):
    elem = driver.find_element_by_name("FINCHK_X")
    # Above element is Hidden. To click the hidden element we are making use of Js
    driver.execute_script("(arguments[0]).click();", elem)
    # The getPacket.js fetches data from Nacc
    driver.execute_script(open("./getpacket.js").read())
    return

def main(argv):
    config = read_config("packet_config.ini")
    driver = webdriver.Chrome()

    options = argv
    username = config.get('credentials','username')
    password = config.get('credentials','password')
    filepath = config.get('uploadpath','path')
    # Sign In credentials along with nacc url
    str = "http://"+username+":"+password+"@www.alz.washington.edu/MEMBER/sitesub.htm"
    driver.get(str)
    # Get the 1Florida ADRC project url
    nacc_project_elem = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[1]/td[2]/font/ul[1]/li[5]/a")
    florida_adrc_link = nacc_project_elem.get_attribute('href')
    driver.get(florida_adrc_link)
    # get the uds link
    uds_project = driver.find_element_by_xpath("//*[@id='m_3subsystem_graphicC']/area[1]")
    uds_link = uds_project.get_attribute('href')
    # Navigate to uds link
    driver.get(uds_link)

    uds_nacc_results = driver.find_element_by_xpath("//*[@id='bodytable']/form/font/b/button").click()
    if options == "upload":
        upload_file(driver,filepath)
    if options == "getdata":
        get_nacc_data(driver)

    assert "No results found." not in driver.page_source
    driver.close()

if __name__ == '__main__':
    main(sys.argv[1])

import ConfigParser
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def read_config(config_path):
    config = ConfigParser.ConfigParser()
    config.read(config_path)
    return config

def upload_file(driver,filepath,email):
    elem1 = driver.find_element_by_name("UPLOADR_X")
    driver.execute_script("(arguments[0]).click();", elem1)
    driver.find_element_by_name("FILEUP").send_keys(filepath)
    driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[2]/td[2]/font/center/button").click()
    if "There are errors click the button below" in driver.page_source:
        print "errors upload new file"
    else:
        print "file uploaded Succesfully"
        driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[2]/td[2]/input").click()
        driver.find_element_by_name("EMAIL").send_keys(email)
    return

def get_nacc_data(driver):
    elem = driver.find_element_by_name("FINCHK_X")
    # Above element is Hidden. To click the hidden element we are making use of Js
    driver.execute_script("(arguments[0]).click();", elem)
    # The getPacket.js fetches data from Nacc
    driver.execute_script(open("./getpacket.js").read())
    return

def replace_link(element, username, password):
    link = element.get_attribute('href')
    link = link.replace("https://","")
    link  = "http://"+username+":"+password+"@"+link
    return link

def main(argv):
    config = read_config("packet_config.ini")
    try:
        
        driver = webdriver.Chrome()
        options = argv
        username = config.get('credentials','username')
        password = config.get('credentials','password')
        email = config.get('credentials', 'email')
        filepath = config.get('uploadpath','path')

        # Sign In credentials along with nacc url
        str = "http://"+username+":"+password+"@www.alz.washington.edu/MEMBER/sitesub.htm"
        driver.get(str)
        # Get the 1Florida ADRC project url
        nacc_project_elem = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[1]/td[2]/font/ul[1]/li[5]/a")
        florida_adrc_link = replace_link(nacc_project_elem, username, password)
        driver.get(florida_adrc_link)
        # get the uds link
        uds_project = driver.find_element_by_xpath("//*[@id='m_3subsystem_graphicC']/area[1]")
        uds_link = replace_link(uds_project, username, password)
        # Navigate to uds link
        driver.get(uds_link)

        uds_nacc_results = driver.find_element_by_xpath("//*[@id='bodytable']/form/font/b/button").click()
        if options == "upload":
            upload_file(driver,filepath,email)
        if options == "getdata":
            get_nacc_data(driver)

        driver.close()

    except Exception as e:
        driver.close()

if __name__ == '__main__':
    main(sys.argv[1])

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
from pandas import read_json
import json

from mp3downloader import Mp3Downloader


class PatoisBot():


    def exportCsv(self):
        df=read_json("result.json",orient="index")
        df.to_csv(r'result.csv',index=False)

    def extractWords(self, dictionary):
        word_list={}
        range_pages=3 #numer of pages for single letter
        driver=webdriver.Firefox()
        driver.implicitly_wait(1)  # seconds
        url = "https://www.patoisvda.org/it/glossari-per-comune/" + dictionary
        list_letter=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        incr=0
        for x in list_letter:

            tmp=url+"_"+x
            for x in range(range_pages):
                i=tmp+"_"+x.__str__()
                driver.get(i)
                time.sleep(0.5)
                for y in range(50):
                    try:
                        #patois_name=driver.find_element_by_xpath("/html/body/main/div/section[2]/div/div[1]/div[3]/div["+ (y+1).__str__() +"]"+"/div/div/h4/a")
                        #print(patois_name.text)
                        patois_name=driver.find_element_by_xpath("/html/body/main/div/section[2]/div/div[1]/div[3]/div["+ (y+1).__str__() +"]"+"/div/div/h4/a")
                        tmp_patois=patois_name.text
                    except:
                        print("error_retreeving patois name")

                    try:
                        url_audio=driver.find_element_by_xpath("/html/body/main/div/section[2]/div/div[1]/div[3]/div["+ (y+1).__str__() +"]"+"/div/div/h4/button")
                        tmp_url_audio=url_audio.get_attribute("data-ap")
                    except:
                        tmp_url_audio=""
                    try:
                        francese=driver.find_element_by_xpath("/html/body/main/div/section[2]/div/div[1]/div[3]/div[" + (y + 1).__str__() + "]" + "/div/div/div/div[1]")
                        tmp_francese=str(francese.text)
                    except:
                        tmp_francese=""
                    try:
                        italiano=driver.find_element_by_xpath("/html/body/main/div/section[2]/div/div[1]/div[3]/div[" + (y + 1).__str__() + "]" + "/div/div/div/div[2]")
                        tmp_italiano=str(italiano.text)
                    except:
                        tmp_italiano=""
                    word_list[incr]={"patois":tmp_patois,"francese":tmp_francese.replace("Francese: ",""),"italiano":tmp_italiano.replace("Italiano: ",""),"audio":tmp_url_audio}
                    incr=incr+1
                    Mp3Downloader().getMp3(tmp_url_audio)
            with open('result.json', 'w') as fp:
                json.dump(word_list, fp)
            fp.close()


        self.exportCsv()
        driver.close()



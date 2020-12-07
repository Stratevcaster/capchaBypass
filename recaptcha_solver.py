# -*- coding: utf-8 -*-
"""

@author: Yani
"""


import os
import random
import time
#selenium libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException   
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.chrome.options import Options

#librerias recapcha 
import speech_recognition as sr
import ffmpy
import requests
import urllib
import pydub
from pydub import AudioSegment

def delay ():
    time.sleep(random.randint(2,3))

try:
    #crea driver para el navegador Chrome
    driver = webdriver.Chrome(os.getcwd()+"\\webdriver\\chromedriver.exe") 
    delay()
    #pagina web
    driver.get("https://www.google.com/recaptcha/api2/demo")
    
except:
    print("[-]Actualiza tu driver Chrome https://chromedriver.chromium.org/downloads")

frames=driver.find_elements_by_tag_name("iframe")
driver.switch_to.frame(frames[0]);
delay()

#Hacer click en el reapcha 
driver.find_element_by_class_name("recaptcha-checkbox-border").click()

#cambia a  recaptcha audio control frame
driver.switch_to.default_content()
frames=driver.find_element_by_xpath("/html/body/div[2]/div[4]").find_elements_by_tag_name("iframe")
driver.switch_to.frame(frames[0])
delay()

#click en audio
driver.find_element_by_id("recaptcha-audio-button").click()

driver.switch_to.default_content()
frames= driver.find_elements_by_tag_name("iframe")
driver.switch_to.frame(frames[-1])
delay()

#click boton play
driver.find_element_by_xpath("/html/body/div/div/div[3]/div/button").click()
#get the mp3 audio file
src = driver.find_element_by_id("audio-source").get_attribute("src")
print("[INFO] Audio src: %s"%src)
#descarga MP3 
urllib.request.urlretrieve(src, os.getcwd()+"\\sample.mp3")
sound = pydub.AudioSegment.from_mp3(os.getcwd()+"\\sample.mp3")
sound.export(os.getcwd()+"\\sample.wav", format="wav")
sample_audio = sr.AudioFile(os.getcwd()+"\\sample.wav")
r= sr.Recognizer()

with sample_audio as source:
    audio = r.record(source)

# language = 'es', show_all=True Importante si la pagina devuelve resultados en español
key=r.recognize_google(audio, language = 'es', show_all=True)
print("[INFO] Recaptcha Passcode: %s"%key)

#key in results and submit
wordDict=key["alternative"]
phraseList=wordDict.values()

dict=wordDict[0]
frase = dict['transcript']




try:
    for phrase in phraseList:
        
        driver.find_element_by_id("audio-response").send_keys(phrase.lower())
        driver.find_element_by_id("audio-response").send_keys(Keys.ENTER)
        driver.switch_to.default_content()
        delay()
        driver.find_element_by_id("recaptcha-demo-submit").click()
except:
    print("La palabra no es adecuada,se deberia de probar con otra combinación")

delay()
delay()
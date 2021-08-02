import pyrebase
from selenium import webdriver
import time
import sys
import random
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

url = sys.argv[1]
name=sys.argv[2]
sender=sys.argv[3]
postedto=sys.argv[4]
password=sys.argv[5]

def send_mail(mail,text,subject):
    message = MIMEMultipart()
    message["From"] = ""
    message["To"] = mail
    message["Subject"] = subject
    message_text = text

    message_content = MIMEText(message_text, "html")
    message.attach(message_content)
    mail = smtplib.SMTP("smtp.gmail.com", 587)
    mail.ehlo()
    mail.starttls()
    mail.login(sender, password)
    mail.sendmail(message["From"], message["To"], message.as_string())
    mail.close()


print ("\nBY ERSEL AKBAY\n")
print ("\nSahibinden Link: %s" % (url))

config={                                                                  #database app settings must be written.
    "apiKey": "***************************************",
    "authDomain": "*******-*****.firebaseapp.com",
    "databaseURL": "*********************.firebaseio.com",
    "projectId": "*********-*****",
    "databaseurl": "-*********************.firebaseio.com/",
    "storageBucket": "*******-*****.appspot.com",
    "messagingSenderId": "********",
    "appId": "********************"
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()

browser = webdriver.Chrome()
browser.get(url)

time.sleep(0.2)

enter = browser.find_element_by_xpath("//*[@id='searchResultsTable']/tbody/tr[1]/td[3]")
enter.click()

time.sleep(1.5)

lasturl=browser.current_url

database.child("Houses").child("Last Url").set(lasturl)

time.sleep(0.5)

while True:

    browser.get(url)
    
    time.sleep(1.5)

    enter = browser.find_element_by_xpath("//*[@id='searchResultsTable']/tbody/tr[1]/td[3]")
    enter.click()

    time.sleep(1.5)

    lasturl=browser.current_url

    dburl= database.child("Houses").child("Last Url").get()
    dburl=dburl.val()

    if dburl != lasturl:
        print("Yeni Link Bulundu! Mail gonderılıyor..")
        now = datetime.datetime.now()
        now=str(now)
        now=now[ 0 : 19 ]
        text="Selam, " + name + " " + now + " tarihinde senin kriterlerine uygun yeni bir ev buldum! İlan Linki: "+ lasturl
        send_mail(postedto,text,"Yeni Ev İlanı!")
        print("Mail gonderimi basarili")

        database.child("Houses").child("Last Url").set(lasturl)

        time.sleep(1.5)

    if dburl == lasturl:
        print("yeni link bulunamadı tekrar aranıyor.")
#from PyQt5.QtCore import *
#from PyQt5.QtWebEngineWidgets import *
#from PyQt5.QtWidgets import QApplication
from threading import Timer
import sys
import time
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import (QHBoxLayout, QPushButton, QWidget, QApplication, QVBoxLayout, QMessageBox)
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import re

# Start using all the regular flask logic

# Write to main page


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        xpos = 300
        ypos= 300
        width = 350
        height =  350
        vbox = QVBoxLayout(self)
        hbox = QHBoxLayout()
        url = "http://192.168.0.161/"
        self.webEngineView = QWebEngineView()
        #self.webEngineView.load(QUrl("http://192.168.0.161/"))
        #self.webEngineView.load(QUrl("https://www.geeksforgeeks.org/selenium-python-tutorial/"))
        self.webEngineView.load(QUrl(url))
        print(self.webEngineView.url().toString())
        #self.showFullScreen()
        self.expBtn = QPushButton('Download PDF', self)
       
        self.expBtn.clicked.connect(self.onClickedPDF)
        
        #expBtn1 = QPushButton('Email PDF', self)
        #expBtn1.clicked.connect(self.onClickedEmail)
        
        hbox.addWidget(self.expBtn)
        #hbox.addWidget(expBtn1)
        vbox.addWidget(self.webEngineView)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        #self.setGeometry(xpos, ypos,width ,height)
        self.setWindowTitle('OHM3000Lite')
        self.showMaximized()
        self.expBtn.hide()
        #expBtn1.hide()
        self.webEngineView.urlChanged.connect(self.checkUrl)
    
    def checkUrl(self):
        currentUrl = self.webEngineView.url().toString()
        print(currentUrl)
        if re.search('^http://192.168.0.161/reports/*',currentUrl):
            print("Button Visible")
            self.expBtn.show()
        else:
            print("Button Disabled")
            self.expBtn.hide()
    
    def onClickedPDF(self):
        print(self.webEngineView.url().toString())
        self.webEngineView.page().printToPdf('myfile.pdf')
        time.sleep(10)
        QMessageBox.information(self, 'info', 'page exported')

    def onClickedEmail(self):
        self.webEngineView.page().printToPdf('selenium.pdf')
        time.sleep(10)
        QMessageBox.information(self, 'info', 'page exported')
        body = '''Hello,
        This is the body of the email
        sicerely yours
        G.G.
        '''
        # put your email here
        sender = r'nirajfakepython@gmail.com'
        # get the password in the gmail (manage your google account, click on the avatar on the right)
        # then go to security (right) and app password (center)
        # insert the password and then choose mail and this computer and then generate
        # copy the password generated here
        password = r'qwerty1234!@#$'
        # put the email of the receiver here
        receiver = r'nirajparte89@gmail.com'
        
        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = receiver
        message['Subject'] = 'This email has an attacment, a pdf file'
        
        message.attach(MIMEText(body, 'plain'))
        
        pdfname = 'selenium.pdf'
        
        # open the file in bynary
        binary_pdf = open(pdfname, 'rb')
        print("open")
        payload = MIMEBase('application', 'octate-stream', Name=pdfname)
        # payload = MIMEBase('application', 'pdf', Name=pdfname)
        payload.set_payload((binary_pdf).read())
        print("set")
        # enconding the binary into base64
        encoders.encode_base64(payload)
        
        # add header with pdf name
        payload.add_header('Content-Decomposition', 'attachment', filename=pdfname)
        message.attach(payload)
        print("attached")
        #use gmail with port
        session = smtplib.SMTP('smtp.gmail.com', 587)
        
        #enable security
        session.starttls()
        
        #login with mail_id and password
        session.login(sender, password)
        print("logged in")
        text = message.as_string()
        session.sendmail(sender, receiver, text)
        session.quit()
        print('Mail Sent')


def main():

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
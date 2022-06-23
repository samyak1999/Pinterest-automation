import logging
import sys
from datetime import datetime
import os
import ntplib
import time
import getpass
import pathlib
import sys
# from mail import send_mail,malfunction_mail

# https://www.programcreek.com/python/example/192/logging.Formatter


class Logging:
    def __init__(self):
        
        ntpClient = ntplib.NTPClient()
        response = ntpClient.request('pool.ntp.org')
        
        try:
            self.curr_time = datetime.strptime(time.ctime(response.tx_time), "%a %b %d %H:%M:%S %Y")
        except:
            sys.exit("Unable to connect internet time")

        curr_dir= os.getcwd()

        log_folder= 'Log'
        output_folder='Output'
        log_dir = os.path.join(curr_dir,log_folder)
        output_dir = os.path.join(curr_dir,output_folder)

        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)
        if not os.path.isdir(log_dir):
            os.mkdir(log_dir)

        self.filename = self.curr_time.strftime("SKE-WP2005_V1 %d-%m-%Y %H.%M.%S logfile.log")
        logs_path = os.path.join(log_dir,self.filename)

        log_path= pathlib.PureWindowsPath(logs_path).as_posix()
        
        logging.basicConfig(filename= f'{log_path}'   ,format='%(asctime)s | %(levelname)s | %(message)s',datefmt='%d-%m-%Y %H:%M:%S', level =logging.INFO,filemode='w')
        #formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s','%d-%m-%Y %H:%M:%S')
        #file_handler = logging.FileHandler(log=,_path)
        #file_handler.setFormatter(formatter)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.logger.info("Program Started")    

    def activate_logging(self):
        print('Logging is now activated!!!!!')
        self.logger.info('Logging activated')

    def program_expired(self):
        
        expiry_date = datetime(2022,7,30,23,59,59)  
        #print(type(curr_time))
        diff = expiry_date - self.curr_time
        expiry_date_day = expiry_date.date()

        if expiry_date < self.curr_time:
            print("Your License has expired on {}.Renew it immediately.".format(expiry_date_day))
            self.logger.critical("Program expired!!") 
            # malfunction_mail(self.filename)
            # send_mail()   
            sys.exit('Renew then retry')
        if  self.curr_time < expiry_date:
            print("License valid.Renewal due in {} hours".format(diff))
            
            
    def credentials_check(self):
        cnt = 0
        while (cnt < 2):
            #user_id = input("Enter userid- ")
            password = getpass.getpass(prompt='Enter password- ')
            if  password == 'admin':
        
                self.logger.info("Correct Credentials!!!Access Granted")
                break
            else:
                cnt += 1
                if cnt == 2:
                    print("Access denied!! Terminating program")
                    self.logger.critical("Sign in Failed")
                    # malfunction_mail(self.filename )
                    # send_mail()   
                    sys.exit()
                else:
                    print("Last attempt left")
                    self.logger.error("Invalid attempts!!!")







#!/usr/bin/env python
# coding: utf-8
# Auteur    : Patrick Pinard
# Date      : 6.5.2021
# Objet     : Pilotage modules relais avec interface web basée sur API RESTful Flask et bootstrap sur PI zero 
# Version   :   1.0 


from gpiozero import Button 
import time 
import os 
import logging

logging.basicConfig(filename='/home/pi/python/relaybox/shutdownbutton.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

stopButton = Button(26) # defines the button as an object and chooses GPIO 26

while True:
    if stopButton.is_pressed: #Check to see if button is pressed
        logging.info("shutdown requested, waiting for confirmation")
        print("shutdown button pressed, waiting for confirmation (3 sec)")
        time.sleep(1) # wait for the hold time we want. 
        print("3... continue to press shutdown button to confirm !")
        if stopButton.is_pressed: 
            time.sleep(1) # wait for the hold time we want. 
            print(".2.. continue to press shutdown button to confirm !")
            if stopButton.is_pressed: 
                time.sleep(1) # wait for the hold time we want. 
                print("..1. continue to press shutdown button to confirm !")
                time.sleep(1) # wait for the hold time we want. 
                if stopButton.is_pressed: #check if the user let go of the button
                    print("...0 shutdown confirmed,  bye !")
                    print("shutdown now -h")
                    logging.info("shutdown now -h initialized")
                    os.system("sudo shutdown now -h") #shut down the Pi -h is or -r will reset
                else:
                    print("shutdown aborted !")
                    logging.info("shutdown aborted")
            else:
                print("shutdown aborted !")
                logging.info("shutdown aborted")
        else:
            print("shutdown aborted !")
            logging.info("shutdown aborted")
    time.sleep(1) # wait to loop again so we don’t use the processor too much.

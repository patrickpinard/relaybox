
#!/usr/bin/env python
# coding: utf-8
# Auteur    : Patrick Pinard
# Date      : 6.5.2021
# Objet     : Pilotage modules relais avec interface web basée sur API RESTful Flask et bootstrap sur PI zero 
# Version   :   1.0 


from gpiozero import Button 
import time 
import os 
#import logging

#logging.basicConfig(filename='shutdownbutton.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

stopButton = Button(26) # defines the button as an object and chooses GPIO 26

while True: 
    
    if stopButton.is_pressed: #Check to see if button is pressed
        #logging.info("shutdown requested, waiting for confirmation")        
        print("shutdown button pressed, waiting for confirmation (3 sec)")
        time.sleep(3) # wait for the hold time we want. 

        if stopButton.is_pressed: #check if the user let go of the button
            print("shutdown confirmed,  bye !")
            print("shutdown now -h")
            #logging.info("shutdown confirmed, sudo shutdown -h command started...") 
            os.system("sudo shutdown now -h") #shut down the Pi -h is or -r will reset
        else:
            print("shutdown NOT confirmed !")
            #logging.info("shutdown not confirmed ! ") 
           
    time.sleep(1) # wait to loop again so we don’t use the processor too much.
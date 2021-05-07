from gpiozero import Button 
import time 
import os 
import logging

stopButton = Button(26) # defines the button as an object and chooses GPIO 26
logging.basicConfig(filename='shutdownbutton.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

while True: 
    if stopButton.is_pressed: #Check to see if button is pressed
        logging.info("stop button pressed... waiting for confirmation to shutdown.")
        print("shutdown button pressed, waiting for confirmation (3 sec)")
        time.sleep(3) # wait for the hold time we want. 
        if stopButton.is_pressed: #check if the user let go of the button
            print("shutdown confirmed,  bye !")
            print("shutdown now -h")
            logging.info("shutdown confirmed,  bye !")
            os.system("shutdown now -h") #shut down the Pi -h is or -r will reset
        else:
            print("shutdown NOT confirmed !")
            logging.info("shutdown NOT confirmed !")
    time.sleep(1) # wait to loop again so we don’t use the processor too much.
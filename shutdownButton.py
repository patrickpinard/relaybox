from gpiozero import Button 
import time 
import os 


stopButton = Button(26) # defines the button as an object and chooses GPIO 26

while True: 
    
    if stopButton.is_pressed: #Check to see if button is pressed
        
        print("shutdown button pressed, waiting for confirmation (3 sec)")
        time.sleep(3) # wait for the hold time we want. 

        if stopButton.is_pressed: #check if the user let go of the button
            print("shutdown confirmed,  bye !")
            print("shutdown now -h")
            
            os.system("sudo shutdown now -h") #shut down the Pi -h is or -r will reset
        else:
            print("shutdown NOT confirmed !")
           
    time.sleep(1) # wait to loop again so we don’t use the processor too much.
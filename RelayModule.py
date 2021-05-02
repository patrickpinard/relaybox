# Auteur : Patrick Pinard 
# Objet : gestion de 4 relais 240V sur Raspeberry Pi Zero
# Version : 1
# -*- coding: utf-8 -*-

#   Clavier MAC :      

#  {} = "alt/option" + "(" ou ")"
#  [] = "alt/option" + "5" ou "6"
#   ~  = "alt/option" + n    
#   \  = Alt + Maj + / 
  
import logging
import RPi.GPIO as GPIO
import time

# fichier log
logging.basicConfig(filename='RelayModule.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DEBUG = True    # si True alors Logging de tous les events

pinRelay1 = 17  #pin11  fil jaune
pinRelay2 = 27  #pin13  fil orange
pinRelay3 = 22  #pin15  fil bleu
pinRelay4 = 23  #pin16  fil blanc

class Relay:

    """
    Classe definissant un relai caracterise par :
        - name : nom du relai, permet de localiser celui-ci 
        - pin : numero de la pin sur le pi
        - state : Etat du relai ON/OFF
    """

    def __init__(self, name, number, pin):
        """
        Constructeur de la classe Relay
        Connecté sur la pin GPIO 
        Etat du relai par défaut = OFF (GPIO.HIGH)
        """

        
        self.name = name
        self.pin = pin  
        self.number = number                                                      
        self.state = "OFF" 

        # GPIO setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.HIGH) 
        
        # debugging                                             
        if DEBUG : logging.info(" Relay : " + self.name + " is created and linked to PIN : " + str(self.pin) + " in OUT mode and set to : " + self.state)

    def __repr__(self):
        """
        Méthode permettant d'afficher les paramètres du relai
        """
    
        return "Relay : {0} on PIN : {1} set to : {2} ".format(self.name, self.pin, self.state)


    def on(self):
        """
        Méthode permettant de fermer le relai (on)
        Etat du relai par défaut = ON (GPIO.LOW)
        """
        GPIO.output(self.pin, GPIO.LOW)  
        self.state = "ON" 
        # debugging 
        if DEBUG : logging.info(" Relay : " + self.name + " on PIN : " + str(self.pin) + " is set to : " + self.state)


    def off(self):
        """
        Méthode permettant d'ouvrir le relai (off)
        Etat du relai par défaut = OFF (GPIO.HIGH)
        """
        GPIO.output(self.pin, GPIO.HIGH)  
        self.state = "OFF" 
        # debugging 
        if DEBUG : logging.info(" Relay : " + self.name + " on PIN : " + str(self.pin) + " is set to : " + self.state)
    


if __name__ == '__main__':

    Relay1 = Relay("r1", 1, pinRelay1)
    Relay2 = Relay("r2", 2, pinRelay2)
    Relay3 = Relay("r3", 3, pinRelay3)
    Relay4 = Relay("r4", 4, pinRelay4)
    

    try:
        while True : 

            
            print(Relay1)
            time.sleep(1)
            Relay1.on()
            print(Relay1)
            time.sleep(1)
            Relay1.off()

            
            print(Relay2)
            time.sleep(1)
            Relay2.on()
            print(Relay2)
            time.sleep(1)
            Relay2.off()

            
            print(Relay3)
            time.sleep(1)
            Relay3.on()
            print(Relay3)
            time.sleep(1)
            Relay3.off()

            
            print(Relay4)
            time.sleep(1)
            Relay4.on()
            print(Relay4)
            time.sleep(1)
            Relay4.off()
            
    except KeyboardInterrupt:
        GPIO.cleanup()




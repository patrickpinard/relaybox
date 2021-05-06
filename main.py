
#!/usr/bin/env python
# coding: utf-8
# Auteur    : Patrick Pinard
# Date      : 6.5.2021
# Objet     : Pilotage modules relais avec interface web basée sur API RESTful Flask et bootstrap sur PI zero 
# Version   :   1.1 - ajout du bouton shutdown externe
#               1.0 - version initiale fonctionelle
 
import RPi.GPIO as GPIO
from flask import Flask, render_template, request, redirect, jsonify, url_for, session, abort
import logging
import time
from gpiozero import Button         
import time                         
import os                           

stopButton = Button(26)             # external button to shutdown if pressed continously 2 sec

PASSWORD    = 'password'
USERNAME    = 'admin'



logging.basicConfig(filename='main.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
    17: {'name': '  Desk Lamp    ', 'state': GPIO.LOW, 'status': "OFF"},
    27: {'name': '  Charger      ', 'state': GPIO.LOW, 'status': "OFF"},
    22: {'name': '  Heating      ', 'state': GPIO.LOW, 'status': "OFF"},
}

# Set each pin as an output and make it low:
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

@app.route('/', methods=["GET", "POST"])
def login():
    
    if request.method == "GET":
        # Check if user already logged in
        
        if not session.get("logged_in"):
            logging.info("login not done, redirect to 'login' page")
            return render_template('login.html', error_message=" welcome ! ")
        else:
            logging.info("login already done, redirect to 'main' page")
            return render_template('main.html')

    if request.method == "POST":
        # Try to login user
        
        name = request.form.get("username")
        pwd = request.form.get("password")

        if pwd == PASSWORD and name == USERNAME:
                logging.info("user: " + name + " logged in")
                session['logged_in'] = True
                # For each pin, read the pin state and store it in the pins dictionary:
                for pin in pins:
                    pins[pin]['state'] = GPIO.input(pin)
                # Put the pin dictionary into the template data dictionary:
                templateData = {
                    'pins': pins
                }
                # Pass the template data into the template main.html and return it to the user
                return render_template('main.html', **templateData)
        else:
                logging.warning("login with wrong username and password")
                return render_template('login.html', error_message="wrong username and password. Please try again")

@app.route("/logout", methods=["GET",'POST'])
def logout():
    
    session["logged_in"] = False
    logging.info("user logout")
    return render_template('login.html')           

@app.route("/command/<changePin>/<action>")
def command(changePin, action):
    message =""
    # Convert the pin from the URL into an integer:
    changePin = int(changePin)
    # Get the device name for the pin being changed:
    deviceName = pins[changePin]['name']
    # If the action part of the URL is "on," execute the code indented below:
    if action == "on":
        # Set the pin high:
        GPIO.output(changePin, GPIO.HIGH)
        # Change the Status
        pins[changePin]['status'] = 'ON'
        # Save the status message to be passed into the template:
        message = "Turned " + deviceName + " on."
    if action == "off":
        GPIO.output(changePin, GPIO.LOW)
        pins[changePin]['status'] = 'OFF'
        message = "Turned " + deviceName + " off."
    if action == "toggle":
        # Read the pin and set it to whatever it isn't (that is, toggle it):
        GPIO.output(changePin, not GPIO.input(changePin))
        message = "Toggled " + deviceName + "."

    # For each pin, read the pin state and store it in the pins dictionary:
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)

    # Along with the pin dictionary, put the message into the template data dictionary:
    templateData = {
        'message': message,
        'pins': pins
    }

    return render_template('main.html', **templateData)

def shutdown(channel):
    # shutdown proprely raspberry pi zero if external button pressed 2 sec. continously
    
    global stopButton

    logging.info("stop button pressed... waiting for confirmation to shutdown.")
    if stopButton.is_pressed: #Check to see if button is pressed
        time.sleep(1) # wait for the hold time we want. 
        if stopButton.is_pressed: #check if the user let go of the button
            logging.info("shutdown raspberry pi confirmed by stop button pressed more than 2 sec.")
            os.system("shutdown now -h") #shut down the Pi -h is or -r will reset
            time.sleep(1) # wait to loop again so we don’t use the processor too much.
        

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    logging.info("program starting...")
    logging.info("pins definition : " + str(pins))
    GPIO.add_event_detect(stopButton, GPIO.RISING, callback=shutdown)  # waiting event to shutdown via external stop button 
    app.run(host='0.0.0.0', port=8000, debug=True)


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
import os                           

PASSWORD    = 'password'
USERNAME    = 'admin'

logging.basicConfig(filename='relaybox.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


app = Flask(__name__)

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
    r = request()
    print("request = ",r)
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

       

if __name__ == "__main__":
    app.secret_key = os.urandom(12)

    logging.info("########   Relaybox V1.0  #########")
    logging.info("program starting...")
    logging.info("pins definition : " + str(pins))
    
    app.run(host='0.0.0.0', port=8000, debug=True)

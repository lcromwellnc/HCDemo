The HCDemo is intended to be a sample app to highlight the SMS and Voice APIs available from Twilio.  The app consists of several Python files that send and recieve SMS messages and places an outbound call to an enduser. The app uses two Goggle Docs Sheets to retrieve and store data.

The theme of the app revolves around Healthcare and the role that SMS interactions can play to improve outcomes of patients and reduce the overall costs. Additional care is often more complex when a patient needs to be readmitted after their initial discharge from a hospital stay. There is ample result information from recognized Medical Associations of the efficacy of this simple use of SMS technology.

Note: This app only sends to a single subscriber in its present form but could easily be adapted to send to a wider audience.  Additionally, the use of Google Sheets for a data repository while functional and free it should be replaced with a more robust database.

The app uses the Flask and gspread modules and makes use of the ngrok utility to for Twilio to tunnel back to your PC to test the and run the code.

The files required for this application are:

    sendHealthTip.py - This sends a random tips that is pulled from the HealthTips Google Sheet to the subscriber
    
    weightcheck.py - This sends a reminder to the subscriber asking them to report their weight.
    
    medcheck.py - This sends a reminder to the subscriber asking them if they took their meds as prescribed.
    
    HCResponder.py - This file listens and responds to messages and voice interactions.
    
    HealthTips - aaaabbbbcccc.json - This is a credential file required by the app so it can access the Sheet files.
    
Installation Tips on Mac
========================
1) You need pip to install the required Python modules and libraries. If you don't have pip installed do the following:

    sudo easy_install pip
    
2) Install Flask - this is a Python based Web Server

    pip install Flask
    
3) Install Python modules needed by app

    sudo pip install gspread
    sudo pip install twilio
    sudo pip install oauth2client --upgrade --ignore-install six

4) Set environment variables used in the app

cd ~
nano .bash_profile

export TWILIO_ACCOUNT_SID=AC2b691d272423be8d147b7033766cab29
export TWILIO_AUTH_TOKEN=1732a50893a37cf11b6804f054f08f40
export TWILIO_NUMBER=+16202664198
export MY_PHONE_NUMBER=+19196569888

Restart terminal to have them take effect.

5) Download ngrok

Running ngrok

    ngrok http 5000
    
ngrok will then generate a list of items on the screen that show a URL running on the port specified (5000 in this case).  This URL changes each time you run the utility.

Session Status                online                                            
Version                       2.2.4                                             
Region                        United States (us)                                
Web Interface                 http://127.0.0.1:4040                             
Forwarding                    http://0093c2eb.ngrok.io -> localhost:5000        
Forwarding                    https://0093c2eb.ngrok.io -> localhost:5000       
In the above example the URL http://0093c2eb.ngrok.io must be specified in the Webhook field of the Twilio Console for SMS.  Additionally, the suffix must also be supplied.

For example in the Console for Phone numbers:

Messaging URL:  http://0093c2eb.ngrok.io/incoming




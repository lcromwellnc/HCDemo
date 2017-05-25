import threading
import os
import twilio
import gspread
import datetime
import twilio.twiml

from twilio.rest import Client
#from app import app, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from flask import request, make_response, render_template, Flask, redirect
from oauth2client.service_account import ServiceAccountCredentials
from twilio.twiml.messaging_response import MessagingResponse


twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
twilio_auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
twilio_number = os.environ.get('TWILIO_NUMBER')
#my_phone_number = os.environ.get('MY_PHONE_NUMBER')

CALL_TIMEOUT = 12   # Number of seconds to wait for answer before hanging up
RETRY_TIMER = 120   # Number of seconds to wait before retrying call
MAX_TRIES = 2       # If busy, no answer or no acknowledgement

root_url =  "http://598cf066.ngrok.io/"

app = Flask(__name__) 

def rotateWeights(subscribers): 
    # subscriber index starts at 0, spreadsheet start at 1
    # print(subscribers) 
    count = 10   # is spreadsheet index
    while count  > 3:
        
        subscribers[i][count+1] =subscribers[i][count-1]
        subscribers[i][count+2] = subscribers[i][count]
        
        Subscribersheet.update_cell(i + 1, count+2, subscribers[i][count+1])  # Date 
        Subscribersheet.update_cell(i + 1, count+3, subscribers[i][count+2]) # Weight
        
        count = count - 2

    return
    
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
#
creds = ServiceAccountCredentials.from_json_keyfile_name('HealthTips-0c88909c6863.json', scope)
client = gspread.authorize(creds)

# Open subscriber sheet but only use first subscriber for this demo

Subscribersheet = client.open("HealthSubscribers").sheet1
# Read in HealthSubscribers spreadsheet data(three columns of strings) into a list of lists
# Only using the first record[1] for demo

subscribers = Subscribersheet.get_all_values()  
goal = float(subscribers[1][13])
print(goal)
i = 1      # me

@app.route("/incoming", methods=['GET', 'POST'])
def HTResponder():
    """Respond to incoming replies with an appropriate simple text message."""
    """Looking for a number only, all other values get warning."""
    
    from_number = request.values.get('From', None)
    body_msg = request.values.get('Body', None)
    body_msg=body_msg.upper()
    medsYes = ['Y', 'YES']
    medsNo =['N','NO']
    
    if body_msg.isdigit():
        
        rotateWeights(subscribers)
        now = str(datetime.datetime.now())
        subscribers[i][3] = now         # datetime
        subscribers[i][4] = body_msg    # weight
        Subscribersheet.update_cell(i + 1, 4, now)      # datetime column
        Subscribersheet.update_cell(i + 1, 5, body_msg) # weight column
        
        if (float(body_msg) > (float(1.1 * float(goal)))) :
            print("you are getting fat") 
            resp = MessagingResponse().message("Looks like you are gaining weight and will be recorded as: " + body_msg)
            #print("TWIML code sent was: " + str(resp))
            make_call(twilio_number, subscribers[i][0], root_url, 1)
            return str(resp)
        else:
            resp = MessagingResponse().message("Thank you, your weight will be recorded as: " + body_msg)
            #print("TWIML code sent was: " + str(resp))
            return str(resp)
    
    elif any(st in body_msg for st in medsYes):
        resp = MessagingResponse().message("Good job! ")
        return str(resp)
    
    elif any(st in body_msg for st in medsNo):
        resp = MessagingResponse().message("Please take your meds as prescribed. ")
        return str(resp)
        
    else:
        resp = MessagingResponse().message("I'm don't understand your request. Please call our Hotline at 415-555-1212")
        return str(resp)
    

@app.route('/', methods=['GET', 'POST'])
@app.route('/call', methods=['GET', 'POST'])
def call():
    """Make an outbound call"""

    # Obtain the parameters and the host/app root URL.
    to_ = request.values.get('To', None)
    from_ = request.values.get('From', None)
    root_url = request.url_root
    print("Call routine url: "+ root_url)
    # If we don't have the parameters, ask the user to provide them.
    if to_ is None or from_ is None:
        return render_template("call.html", message="Please input the From and To numbers")

    # Otherwise, make the call.
    message = make_call(from_, to_, root_url, 1)
   
    return render_template("call.html", message=message)


def make_call(from_, to_, root_url, tries):
    """Make a REST API request to create a call."""
    print("Inside make_call: " + root_url)
    #client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client = Client(twilio_account_sid, twilio_auth_token)
    try:
        url = root_url + 'announcement?Tries=' + str(tries)
        status_callback = root_url + 'callended?Tries=' + str(tries)
        call = client.calls.create(to=to_,
                                   from_=from_,
                                   timeout=str(CALL_TIMEOUT),
                                   url=url,
                                   status_callback=status_callback)
        app.logger.info("Call initiated: From={0}, To={1}, URL={2}, StatusCallback={3}"
                        .format(from_, to_, url, status_callback))
        return "Call initiated..."
    except TwilioRestException as ex:
        app.logger.warn("Call failed: From={0}, To={1}, {2}"
                        .format(from_, to_, ex))
        return ex


@app.route('/announcement', methods=['GET', 'POST'])
def announcement():
    """Render TwiML to make an announcement."""

    # Get number of tries and render TwiML.
    tries = request.values.get('Tries', '1')
    template = render_template('announcement.xml', tries=tries)
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'
    return response


@app.route('/orderack', methods=['POST'])
def order_ack():
    """Render TwiML to acknowledge order acknowledgement."""

    # Log results.
    to_ = request.values.get('To', None)
    from_ = request.values.get('From', None)
    app.logger.info("Order acknowledged: From={0}, To={1}"
                    .format(from_, to_))

    # Render TwiML.
    template = render_template('acknowledgement.xml')
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'
    print("ack TWIML" + str(response))

    return response


@app.route('/noack', methods=['POST'])
def no_ack():
    """No acknowledgement; retry."""

    # Log results.
    to_ = request.values.get('To', None)
    from_ = request.values.get('From', None)
    tries = request.values.get('Tries', None)
    root_url = request.url_root
    app.logger.info("No acknowledgement: From={0}, To={1}, Tries={2}"
                    .format(from_, to_, tries))

    # Retry.
    if tries is not None and tries.isdigit():
        do_retry(from_, to_, root_url, int(tries))

    resp = twilio.twiml.Response().hangup()
    print("noack TWIML" + str(resp))
    return str(resp)


@app.route('/callended', methods=['POST'])
def call_ended():
    """URL invoked when call ends."""

    # Log call results.
    to_ = request.values.get('To', None)
    from_ = request.values.get('From', None)
    status = request.values.get('CallStatus', None)
    tries = request.values.get('Tries', None)
    root_url = request.url_root
    app.logger.info("Call ended: From={0}, To={1}, Status={2}, Tries={3}"
                    .format(from_, to_, status, tries))

    # Do we need to retry the call?
    if (status == "no-answer" or status == "busy") and tries is not None and tries.isdigit():
        do_retry(from_, to_, root_url, int(tries))

    return ('', 204)


def do_retry(from_, to_, root_url, num_tries):
    """Retry the call."""

    if num_tries < MAX_TRIES:
        num_tries = num_tries + 1
        threading.Timer(RETRY_TIMER, make_call, args=[from_, to_, root_url, num_tries]).start()
    return

if __name__ == "__main__":
    app.run(debug=True)
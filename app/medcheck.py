import gspread
import random
import os
import json
import pprint
import pdb

from oauth2client.service_account import ServiceAccountCredentials
from twilio.rest import Client

twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
twilio_auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
twilio_number = os.environ.get('TWILIO_NUMBER')
#my_phone_number = os.environ.get('MY_PHONE_NUMBER')

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

#print(subscribers)
i = 1      # me
phone_number = subscribers[i][0]
status = subscribers[i][1]
name = subscribers[i][2]

hmsg = " -- Hello " + name + " - \nDid you take your prescribed medications this morning?\n"
#print("processing..." +name)


twclient = Client(twilio_account_sid, twilio_auth_token)


message = twclient.messages.create(to=phone_number,from_=twilio_number,body=hmsg)
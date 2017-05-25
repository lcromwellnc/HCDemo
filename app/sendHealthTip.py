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

# States for subscriber: Blank - brand new and welcome message needs to be sent
#                        New - they have been welcomed and want Tips to be sent
#                        Active - they have been welcomed and want Tips to be sent


WelcomeMsg = " -- Welcome to Health Tips\n\nWe hope our daily tips bring you good health."
ControlMsg = "You can stop and start tips being sent by replying with STOP or START message."
HelpMsg = "Health Tips is a free service that sends you a few motivational messages each day to guide you to a healthy lifesytle."

def WelcomeToHT(name):
    
    hmsg = name + WelcomeMsg + "\n\n" + HelpMsg
    #print(hmsg)
    htstat = Subscribersheet.update_cell(i+1, 2,'Active')  # Change Status to Active after welcome has been sent
    message = twclient.messages.create(to=phone_number,from_=twilio_number,body=hmsg)
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

print(subscribers)
i = 1      # me
phone_number = subscribers[i][0]
status = subscribers[i][1]
name = subscribers[i][2]

#print("processing..." +name)

# Open up spreadsheet from Google docs for health tips

HTsheet = client.open("HealthTips").sheet1

# Read in HealthTips spreadsheet data(single column of strings) into a list of lists
# 
tips = HTsheet.get_all_values()  
#print(tips)

# pick a random tip from the list
hmsg = tips[random.randint(0,len(tips))]
print(hmsg)


twclient = Client(twilio_account_sid, twilio_auth_token)
if (status =="New") : 
    
    WelcomeToHT(name) 
    print("Came back from WelcomeToHT")

message = twclient.messages.create(to=phone_number,from_=twilio_number,body=hmsg)
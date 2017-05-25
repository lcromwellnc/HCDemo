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
    
def menu():
    print("\n Welcome to the Health Tips Demo\n")
    strs = ('Enter 1 for sending Weight Check SMS\n'
            'Enter 2 for sending Med Check SMS\n'
            'Enter 3 for sending Health Tip SMS\n\n'
            'Enter 5 for exit : ')
    choice = raw_input(strs)
    return int(choice)    

def weightcheck(name):
    hmsg = " -- Hello " + name + " - \nPlease tell us your weight this morning so we can track your recovery.\n" 
    message = twclient.messages.create(to=phone_number,from_=twilio_number,body=hmsg)
    return

def medcheck(name):
    hmsg = " -- Hello " + name + " - \nDid you take your prescribed medications this morning?\n" 
    message = twclient.messages.create(to=phone_number,from_=twilio_number,body=hmsg)
    return

def sendtip():
    # pick a random tip from the list
    hmsg = tips[random.randint(0,len(tips))]
    message = twclient.messages.create(to=phone_number,from_=twilio_number,body=hmsg)
    return

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
#
creds = ServiceAccountCredentials.from_json_keyfile_name('HealthTips-0c88909c6863.json', scope)
client = gspread.authorize(creds)

# Open subscriber sheet but only use first subscriber for this demo
print("Opening up Subscriber Sheet...")
Subscribersheet = client.open("HealthSubscribers").sheet1
# Read in HealthSubscribers spreadsheet data(three columns of strings) into a list of lists
# Only using the first record[1] for demo

subscribers = Subscribersheet.get_all_values()  
print("         ...Subscribers loaded.")

i = 1      # me
phone_number = subscribers[i][0]
status = subscribers[i][1]
name = subscribers[i][2]

#print("processing..." +name)

# Open up spreadsheet from Google docs for health tips
print("Opening up Health Tips Sheet...")
HTsheet = client.open("HealthTips").sheet1

# Read in HealthTips spreadsheet data(single column of strings) into a list of lists
# 
tips = HTsheet.get_all_values()  
print("      ...Health Tips loaded.")

twclient = Client(twilio_account_sid, twilio_auth_token)

# Check to see if this subscriber is new and send welcome if they are

if (status =="New") : 
    
    WelcomeToHT(name) 

while True:          #use while True
    choice = menu()
    if choice == 1:
        weightcheck(name)
    elif choice == 2:
        medcheck(name)
    elif choice == 3:
        sendtip()
    elif choice == 5:
        break

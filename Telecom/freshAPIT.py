from secureT import *
from matplotlib.axis import Tick
import requests
import json
import pandas as pd
import datetime
import os
import time
x=0
# Defines vars
while x ==0:
    page = 1

    ticketCount = 0

    Requesters=[]
    TicketID=[]
    Sub_Line=[]
    Agents=[]
    Building=[]
    data = {}
    tickets = []

    # Loop through the tickets and print the subject, ticket number, and building location of each ticket
    # Sorts the Data for the CSV
    def sortData(ticketArray):
        global ticketCount
        for ticket in ticketArray:
                ticketCount += 1
                print(str(datetime.datetime.now()) + ' Processing Ticket [' + str(ticketCount) + "]\r", end="")
                #Subject
                Sub_Line.append(ticket["subject"])

                #Ticket ID
                TicketID.append(ticket["id"])

                #Building
                Building.append(ticket["custom_fields"]["location"])

                #Get Responder and Requester Name with IDs
                requester_id = ticket["requester_id"]
                responder_id = ticket["responder_id"]
                requester_response = requests.get(f"{DOMAIN}/api/v2/requesters/{requester_id}", auth=(API_KEY, "X"))
                responder_response = requests.get(f"{DOMAIN}/api/v2/agents/{responder_id}", auth=(API_KEY, "X"))
                
                #Responders
                if responder_response.status_code == 200:
                    responder_data = json.loads(responder_response.content)
                    Agents.append(responder_data["agent"]["first_name"])
                else:
                    Agents.append("Unassigned")
                
                #Requesters
                if requester_response.status_code == 200:
                    requester_data = json.loads(requester_response.content)
                    fName=(requester_data["requester"]["first_name"])   
                    lName=(requester_data["requester"]["last_name"])
                    if lName==None:
                        Requesters.append(fName)
                    else:
                        Name=fName+" "+lName
                        Requesters.append(Name)

                else:
                    Requesters.append("Unassigned")


        

    #Script
    while((page == 1 or response.status_code == 200) and page != 0):

        print(str(datetime.datetime.now()) + " Getting page : "  + str(page))
        endpoint = str(DOMAIN) +'/api/v2/tickets/filter?query="status:2%20AND%20group_id:' + str(GROUP_ID) + '"&page='+ str(page)
        response = requests.get(endpoint, auth=(API_KEY, "X"))

        if response.status_code == 200:

            # Parse the JSON response
            data = json.loads(response.content)

            # if there are no tickets in the JSON file
            if(str(data)[:14] == "{'tickets': []"):
                print(str(datetime.datetime.now()) +" No more tickets!")
                page = -1
                break
                
            # Retrieve the tickets in the group
            tickets.append(data["tickets"])
            
        
            page += 1
        else:
            print(str(datetime.datetime.now()) + " Request failed with status code", response.status_code)


    # Loops through the different pages of tickets and send them to sortData before the CSV is made
    print("\n" + str(datetime.datetime.now()) + " Making CSV!")
    for i in tickets:
        sortData(i)
    print("\n" + str(datetime.datetime.now()) + " CSV Creation Done")

    df = pd.DataFrame({'Requester':Requesters,'TicketID':TicketID,'Summary':Sub_Line,'Building':Building,'AgentName':Agents})
    df.to_csv('/home/freshservice/Telecom/directoryT.csv', index=False, encoding='utf-8')
    try:
        os.popen('sh /home/freshservice/Telecom/scpT.sh')
        print("Sent to Grafana!")
    except:
        time.sleep(1)
        print("Could not connect to Grafna")
    time.sleep(500)

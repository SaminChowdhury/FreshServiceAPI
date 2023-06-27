from secure import *
from matplotlib.axis import Tick
import requests
import json
import pandas as pd
from datetime import datetime
from datetime import timedelta
import time
import os

x=0
# Defines vars
while x ==0:
    cpage = 1

    SticketCount = 0
    TticketCount = 0
    HticketCount = 0
    SticketCountOpen = 0
    TticketCountOpen = 0
    HticketCountOpen = 0

    Sticket=[]
    Tticket=[]
    Hticket=[]
    SticketOpen=[]
    TticketOpen=[]
    HticketOpen=[]

    data = {}
    Ctickets = []
    # --Make date--
    now = datetime.now()
    dt_now = now.strftime('%Y-%m-%d %H:%M:%S')
    dt_now = datetime.strptime(dt_now, '%Y-%m-%d %H:%M:%S')
    start_of_week = dt_now - timedelta(days=dt_now.weekday())  # Monday
    start_of_week = start_of_week.strftime('%Y-%m-%dT00:00:00Z')
    
    # Loop through the tickets and print the subject, ticket number, and building location of each ticket
    # Sorts the Data for the CSV
    def sortData(ticketArray):
        global SticketCount
        global TticketCount
        global HticketCount
        global SticketCountOpen
        global TticketCountOpen
        global HticketCountOpen

        for Cticket in ticketArray:
                if (Cticket["status"]==5):
                    if (Cticket["group_id"]==15000283771): #SystemAdmin
                        SticketCount += 1
                        print(' Processing Ticket SysAdmin [' + str(SticketCount) + "]\r", end="")
                    if (Cticket["group_id"]==15000283767): #Telecom
                        TticketCount += 1
                        print(' Processing Ticket SysAdmin [' + str(TticketCount) + "]\r", end="")
                    if (Cticket["group_id"]==15000283766): #HelpDesk
                        HticketCount += 1
                        print(' Processing Ticket SysAdmin [' + str(HticketCount) + "]\r", end="")

                if (Cticket["status"]==2):
                    if (Cticket["group_id"]==15000283771): #SystemAdmin
                        SticketCountOpen += 1
                        print(' Processing Ticket SysAdmin [' + str(SticketCountOpen) + "]\r", end="")
                    if (Cticket["group_id"]==15000283767): #Telecom
                        TticketCountOpen += 1
                        print(' Processing Ticket SysAdmin [' + str(TticketCountOpen) + "]\r", end="")
                    if (Cticket["group_id"]==15000283766): #HelpDesk
                        HticketCountOpen += 1
                        print(' Processing Ticket SysAdmin [' + str(HticketCountOpen) + "]\r", end="")

                    else:
                        continue 


        

    #Script
    while((cpage == 1 or response.status_code == 200) and cpage != 0):

        print(" Getting page : "  + str(cpage))
        endpoint = str(DOMAIN) +'/api/v2/tickets?updated_since='+str(start_of_week)+'&page='+str(cpage)

        
        response = requests.get(endpoint, auth=(API_KEY, "X"))

        if response.status_code == 200:

            # Parse the JSON response
            data = json.loads(response.content)

            # if there are no tickets in the JSON file
            if(str(data)[:14] == "{'tickets': []"):
                print(" No more tickets!")
                cpage = -1
                break
                
            # Retrieve the tickets in the group
            Ctickets.append(data["tickets"])
            
        
            cpage += 1
        else:
            print( " Request failed with status code", response.status_code)
        #if (cpage ==5):
            #break


    # Loops through the different pages of tickets and send them to sortData before the CSV is made
    print("\n" + " Making CSV!")
    for z in Ctickets:
        sortData(z)
    Sticket.append(SticketCount)
    Hticket.append(HticketCount)
    Tticket.append(TticketCount)
    SticketOpen.append(SticketCountOpen)
    HticketOpen.append(HticketCountOpen)
    TticketOpen.append(TticketCountOpen)

    df = pd.DataFrame({'SystemAdminOpen':SticketOpen,'SystemAdminClosed':Sticket,'TelecomOpen':TticketOpen,'TelecomClosed':Tticket,'HelpdeskOpen':HticketOpen,'HelpdeskClosed':Hticket})
    df.to_csv('/home/freshservice/ClosedTickets/ClosedTickets.csv', index=False, encoding='utf-8')
    print("\n" + " CSV done!")
    try:
        os.popen('sh /home/freshservice/ClosedTickets/scp.sh')
        print("Sent To Grafana")
    except:
        time.sleep(1)
        print("Could not connect to Grafana")
    time.sleep(300)

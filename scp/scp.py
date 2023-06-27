import os 
while True:
    try:
        os.popen('sh /home/freshservice/ClosedTickets/scp.sh')
        print("Sent To Grafana")
    except:
        time.sleep(1)
        print("Could not connect to Grafana")

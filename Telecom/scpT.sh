#!/bin/bash

# Define the source and destination file paths
source_file="/home/freshservice/Telecom/directoryT.csv"
destination="ocissecadmin@10.100.0.22:/usr/share/grafana/reports/"

# Use the scp command to transfer the file

scp $source_file $destination

# Print a message to confirm the transfer
echo "File transfer complete!"


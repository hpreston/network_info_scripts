#! /usr/bin/env python
"""Exploring Genie's ability to gather details and write to CSV

This script is meant to be run line by line interactively in a Python
interpretor (such as iPython) to learn how the Genie and csv libraries work.

This script assumes you have a virl simulation running and a testbed file
created.

Example:

virl up --provision virlfiles/5_router_mesh
virl generate pyats -o testbed.yaml

Copyright (c) 2018 Cisco and/or its affiliates.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Import the Genie library
from genie.conf import Genie

# Create a testbed object
testbed = Genie.init("testbed.yaml")

# Take a look at the devices that are in the testbed
print(testbed.devices)

# Create a "convenience" variable for one device
iosv1 = testbed.devices["iosv-1"]

# Connect to the router
iosv1.connect()

# Check that you are connected
iosv1.connected


# Run the "show interfaces" command and "parse" results to Python object
interfaces = iosv1.parse("show interfaces")

# Print the parsed data
print(interfaces)

# That's a lot of data, let's explore it some..
# Look at the first set of dictionary keys avialable
interfaces.keys()

# Now let's checkout one interface in a pretty printed way
from pprint import pprint
pprint(interfaces["GigabitEthernet0/0"])

# Much nicer... now let's just get the mac-address for one interface
interfaces["GigabitEthernet0/0"]["mac_address"]

# Suppose we wanted the IP address...
interfaces["GigabitEthernet0/0"]["ipv4"]

# Now let's create a CSV file of the MAC Addresses for each interface
# Import in the CSV library
import csv

# Name our CSV file
interface_file = "interfaces.csv"

# Let's setup the headers for our CSV file
report_fields = ["Interface", "MAC Address"]

# Now let's open up our file and create our report
# This whole block of text from `with` and everything
# indented under it will run at once.  Copy or type it all in.
# DON'T FORGET TO SPACE OVER IF TYPING MANUALLY
with open(interface_file, "w") as f:
    # Create a DictWriter object
    writer = csv.DictWriter(f, report_fields)
    # Write the header row
    writer.writeheader()
    # Loop over each interface and write a row
    for interface, details in interfaces.items():
        writer.writerow({"Interface": interface, "MAC Address": details["mac_address"]})

# Uh oh.. did you get a "KeyError: 'mac_address'"?
# That's because Loopbacks do NOT have mac_addresses.
# See for yourself...
interfaces["Loopback0"].keys()

# So we need to create our code so we can handle interfaces without mac-addresses
# Several ways you COULD do it, here's one.  A "try... except... " block
with open(interface_file, "w") as f:
    writer = csv.DictWriter(f, report_fields)
    writer.writeheader()
    for interface, details in interfaces.items():
        # Try to write a row with a mac-address
        try:
            writer.writerow(
                {
                    "Interface": interface,
                    "MAC Address": details["mac_address"],
                }
            )
        except KeyError:
            # If there isn't one... use "N/A"
            writer.writerow(
                {
                    "Interface": interface,
                    "MAC Address": "N/A"}
            )

# Great... let's see what was written.
# Open up the file again for "r"eading (also the default)
with open(interface_file, "r") as f:
    # Just print it out
    print(f.read())

# Great job!

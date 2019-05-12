#! /usr/bin/env python
"""Sample script to gather MAC addresses for interfaces into csv

This script leverages the Genie Python Library to learn details about network
interfaces and then write them to a CSV file.

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

# Import our libraries
from genie.conf import Genie
import csv

# Create a testbed object for the network
testbed = Genie.init("testbed.yaml")

# Create an empty dictionary that will hold the details we'll write to the CSV
device_interface_details = {}

# Loop over each device in the network testbed
for device in testbed.devices:
    # Connect to the device
    testbed.devices[device].connect()

    # Run the "show interfaces" command on the device
    interface_details = testbed.devices[device].parse("show interfaces")
    #   Note: see available commands to parse for each platform at
    #         https://pubhub.devnetcloud.com/media/pyats-packages/docs/genie/genie_libs/#/parsers
    #   Extra Note: IOS uses "show interfaces" NX-OS uses "show interface"
    #     so the below will work on IOS, but not NX-OS.
    #     A "better option" would be to .learn("interface") which works on
    #     all platforms

    # Store this devices interface details into the dictionary
    device_interface_details[device] = interface_details

# The name for our report file
interface_file = "interfaces.csv"

# The headers we'll use in the CSV file
report_fields = ["Device", "Interface", "MAC Address"]

# Open up the new file for "w"riting
with open(interface_file, "w") as f:
    # Create a CSV "DictWriter" object providing the list of fields
    writer = csv.DictWriter(f, report_fields)
    # Write the header row to start the file
    writer.writeheader()

    # Loop over each device and interface details we gathered and stored
    for device, interfaces in device_interface_details.items():
        # Loop over each interface for the current device in the outer loop
        for interface, details in interfaces.items():
            # Attempt to write a row. If an interface lacks a MAC (ie Loopback)
            # it will raise a "KeyError"
            try:
                writer.writerow(
                    {
                        "Device": device,
                        "Interface": interface,
                        "MAC Address": details["mac_address"],
                    }
                )
            except KeyError:
                # Loopback interfaces lack a mac_address, mark it as "N/A"
                writer.writerow(
                    {"Device": device, "Interface": interface, "MAC Address": "N/A"}
                )

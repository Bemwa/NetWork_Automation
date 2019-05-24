__author__ = "Bemwa Refaat Aziz"
__EMAIL__ = "engbmwa@gmail.com"

from netmiko import ConnectHandler
from netmiko.ssh_exception import AuthenticationException,NetMikoAuthenticationException, NetMikoTimeoutException
import xlrd
import datetime

start_time = datetime.datetime.now().replace(microsecond=0)

# Read the Hosts details and credentials from Excel file and save the all details to list of DIC
try:
    workbook=xlrd.open_workbook("C:\\python_Scripts\\send_configuration\\hosts\\hosts.xlsx")
    sheet = workbook.sheet_by_index(0)

    device_list = []
    hostname_device_list = {}
    for index in range(1, sheet.nrows):
        hostname = sheet.row(index)[0].value
        ipaddress = sheet.row(index)[1].value
        username = sheet.row(index)[2].value
        password = sheet.row(index)[3].value
        enable_password = sheet.row(index)[4].value
        vendor = sheet.row(index)[5].value
        device = {
            'device_type': vendor,
            'ip': ipaddress,
            'username': username,
            'password': password,
            'secret': enable_password,
        }
        device_list.append(device)
        # this DIC to be used for formatting the heading of each router NOT for Netmiko
        hostname_device_list[sheet.row(index)[1].value] = sheet.row(index)[0].value

    # set the path of the text file that contain the required show commands and pass it to the read fn
    cisco_commands = "C:\\python_Scripts\\send_configuration\\commands\\cisco_cmd.txt"
    junos_commands = "C:\\python_Scripts\\send_configuration\\commands\\junos_cmd.txt"
    xr_commands = "C:\\python_Scripts\\send_configuration\\commands\\xr_cmd.txt"

    for item in device_list:
        print ("Access Network Device : " + str(hostname_device_list[item["ip"]]))
        # Customize my script to these network Boxes only
        try:
            if item["device_type"] in ["cisco_ios","juniper","cisco_xr"]:
                # Connect the network device via Netmiko connecthandler fn
                connection = ConnectHandler(**item)
                connection.enable()
                print "Connected Successfully"
                if item["device_type"] == "cisco_ios":
                    print "Script not ready for ios now, to be updated soon"
                elif item["device_type"] == "juniper":
                    connection.send_command("\n")
                    print (connection.send_config_from_file(junos_commands,exit_config_mode=False,delay_factor=10))
					# the IF to make double check before commit the new configuration 
                    x = raw_input(" A commit wala ? Y/N  ::").lower()
                    if x == "y":
                        print (connection.send_config_set("commit"))
                    else:
                        print (connection.send_config_set("rollback 0"))
                elif item["device_type"] == "cisco_xr":
                    print "Script not ready for XR now"
            else:
                print "unknown Device Type"
                continue
        except NetMikoTimeoutException as c:
            print ("Connection error with " + str(hostname_device_list[item["ip"]])+"  >>>  " + str(c))
        except NetMikoAuthenticationException as z:
            print ("Connection error with " + str(hostname_device_list[item["ip"]])+"  >>>  " + str(z))
        except AuthenticationException as q:
            print ("Connection error with " + str(hostname_device_list[item["ip"]])+"  >>>  " + str(q))


    end_time = datetime.datetime.now().replace(microsecond=0)

    print ("total_time " + str(end_time - start_time))

except Exception as e:
    print e

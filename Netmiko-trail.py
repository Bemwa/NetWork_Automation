from netmiko import ConnectHandler
from netmiko.ssh_exception import AuthenticationException,NetMikoAuthenticationException, NetMikoTimeoutException
import xlrd
import datetime

# function to read the required commands form txt file and return the commands as items in list
def read_commands(x):
    try:
        commands = []
        cmd_file = open(x,"r")
        cmd_file.seek(0)
        for each_line in cmd_file.readlines():
            commands.append(each_line)
        cmd_file.close()
        return commands
    except IOError as f:
        print f
        exit()

start_time = datetime.datetime.now().replace(microsecond=0)

# Read the Hosts details and credentials from Excel file and save the all details to list of DIC
try:
    workbook=xlrd.open_workbook("C:\\Users\\Bemwa\\PycharmProjects\\NetMiko-trail01\\hosts1.xlsx")
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

    # create a unique output file name each time the script run
    date = datetime.datetime.now()
    script_date = str(date.day) + "-" + str(date.month) + "-" + str(date.year) + "@" + str(date.hour) + "%" + str(
        date.minute) + "%" + str(date.second)
    script_Path = "C:\\Users\\Bemwa\\PycharmProjects\\NetMiko-trail01\\Output-" + script_date + ".txt"
    output_file = open(script_Path, "a")

    # set the path of the text file that contain the required show commands and pass it to the read fn
    ios = "C:\\Users\\Bemwa\\PycharmProjects\\NetMiko-trail01\\cisco_cmd.txt"
    junos = "C:\\Users\\Bemwa\\PycharmProjects\\NetMiko-trail01\\junos_cmd.txt"
    xr = "C:\\Users\\Bemwa\\PycharmProjects\\NetMiko-trail01\\xr_cmd.txt"

    cisco_commands = read_commands(ios)
    junos_commands = read_commands(junos)
    xr_commands = read_commands(xr)

    for item in device_list:
        print ("Access Network Device : " + str(hostname_device_list[item["ip"]]))
        output_file.write("Access Network Box : " + str(hostname_device_list[item["ip"]]) + " " + "(" + str(item["ip"])+")"+"\n")
        output_file.write("="*(len("Access Network Box : ")+len(str(hostname_device_list[item["ip"]])+" "+"("+str(item["ip"])+")"))+"\n")
        # Customize my script to these network Boxes only
        try:
            if item["device_type"] in ["cisco_ios","juniper","cisco_xr"]:
                # Connect the network device via Netmiko connecthandler fn
                connection = ConnectHandler(**item)
                connection.enable()
                print "Connected Successfully"
                if item["device_type"] == "cisco_ios":
                    for cmd in cisco_commands:
                        print ("Command send > " + cmd)
                        output_file.write(connection.send_command(cmd,delay_factor=10,strip_command=False,strip_prompt=False) + "\n")
                elif item["device_type"] == "juniper":
                    for cmd in junos_commands:
                        print ("Command send > " + cmd)
                        output_file.write(connection.send_command(cmd,delay_factor=10,strip_command=False,strip_prompt=False) + "\n")
                        print " Get the output"
                elif item["device_type"] == "cisco_xr":
                    for cmd in xr_commands:
                        print ("Command send > " + cmd)
                        output_file.write(connection.send_command(cmd,delay_factor=10,strip_command=False,strip_prompt=False) + "\n")
            else:
                print "unknown Device Type"
                output_file.write("unknown Device" + "\n")
                continue
        except NetMikoTimeoutException as c:
            print ("Connection error with " + str(hostname_device_list[item["ip"]])+"  >>>  " + str(c))
        except NetMikoAuthenticationException as z:
            print ("Connection error with " + str(hostname_device_list[item["ip"]])+"  >>>  " + str(z))
        except AuthenticationException as q:
            print ("Connection error with " + str(hostname_device_list[item["ip"]])+"  >>>  " + str(q))
        output_file.write(90 * "-" + "\n")
        output_file.write(90 * "/" + "\n")
        output_file.write(90 * "-" + "\n")

    output_file.close()
    end_time = datetime.datetime.now().replace(microsecond=0)

    print ("total_time " + str(end_time - start_time))

except Exception as e:
    print e

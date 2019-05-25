__author__ = "Bemwa Refaat Aziz"
__EMAIL__ = "engbmwa@gmail.com"

# this script to retrieve the junos candidate configuration (Backup Configuration) by get the junos devices credentials
# from Excel sheet then use PyEZ .rpc.get_config() to get the required configuration and save it in unique txt file

from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
import datetime
import xlrd
from lxml import etree

start_time = datetime.datetime.now().replace(microsecond=0)

def PyEZ_Hosts_from_xls(w):
    workbook = xlrd.open_workbook(w)
    sheet = workbook.sheet_by_index(0)
    device_list = []
    for index in range(1, sheet.nrows):
        ip_address = sheet.row(index)[0].value
        user_name = sheet.row(index)[1].value
        password = sheet.row(index)[2].value
        device = {
            'ip': ip_address,
            'username': user_name,
            'password': password,
        }
        device_list.append(device)
    return device_list


r = "C:\\python_Scripts\\Junos_Backup\\hosts.xlsx"
device_list = PyEZ_Hosts_from_xls(r)

# In order to create unique output file name each time the script run >> part of the output file will be a time stamp
date = datetime.datetime.now()
script_date = str(date.day) + "-" + str(date.month) + "-" + str(date.year) + "@" + str(date.hour) + "%" + str(
    date.minute) + "%" + str(date.second)


# for loop to pass the device [] and use the credentials to connect using PyEZ over port TCP 22
for item in device_list:
    dev = Device(host=item["ip"],user=item["username"],password=item["password"],port=22)
    try:
        dev.open()
        print ("connected to " + dev.facts["hostname"])
        script_Path = "C:\\python_Scripts\\Junos_Backup\\Backup_files\\Backup-" + dev.facts["hostname"] + script_date + ".txt"
        output_file = open(script_Path, "w")
        print "create file for Backup"
        # retrive the needed configuration with set format , for junos version above 14 you can use set fromat
        data = dev.rpc.get_config(options={'format': 'text'})
        output_file.write(etree.tostring(data, encoding='unicode', pretty_print=True))
        print "saving the Backup Configuration ...."
        output_file.close()
    except ConnectError as err:
        print ("Cannot connect to device: {0}".format(err))
    except Exception as err:
        print (err)
    try:
        dev.close()
    except Exception as err:
        print (err)

end_time = datetime.datetime.now().replace(microsecond=0)
print ("total_time " + str(end_time - start_time))


z = raw_input(" Press Enter to Exit ")
while z != "":
    exit()

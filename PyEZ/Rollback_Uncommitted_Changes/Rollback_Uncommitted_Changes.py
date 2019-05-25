__author__ = "Bemwa Refaat Aziz"
__EMAIL__ = "engbmwa@gmail.com"

from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import ConnectError
import datetime
import xlrd

start_time = datetime.datetime.now().replace(microsecond=0)

# get the devices info and credentials from sheet Excel
# Excel sheet consist of three Col <ip address><username><password>

workbook = xlrd.open_workbook("C:\\python_Scripts\\Rollback_Uncommitted_Changes\\hosts.xlsx")
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

q = 0
# for loop to pass the device [] and use the credinitials to connect using PyEZ over port TCP 22
for item in device_list:
    dev = Device(host=item["ip"],user=item["username"],password=item["password"],port=22)
    try:
        dev.open()
        print ("connected to " + dev.facts["hostname"])
        q = q + 1
        Box = Config(dev)
        # create var to save the diff conf , you can change the rb_id# to define which committed configuration you need to comapre with
        Uncommitted = Box.diff(rb_id=0)
        # if section to check if there are an Uncommitted Changes to be displayed before rollback
        if Uncommitted:
            print "There are an Uncommitted Changes"
            print Uncommitted
            Box.rollback()
            print "Rollback Done"
        else:
            print "Uncommitted Changes Not Found, Exit"
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
print ("no of junos devices " + str(q))
z = raw_input(" Press Enter to Exit ")
while z != "":
    exit()

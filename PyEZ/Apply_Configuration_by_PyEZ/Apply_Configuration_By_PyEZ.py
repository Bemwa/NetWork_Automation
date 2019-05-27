__author__ = "Bemwa Refaat Aziz"
__EMAIL__ = "engbmwa@gmail.com"

from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import ConnectError
import datetime
import xlrd

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


r = "C:\\python_Scripts\\Apply_Junos_Conf\\hosts.xlsx"
device_list = PyEZ_Hosts_from_xls(r)

# for loop to pass the device [] and use the credentials to connect using PyEZ over port TCP 22
for item in device_list:
    dev = Device(host=item["ip"],user=item["username"],password=item["password"],port=22)
    try:
        dev.open()
        jo = Config(dev,mode='private')
        jo.load(path="C:\\python_Scripts\\Apply_Junos_Conf\\Junos_cmds.txt",merge=True,format="set")
        print jo.diff()
        jo.commit()
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
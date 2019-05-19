__author__ = "Bemwa Refaat Aziz"
__EMAIL__ = "engbmwa@gmail.com"

from jnpr.junos import Device
import xlrd , xlwt
from jnpr.junos.exception import ConnectError
import datetime

start_time = datetime.datetime.now().replace(microsecond=0)

# get the devices info and credentials from sheet Excel
# Excel sheet consist of three Col <ip address><username><password>

workbook = xlrd.open_workbook("C:\\Users\\Bemwa\\PycharmProjects\\Pyez-test\\hosts.xlsx")
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

# Using Netmiko , Loop to pass all devices and extract certain facts and save to facts_List > it's list of DIC
# each Dic represent one device

facts_List = []
for item in device_list:
    dev = Device(host=item["ip"],user=item["username"],password=item["password"],port=22)
    try:
        dev.open()
        print ("connected to " + dev.facts["hostname"])
        # creating Custom Dic of devices facts
        router_fact = {"2RE":dev.facts["2RE"],"current_re":dev.facts["current_re"],"hostname":dev.facts["hostname"],
                       "master":dev.facts["master"],"model":dev.facts["model"],"RE0":dev.facts["RE0"],
                       "RE1":dev.facts["RE1"],"serialnumber":dev.facts["serialnumber"],
                       "switch_style":dev.facts["switch_style"],
                       "version":dev.facts["version"]}
        facts_List.append(router_fact)
        print "get the facts"
        print facts_List
    except ConnectError as err:
        print ("Cannot connect to device: {0}".format(err))
    except Exception as err:
        print (err)
    try:
        dev.close()
    except Exception as err:
        print (err)

# Create the font specs for the first raw Heading
font = xlwt.Font()          # Create the Font
font.name = 'Times New Roman'
font.bold = True
font.height = 220
style = xlwt.XFStyle() # Create the Style
style.font = font # Apply the Font to the Style


# fill XLS sheet with Devices facts
workbook = xlwt.Workbook(encoding = 'ascii')
worksheet = workbook.add_sheet('Juniper Inventory')
keys = ["hostname","2RE","current_re","master","model","RE0","RE1","serialnumber","switch_style","version"]
for item in keys:
    worksheet.write(0,keys.index(item),item,style=style)

x = 0
for no in range(len(facts_List)):
    vlaues = []
    x = x + 1
    y = 0
    fact_details_dic = (facts_List[no])
    for item in keys:
        vlaues.append(fact_details_dic[item])
    while y < len(vlaues):
        worksheet.write(x,y,str(vlaues[y]))
        y = y + 1
workbook.save("PACO-Juniper inventory-3.xls")

end_time = datetime.datetime.now().replace(microsecond=0)
print ("total_time " + str(end_time - start_time))
z = raw_input(" Press Enter to Exit ")
while z != "":
    exit()

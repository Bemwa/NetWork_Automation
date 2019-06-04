__author__ = "Bemwa Refaat Aziz"
__EMAIL__ = "engbmwa@gmail.com"

# the below script is to catch the flapping interfaces within predefined hours that my cause any routing changes

from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from lxml import etree
import jxmlease,re,xlrd,datetime

# wait the user untill submit right integar no
while True:
    try:
        hr = int(raw_input("Enter the No of Hours to check the flapping within (0-24) :"))
        break
    except:
        print "Invalid No. of Hours"

print "\n"
start_time = datetime.datetime.now().replace(microsecond=0)

# Fn to read the nodes credentials from excel file and return it as List of Dic
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


r = "C:\\python_Scripts\\Catch_the_flapped_junos_interface\\hosts.xlsx"
device_list = PyEZ_Hosts_from_xls(r)

# for loop to pass the device [] and use the credentials to connect using PyEZ over port TCP 22
for item in device_list:
    dev = Device(host=item["ip"],user=item["username"],password=item["password"],port=22,normalize=True)
    try:
        dev.open()
        print ("Connected to " + dev.facts["hostname"])
        # use get RPC to retrieve the interface info
        data = dev.rpc.get_interface_information()
        # Parse the return xml data into python data structure
        XML_data = etree.tostring(data, pretty_print=True, encoding='unicode')
        result = jxmlease.parse(XML_data)
        # for loop to iterate over each physical interface and extract the last flapping time
        for index in result["interface-information"]["physical-interface"]:
            if str(index["name"]).startswith(("ge", "ae", "et", "fe", "fxp", "xe", "reth")):
                # usually the flapping format is "2018-12-19 03:18:22 UTC (05:48:14 ago)"
                # regex used to match this part <(05:> then remove extra char
                match = re.search(".\(\d\d:", str(index["interface-flapped"]))
                if match:
                    y = int(match.group().replace("(","").replace(":",""))
                    if hr >= y:
                        print ("Interface " + index["name"] + " flapped @ " + str(index["interface-flapped"]))
                        # try clause here to avoid error raised if interface has no description
                        try:
                            print ("Interface description : "+str(index["description"]))
                        except KeyError as e:
                            print ("No " + str(e) + " found")
    except ConnectError as err:
        print ("Cannot connect to device: {0}".format(err))
    except Exception as err:
        print ("Error found : {0}".format(err))
    try:
        dev.close()
        print ("Exit Node " + dev.facts["hostname"])
        print 40*"^"
        print 1 * "\n"
    except Exception as err:
        print (err)

end_time = datetime.datetime.now().replace(microsecond=0)
print ("total_time " + str(end_time - start_time))

z = raw_input(" Press any key to Exit ")
while z != "":
    exit()

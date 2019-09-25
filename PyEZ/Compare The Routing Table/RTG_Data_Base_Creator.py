__author__ = "Bemwa Refaat Aziz"
__EMAIL__ = "engbmwa@gmail.com"

from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from lxml import etree
import jxmlease,datetime,re, os
from sortedcontainers import SortedDict

# This Script aimed to extract the full routes in the Routing Table with its NextHop Details
# and save it in Dictionary format (each VRF in separated Dic) and save it finally in Txt file as Database

Host = raw_input("Please enter the Host IP address : ")
User = raw_input("Please entter the Username : ")
Pass = raw_input("Please enter the Password : ")

start_time = datetime.datetime.now().replace(microsecond=0)

dev = Device(host=Host, user=User, password=Pass, port=22,normalize=True)
try:
    dev.open(auto_probe=5)
    print "Device Connected, Extracting the Routes , Please Wait ... "
    data = dev.rpc.get_route_information()
except ConnectError as err:
    print ("Cannot connect to device: {0}".format(err))
except Exception as err:
    print (err)
try:
    dev.close()
except Exception as err:
    print (err)

XML_data = etree.tostring(data, pretty_print=True, encoding='unicode')
result = jxmlease.parse(XML_data)

try:
    script_Path = "C:\\python_Scripts\\RTG_Compare\\backup.txt"
    backup_file = open(script_Path, "w")
except IOError:
    print "Error to set the txt file for backup"

# Parsing the XML Output (DIC) to extract the Route and its Nexthop details
# Save the Output from the For Loop into Dic >> Key is the route , Value is a List of [ Routing protocol, Protocol
# Preference, Nexthop IP, Exit interface]
for vrf in result['route-information']['route-table']:
    # Script is Limited to L3 VRF Routes only (no MPLS, No L2vpn ,,)
    if "inet.0" not in (str(vrf["table-name"])):
        continue
    else:
        print "<<<< Access Routing instance "+ str(vrf["table-name"]+ ">>>>>>")
        x = SortedDict()
        for route in vrf["rt"]:
            # Discard wellKnown Multicast Subnet used by the Routing Protocols (IP start with 224)
            if re.search("^224.",str(route["rt-destination"])):
                continue
            else:
                # Match all possible combination for the XML output
                print "- Route :  " + route["rt-destination"]
                y = route["rt-destination"]
                z = []
                # the Output of the "Route Entry" sometimes be a DIC or A List , depending on the Route Type.
                if isinstance((route['rt-entry']),dict):
                    print "-- protocol-name : " + route['rt-entry']['protocol-name']
                    z.append(str(route['rt-entry']['protocol-name']))
                    print "-- preference : " + route['rt-entry']['preference']
                    z.append(int(route['rt-entry']['preference']))
                    if route['rt-entry']['protocol-name'] == "Local":
                        if route['rt-entry']["nh-type"] == "Reject":
                            print "-- nh ip : Reject"
                            z.append("Reject")
                        else:
                            print "-- nh-local-interface : " + route['rt-entry']["nh"]["nh-local-interface"]
                            z.append(str(route['rt-entry']["nh"]["nh-local-interface"]))
                    elif route['rt-entry']['protocol-name'] == "Direct":
                        print "-- Direct-interface : " + route['rt-entry']["nh"]["via"]
                        z.append(str(route['rt-entry']["nh"]["via"]))
                    elif route['rt-entry']['protocol-name'] == "Static":
                        if "nh" in (route['rt-entry']):
                            if "nh-table" in route['rt-entry']['nh']:
                                print "-- nh table : " + route['rt-entry']['nh']["nh-table"]
                                z.append(str(route['rt-entry']['nh']["nh-table"]))
                            else:
                                print "-- nh ip : " + route['rt-entry']['nh']["to"]
                                z.append(str(route['rt-entry']['nh']["to"]))
                                print "-- exit Interface : " + route['rt-entry']['nh']["via"]
                                z.append(str(route['rt-entry']['nh']["via"]))
                        else:
                            print "-- nh ip : Discard"
                            z.append("Discard")
                    else:
                        # if the Output is in List formate, the Best next hop is the first element [0]
                        if isinstance((route['rt-entry']['nh']),list):
                            print "-- nh ip : " + route['rt-entry']['nh'][0]["to"]
                            z.append(str(route['rt-entry']['nh'][0]["to"]))
                            print "-- exit Interface : " + route['rt-entry']['nh'][0]["via"]
                            z.append(str(route['rt-entry']['nh'][0]["via"]))
                        else:
                            print "-- nh ip : " + route['rt-entry']['nh']["to"]
                            z.append(str(route['rt-entry']['nh']["to"]))
                            print "-- exit Interface : " + route['rt-entry']['nh']["via"]
                            z.append(str(route['rt-entry']['nh']["via"]))
                elif isinstance((route['rt-entry']),list):
                    print "-- protocol-name : " + route['rt-entry'][0]['protocol-name']
                    z.append(str(route['rt-entry'][0]['protocol-name']))
                    print "-- preference : " + route['rt-entry'][0]['preference']
                    z.append(str(route['rt-entry'][0]['preference']))
                    if route['rt-entry'][0]['protocol-name'] == "Local":
                        if route['rt-entry'][0]["nh-type"] == "Reject":
                            print "-- nh ip : Reject"
                            z.append("Reject")
                        else:
                            print "-- nh-local-interface : " + route['rt-entry'][0]["nh"]["nh-local-interface"]
                            z.append(str(route['rt-entry'][0]["nh"]["nh-local-interface"]))
                    elif route['rt-entry'][0]['protocol-name'] == "Direct":
                        print "-- Direct-interface : " + route['rt-entry'][0]["nh"]["via"]
                        z.append(str(route['rt-entry'][0]["nh"]["via"]))
                    else:
                        if isinstance((route['rt-entry'][0]['nh']),dict):
                            if "nh-table" in route['rt-entry'][0]['nh']:
                                print "-- nh ip : " + route['rt-entry'][0]['nh']["nh-table"]
                                z.append(str(route['rt-entry'][0]['nh']["nh-table"]))
                            else:
                                print "-- nh ip : " + route['rt-entry'][0]['nh']["to"]
                                z.append(str(route['rt-entry'][0]['nh']["to"]))
                                print "-- exit Interface : " + route['rt-entry'][0]['nh']["via"]
                                z.append(str(route['rt-entry'][0]['nh']["via"]))
                        else:
                            print "-- nh ip : " + route['rt-entry'][0]['nh'][0]["to"]
                            z.append(str(route['rt-entry'][0]['nh'][0]["to"]))
                            print "-- exit Interface : " + route['rt-entry'][0]['nh'][0]["via"]
                            z.append(str(route['rt-entry'][0]['nh'][0]["via"]))

            x[str(y)]=z
    backup_file.write(str(vrf["table-name"]+"="+str(x)+"\n"))

backup_file.close()
end_time = datetime.datetime.now().replace(microsecond=0)

print 3*"\n"
print ("<< Total_time " + str(end_time - start_time)+" >>")
print "\n"
print "Routing Table DB extracted to " +script_Path
print "\n"
os.system("pause")
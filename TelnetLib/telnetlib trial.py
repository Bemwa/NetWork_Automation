__author__ = "Bemwa Refaat Aziz"
__EMAIL__ = "engbmwa@gmail.com"

import telnetlib
import time
import datetime
import netaddr
from collections import OrderedDict

# telnet Access Variable
username = 'Bemwa'
password = 'python'
TELNET_PORT = 23
TELNET_TIMEOUT = 5
READ_TIMEOUT = 5
try:
    # Read the Router IPs form a file and save it to List Variable(host_list), each list item contain router name and its IP
    host_list = []
    host_file = open("C:\\Users\\Bemwa\\PycharmProjects\\test1\\hosts.txt","r")
    host_file.seek(0)

    for each_line in host_file.readlines():
        host_list.append(each_line)
    host_file.close()
    print host_list

    # iterate over the host List and split the item to Key(router name) and value(Rtr IP address) then save it to OrderDic
    host_Dic = OrderedDict()
    for element in host_list:
        if element != "\n":
            zyx = element.split("=")
            host_Dic[zyx[0].strip()] = zyx[1].replace("\n", "").strip()
        else:
            continue
    print host_Dic

    # create a unique output file name each time the script run
    date = datetime.datetime.now()
    script_date = str(date.day)+"-"+str(date.month)+"-"+str(date.year)+"@"+str(date.hour)+"%"+str(date.minute)+"%"+str(date.second)
    script_Path = "C:\\Users\\Bemwa\\PycharmProjects\\test1\\Output-"+script_date+".txt"
    output_file = open(script_Path , "a")


    # iterate over the OrderedDic then use the Key to write the heading in the output file
    # change the value to IP address opbject for ip validation
    # use telnetlib to access the Hosts and apply the required commands
    # save the all output to uniqie file name to avoid duplication

    for k,v in host_Dic.items():
        print ("Access Network Box : " + k)
        output_file.write("Access Network Box : " + k+"\n")
        output_file.write("="*(len("Access Network Box : ")+len(k)))
        ip = str(netaddr.IPAddress(v))
        connection = telnetlib.Telnet(ip, TELNET_PORT, TELNET_TIMEOUT)
        connection.read_until("name:", READ_TIMEOUT)
        connection.write(username + "\n")
        connection.read_until("word:", READ_TIMEOUT)
        connection.write(password + "\n")
        time.sleep(1)
        connection.write("terminal length 0\n")
        connection.read_until("#",timeout=50)
        connection.write("sh ip int br"+"\n")
        time.sleep(1)
        y = connection.read_very_eager().replace("terminal length 0","")
        output_file.write(y+"\n")
        output_file.write(90*"-"+"\n")
        output_file.write(90*"/"+"\n")
        output_file.write(90*"-"+"\n")
        connection.close()

    output_file.close()
except IOError:
    print "Invalid Host file name or directory "

except netaddr.core.AddrFormatError:
    print "Invalid IP address format"

except Exception as e:
	print e 

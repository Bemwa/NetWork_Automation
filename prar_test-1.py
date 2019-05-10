import paramiko
import time
import datetime
import netaddr
from collections import OrderedDict

# telnet Access Variable
username = 'bemwa'
password = 'cisco'

try:
    # Read the Router IPs form a file and save it to List Variable(host_list), each list item contain router name and its IP
    host_list = []
    host_file = open("C:\\Users\\Bemwa\\PycharmProjects\\Para-test\\hosts.txt","r")
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
    script_Path = "C:\\Users\\Bemwa\\PycharmProjects\\Para-test\\Output-"+script_date+".txt"
    output_file = open(script_Path , "a")


    # iterate over the OrderedDic then use the Key to write the heading in the output file
    # change the value to IP address opbject for ip validation
    # use paramiko to access the Hosts and apply the required commands
    # save the all output to unique file name to avoid duplication

    for k,v in host_Dic.items():
        print ("Access Network Box : " + k)
        output_file.write("Access Network Box : " + k+"\n")
        output_file.write("="*(len("Access Network Box : ")+len(k)))
        ip = str(netaddr.IPAddress(v))
        Channel = paramiko.SSHClient()

        # set_missing_host_key_policy : define the policy to be used that the SSHClient should use when the hostname is not in
        # either the system host keys or the application keys
        # AutoAddPolicy :: Policy for automatically adding the hostname and new host key to the local HostKeys object, and saving it

        Channel.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        Channel.connect(hostname=v, username=username, password=password, look_for_keys=False, allow_agent=False)

        shell = Channel.invoke_shell()  # This will set interactive shell
        shell.send("enable\n")
        shell.send("python\n")
        shell.send("terminal length 0\n")
        shell.send("show ip int b\n")
        shell.send("show arp \n")
        time.sleep(3)
        # recv int size: how many chars should be read
        y = str(shell.recv(50000)).replace("terminal length 0","").replace("R1>enable","").replace("Password:","")
        Channel.close()
        output_file.write(y+"\n")
        output_file.write(90*"-"+"\n")
        output_file.write(90*"/"+"\n")
        output_file.write(90*"-"+"\n")

    output_file.close()

    x = raw_input("press Enter to exit")
    while x != "":
        exit()

except IOError:
    print "Invalid Host file name or directory "

except netaddr.core.AddrFormatError:
    print "Invalid IP address format"
__author__ = "Bemwa Refaat Aziz"
__EMAIL__ = "engbmwa@gmail.com"

import filecmp,os ,ast,datetime

# This Script aimed to compare the Contents of two copies of the Routing table and extract the below differences :
# 1- Any Missing Routes
# 2- Any New Routs
# 3- Routes that have changes in the Nexthop details like 'exit interface' , 'Routing Protocol' , 'Nexthop IP'

Otxt = raw_input("Please enter the full name(fname.txt) of the first Backup file, located in C:\python_Scripts\RTG_Compare : ")
Ntxt = raw_input("Please enter the full name(fname.txt) of the second Backup file, located in C:\python_Scripts\RTG_Compare : ")

start_time = datetime.datetime.now().replace(microsecond=0)

Oldfile = "C:\\python_Scripts\\RTG_Compare\\"+Otxt
Newfile = "C:\\python_Scripts\\RTG_Compare\\"+Ntxt

# Compare that exact txt files without digging into the Route details
if filecmp.cmp(Oldfile,Newfile) == True:
    print "No changes found"
else:
    print "Changes found , let's check ... "
    file1 = open(Oldfile,"r")
    file2 = open(Newfile,"r")

    for line in file1.read().splitlines():
        VRF_name = line.split("=")[0]
        VRF_Content = line.split("=")[1]
        file2.seek(0)
        print "\n"
        for entry in file2.read().splitlines():
            if VRF_name == entry.split("=")[0]:
                print "Checking Routing Instance : "+ VRF_name
                # compare the entire VRF
                if VRF_Content == entry.split("=")[1]:
                    print "No Changes found"
                    continue
                # Content of two VRF don't match
                else:
                    # remove the SortedDict "( )"
                    x = VRF_Content.split("(")[1].replace(")","")
                    y = entry.split("=")[1].split("(")[1].replace(")","")
                    # convert to DIC
                    xx = ast.literal_eval(x)
                    yy = ast.literal_eval(y)
                    for k, v in xx.items():
                        if k in yy:
                            if v == yy[k]:
                                # delete the key vlaue pair for the next fast searching, also the remaining will be
                                # considered as new Routes
                                del xx[k]
                                del yy[k]
                            else:
                                print "<<<<<<<<< changes In the Nexthop Details found for Route: "+k + "  >>>>>>>>>>>>>"
                                print "- Old Next Hop Value: "+ str(v)
                                print "+ New Next Hop Value: "+ str(yy[k])
                                print "\n"
                                del xx[k]
                                del yy[k]
                        else:
                            print "<<<<<<<<< Route : " + k + " not found >>>>>>>>>"
                            del xx[k]
                    if bool(yy)==True:
                        print "<<<<<<<<< New Routes Found >>>>>>>>>>>>>"
                        print str(yy.keys()).replace("[","").replace("]","   ")
            else:
                continue

end_time = datetime.datetime.now().replace(microsecond=0)

print 3*"\n"
print ("<< Total_time " + str(end_time - start_time)+" >>")
print "\n"


os.system("pause")

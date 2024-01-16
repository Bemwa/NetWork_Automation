__author__ = "Bemwa Refaat Aziz"
__EMAIL__ = "engbmwa@gmail.com"

import xml.etree.ElementTree as ET

def extract_namespace(file_path):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.strip().startswith("<route-information"):
                    namespace = line.split('"')[1]
                    return namespace
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def parse_routing_info(file_path):
    try:
        # Extracting namespace
        namespace = extract_namespace(file_path)
        if namespace:
            ns = {'ns0': namespace}
            routing_info = {}
            tree = ET.parse(file_path)
            root = tree.getroot()

            for route_table in root.findall('.//ns0:route-table', namespaces=ns):
                table_name = route_table.find('ns0:table-name', namespaces=ns).text
                route_entries = {}

                for rt_entry in route_table.findall('.//ns0:rt', namespaces=ns):
                    rt_dest = rt_entry.find('ns0:rt-destination', namespaces=ns).text

                    entry_details = {}
                    entry_details['protocol'] = rt_entry.find('ns0:rt-entry/ns0:protocol-name', namespaces=ns).text if rt_entry.find('ns0:rt-entry/ns0:protocol-name', namespaces=ns) is not None else None
                    entry_details['metric'] = rt_entry.find('ns0:rt-entry/ns0:metric', namespaces=ns).text if rt_entry.find('ns0:rt-entry/ns0:metric', namespaces=ns) is not None else None

                    nh_list = []
                    for nh in rt_entry.findall('ns0:rt-entry/ns0:nh', namespaces=ns):
                        nh_details = nh.find('ns0:to', namespaces=ns).text if nh.find('ns0:to', namespaces=ns) is not None else None
                        nh_list.append(nh_details)

                    entry_details['nh'] = nh_list
                    route_entries[rt_dest] = entry_details

                routing_info[table_name] = route_entries

            return routing_info
        else:
            print("Namespace not found in the route-information tag.")
            return None

    except ET.ParseError as e:
        print(f"XML Parsing Error: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

# Function to compare routing information from two dictionaries
def compare_routing_info(routing_info1, routing_info2):
    # Compare routing information from routing_info1 to routing_info2
    for table_name, entries in routing_info1.items():
        if table_name in routing_info2:
            print(f"Comparing entries in Route Table: {table_name}")
            print("==================================================")
            print()
            for rt_dest, details in entries.items():
                if rt_dest in routing_info2[table_name]:
                    #print (rt_dest)
                    if details != routing_info2[table_name][rt_dest]:
                        print(f"Differences detected in {rt_dest} from routing_info1 to routing_info2:")
                        print(f"Protocol Name: {details.get('protocol')} -> {routing_info2[table_name][rt_dest].get('protocol')}")
                        print(f"Metric: {details.get('metric')} -> {routing_info2[table_name][rt_dest].get('metric')}")
                        print(f"Next-Hop: {details.get('nh')} -> {routing_info2[table_name][rt_dest].get('nh')}")
                        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                        print()
                else:
                    print(f"{rt_dest} exists in routing_info1 but is missing in routing_info2 (from routing_info1 to routing_info2)")
                    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    print()

    # Compare routing information from routing_info2 to routing_info1
    for table_name, entries in routing_info2.items():
        if table_name in routing_info1:
            for rt_dest, details in entries.items():
                if rt_dest not in routing_info1[table_name]:
                    print(f"{rt_dest} exists in {table_name} table of routing_info2 but is missing in routing_info1 (from routing_info2 to routing_info1)")
                    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    print()
        else:
            for rt_dest, details in entries.items():
                print(f"{rt_dest} exists in {table_name} table of routing_info2 but is missing in routing_info1 (from routing_info2 to routing_info1)")
                print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                print()

# Paths to the text files containing routing information from Juniper devices
file1_path = '/Users/bemwabeshay/scripts/Collect_cmds/routing_info_device1.xml'
file2_path = '/Users/bemwabeshay/scripts/Collect_cmds/routing_info_device2.xml'

try:
    routing_info1 = parse_routing_info(file1_path)
    routing_info2 = parse_routing_info(file2_path)

    if routing_info1 and routing_info2:
        compare_routing_info(routing_info1, routing_info2)
    else:
        print("Parsing failed for one or both files.")

except Exception as e:
    print(f"An error occurred: {e}")

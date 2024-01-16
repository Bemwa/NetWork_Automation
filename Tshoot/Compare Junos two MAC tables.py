__author__ = "Bemwa Refaat Aziz"
__EMAIL__ = "engbmwa@gmail.com"

import xml.etree.ElementTree as ET

def extract_mac_details(file_name):
    try:
        with open(file_name, 'r') as file:
            xml_content = file.read()
            root = ET.fromstring(xml_content)
            mac_details = {}
            for mac_entry in root.findall('.//l2ng-mac-entry'):
                mac_address = mac_entry.find('./l2ng-l2-mac-address').text
                vlan_name = mac_entry.find('./l2ng-l2-mac-vlan-name').text
                logical_interface = mac_entry.find('./l2ng-l2-mac-logical-interface').text
                active_source_elem = mac_entry.find('./l2ng-l2-active-source')
                active_source = active_source_elem.text if active_source_elem is not None else 'N/A'
                mac_details[mac_address] = {
                    'VLAN Name': vlan_name,
                    'Logical Interface': logical_interface,
                    'Active Source': active_source
                }
            return mac_details
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
        return {}

def compare_mac_addresses(file1, file2):
    mac_details_file1 = extract_mac_details(file1)
    mac_details_file2 = extract_mac_details(file2)

    unique_to_file1 = {mac: mac_details_file1[mac] for mac in mac_details_file1 if mac not in mac_details_file2}
    unique_to_file2 = {mac: mac_details_file2[mac] for mac in mac_details_file2 if mac not in mac_details_file1}

    return unique_to_file1, unique_to_file2

file1_name = "/Users/bemwabeshay/scripts/Collect_cmds/Ethernet_switching_table01.txt"
file2_name = "/Users/bemwabeshay/scripts/Collect_cmds/Ethernet_switching_table02.txt"

unique_file1, unique_file2 = compare_mac_addresses(file1_name, file2_name)

print(f"MAC addresses in '{file1_name}' but not in '{file2_name}':")
for mac in unique_file1:
    print(f"MAC Address: {mac}")
    print(f"VLAN Name: {unique_file1[mac]['VLAN Name']}")
    print(f"Logical Interface: {unique_file1[mac]['Logical Interface']}")
    print(f"Active Source: {unique_file1[mac]['Active Source']}")
    print()

print(f"\nMAC addresses in '{file2_name}' but not in '{file1_name}':")
for mac in unique_file2:
    print(f"MAC Address: {mac}")
    print(f"VLAN Name: {unique_file2[mac]['VLAN Name']}")
    print(f"Logical Interface: {unique_file2[mac]['Logical Interface']}")
    print(f"Active Source: {unique_file2[mac]['Active Source']}")
    print()

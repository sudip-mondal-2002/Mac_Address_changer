#! usr/bin/env python3

import optparse as opt

import re

import subprocess as sp


def get_arguments():
    parser = opt.OptionParser()

    parser.add_option("-i", "--interface", dest="interface", help="Interface to change Mac address")

    parser.add_option("-m", "--mac", dest="mac", help="New Mac address")

    (options, arguments) = parser.parse_args()

    if not options.interface:

        parser.error("[-] please enter an interface")

    elif not options.mac:

        parser.error("[-] please enter an mac")

    else:

        return options


def get_current_mac(interface):
    ifconfig_result = sp.check_output(["ifconfig", interface])

    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

    if mac_address_search_result:

        return (mac_address_search_result.group(0))

    else:

        print(" [-] No MAC address")


def change_mac(interface, new_mac):
    print("[+] changing mac adress for " + interface + " to " + new_mac)

    sp.call(["ifconfig", interface, "down"])

    sp.call(["ifconfig", interface, "hw", "ether", new_mac])

    sp.call(["ifconfig", interface, "up"])


options = get_arguments()

current_mac = get_current_mac(options.interface)

print("Current MAC = " + str(current_mac))

change_mac(options.interface, options.mac)

current_mac = get_current_mac(options.interface)

if current_mac == options.mac:

    print("[+] MAC address changed to" + str(current_mac))

else:

    print("[-] MAC address did not change")

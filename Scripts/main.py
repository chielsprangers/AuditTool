import ptvsd
ptvsd.enable_attach()
import scancode
import sys
import os
import click
import json


import nmapscan, msf
#import dirb, whatweb, zaproxy, bruteforce

click.disable_unicode_literals_warning = True

@click.group()
def main():
    pass

@main.command()
@click.option('-h', '--hosts')
def netscan(hosts):
    cleanedIPs = []
    scandata = {}
    ipArray = hosts.split(';')
    
    for ip in ipArray:
        cleanedIPs.append(ip)
        scandata[ip] = scancode.network(ip)

    #Change data to JSON
    JSONResult = json.dumps(scandata)

    print(JSONResult)
    

@main.command()
@click.option('-h', '--hosts')
def webscan(hosts):
    scandata = {}
    
    scandata = scancode.webapp(hosts)

    #Change data to JSON
    JSONResult = json.dumps(scandata)

    print(JSONResult)

if __name__ == "__main__":
    main()
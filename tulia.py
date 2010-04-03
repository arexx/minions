#!/usr/bin/env python2.6
import sys
import threading
import commands

from minion.minion import Minion
from minion import require 

def free_space():
    out = commands.getoutput('df -h').split('\n')
    main = "UNKNOWN"
    storage = "UNKNOWN"
    for line in out:
        if line.startswith("/dev/sda1"):
            main = line.split()[3]
        elif line.startswith("/dev/sdb1"):
            storage = line.split()[3]
    return "%s free on root, %s free on /storage" % (main, storage,)
    
def main():
    tulia = Minion("tulia",
        description="""Tulia is an avatar for Alex's flat server.""")
        
    tulia.register("FREE SPACE", free_space, requires=require.name)
    
    tulia.start()
    tulia.wait()
    
if __name__ == '__main__':
    main()
#!/usr/bin/env python2.6
from minion.minion import Minion
from threading import Thread
import logging,os,errno,sys

class StdInWriter(Thread):
    def __init__(self, minion):
        Thread.__init__(self)
        self.minion = minion
        self.alive = False
        
    def run(self):
        self.alive = True
        while self.alive:
            line = sys.stdin.readline()
            self.minion.write(line)

def drop_permissions():
    logging.debug("Dropping permissions")
    try:
        import pwd
    except ImportError:
        logging.critical('Cannot import module "pwd"')
        sys.exit(1)
    nobody = pwd.getpwnam('nobody')[2]
    try:
        os.setuid(nobody)
    except OSError, e:
        if e.errno != errno.EPERM: raise
        logging.warn('Cannot setuid "nobody"')
        #sys.exit(1)

drop_permissions()

ramirez = Minion("ramirez")
ramirez.start()

writer = StdInWriter(ramirez)
writer.start()

ramirez.wait()

#!/usr/bin/env python2.6
import sys
import threading

from minion.minion import Minion
from minion.util import drop_permissions

class StdInWriter(threading.Thread):
    def __init__(self, minion):
        threading.Thread.__init__(self)
        self.minion = minion
        self.alive = False
        
    def run(self):
        self.alive = True
        while self.alive:
            line = sys.stdin.readline()
            self.minion.write(line)

drop_permissions()

ramirez = Minion("ramirez")
ramirez.start()

writer = StdInWriter(ramirez)
writer.start()

ramirez.wait()

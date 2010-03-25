#!/usr/bin/env python2.6
from minion.minion import Minion
from sys import stdin
from threading import Thread

class StdInWriter(Thread):
    def __init__(self, minion):
        Thread.__init__(self)
        self.minion = minion
        self.alive = False
        
    def run(self):
        self.alive = True
        while self.alive:
            line = stdin.readline()
            self.minion.write(line)

ramirez = Minion("ramirez")
ramirez.start()

writer = StdInWriter(ramirez)
writer.start()

ramirez.wait()
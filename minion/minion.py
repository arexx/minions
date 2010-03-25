from oyoyo.client import IRCClient, IRCApp
from oyoyo.cmdhandler import DefaultCommandHandler
from oyoyo import helpers
from threading import Thread

import logging
class PrintHandler(logging.Handler):
    def emit(self, record):
        print record
logging.getLogger("oyoyo.client").addHandler(PrintHandler())
logging.getLogger("oyoyo.cmdhandler").addHandler(PrintHandler())

class MyHandler(DefaultCommandHandler):
    def __init__(self, cli, callback, room):
        self.client = cli
        self.callback = callback
        self.room = room
    
    def privmsg(self, src, room, msg):
        print "%s in %s said: %s" % (src, room, msg,)
        
        if msg == "RAMIREZ GO AWAY":
            helpers.quit(self.client)
        
        self.callback(msg)
        
    def endofmotd(self, server, user, msg):
        helpers.join(self.client, self.room)

class Minion(Thread):
    def __init__(self, nick, room="#minions"):
        Thread.__init__(self)

        def connect_callback(cli):
            print "Connected."
            #helpers.join(cli, "#inforum")

        self.app = IRCApp()
        self.cli = IRCClient(
            host="irc.imaginarynet.org.uk",
            port=6667,
            nick=nick,
            connect_cb=connect_callback,
            )
        self.cli.command_handler = MyHandler(self.cli, self.msg_handler, room)
        self.app.addClient(self.cli)
        
    
    def run(self):
        thread = Thread()
        self.app.run()
        print "Minion started."
        
    def wait(self):
        self.join()
        
    def write(self, msg):
        helpers.msg(self.cli, "#minions", msg)

    def msg_handler(self, msg):
        """Called when the bot recieves a message."""
        print "Minion recieved: %s" % msg


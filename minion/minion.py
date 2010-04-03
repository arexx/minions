from threading import Thread
import string
import logging

from oyoyo.client import IRCClient, IRCApp
from oyoyo.cmdhandler import DefaultCommandHandler
from oyoyo import helpers

import require

class PrintHandler(logging.Handler):
    def emit(self, record):
        print record
logging.getLogger("oyoyo.client").addHandler(PrintHandler())
logging.getLogger("oyoyo.cmdhandler").addHandler(PrintHandler())


uppercase_a_to_z = [chr(x) for x in range(ord('A'), ord('Z')+1)]
lowercase_a_to_z = [chr(x) for x in range(ord('a'), ord('z')+1)]
from_list = lowercase_a_to_z + uppercase_a_to_z + [' ', '\t', '\n']
to_list   = uppercase_a_to_z + uppercase_a_to_z + [' ', ' ', ' ']
translation_dict = dict(zip(from_list, to_list))

def simplify(inp):
    """Simplifies a punctuation-filled sentence to assist recognition.
     - Removes all non-alphanumeric, non-whitespace characters
     - Condenses all whitespace to single spaces
     - Upper-cases everything
     - Trims whitespace
     
     In [2]: simplify("Hello, ramirez! How are you   doing? ")
     Out[2]: 'HELLO RAMIREZ HOW ARE YOU DOING'
    """
    buf = ""
    for char in inp:
        if char in translation_dict:
            buf += translation_dict[char]
    return " ".join(buf.split()) 

class MyHandler(DefaultCommandHandler):
    def __init__(self, minion, callback, room):
        self.client = minion.client
        self.minion = minion
        self.callback = callback
        self.room = room
    
    def privmsg(self, src, room, msg):
        print "%s in %s said: %s" % (src, room, msg,)
        self.callback(msg)
        
    def endofmotd(self, server, user, msg):
        helpers.join(self.client, self.room)

class Minion(Thread):
    def __init__(self, nick, room="#minions", description="This minion does not have a description."):
        Thread.__init__(self)
        self.nick = nick
        self.description = description
        self.room = room
        self.matches = []
        
        def connect_callback(cli):
            print "Connected."
            #helpers.join(cli, "#inforum")

        self.app = IRCApp()
        self.client = IRCClient(
            host="irc.imaginarynet.org.uk",
            port=6667,
            nick=nick,
            connect_cb=connect_callback,
            )
        self.client.command_handler = MyHandler(self, self.msg_handler, self.room)
        self.app.addClient(self.client)
        
        # Default minion commands 
        self.register("GO AWAY", lambda: helpers.quit(self.client), require.name)
        self.register("WHO ARE YOU", lambda: self.description, require.name)
    
    def run(self):
        thread = Thread()
        self.app.run()
        print "Minion started."
        
    def wait(self):
        self.join()
        
    def write(self, msg):
        helpers.msg(self.client, self.room, msg)

    def msg_handler(self, msg):
        """Called when the bot recieves a message."""
        print "Minion recieved: %s" % msg
        simplemsg = simplify(msg)
        
        # Check to see if any of the registered matches match this message.
        for (match, callback, requires) in self.matches:
            if simplemsg.find(match) > -1:
                
                # Test if all of the requires for the match succeed.
                if min([require(self, simplemsg) for require in requires]):
                    
                    print "Calling callback for %s" % match
                    # Call the callback, if it returns a string, send it to the client.
                    result = callback()
                    if isinstance(result, str):
                        self.write(result)
                    else:
                        print "Callback didn't return a string."
                    
    def register(self, match, callback, requires):
        """Registers a string to be matched against all received messages, with a callback to execute if the string matches, and a list of requirements that must be fulfilled before the callback is called."""
        if not isinstance(requires, list):
            requires = [requires]
        self.matches += [(match, callback, requires)]
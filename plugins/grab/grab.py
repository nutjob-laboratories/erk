from erk import *
import random

'''
grab.py

This plugin will grab a nickname that is currently in use.
It will try to change the client's nickname every 5-20 seconds until
the client has attained the desired nickname.

'''

class NicknameGrabber(Plugin):

    def __init__(self):
        self.name = "Nickname Grabber"
        self.description = "Grabs a nickname"
        
        self.author = None
        self.version = None
        self.website = None
        self.source = None
        
        self.active = False
        self.next = 0
        self.target = None

    def input(self,client,name,text):
        
        tokens = text.split()
        
        if len(tokens)==2:
            if tokens[0].lower()=="/grab":
                self.target = tokens[1]
                self.active = True
                return True
        
        if len(tokens)>1 and tokens[0].lower()=="/grab":
            self.print("Usage: /grab NICKNAME")
            return True

    def tick(self,client):
        if self.target==None: return
        if self.active:
            if client.nickname==self.target:
                self.active = False
                self.target = None
            else:
                if self.uptime()>=self.next:
                    client.setNick(self.target)
                    self.next = self.uptime() + random.randint(5,20)

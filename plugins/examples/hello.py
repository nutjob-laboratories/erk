from erk import *

class HelloWorld(Plugin):
    def __init__(self):
        self.name = "Hello World plugin"
        self.author = "Dan Hetrick"
        self.version = "1.0"
        self.website = "https://github.com/nutjob-laboratories/erk"
        self.source = "https://github.com/nutjob-laboratories/erk"
        self.description = "Example plugin for documentation"

    def input(self,client,name,text):

        # Look for our new command
        if text=="/hello":

            # Found it! Display our message
            self.print("Hello, world!")

            # Now, we return "True" to make sure that
            # "/hello" isn't sent to the IRC server as
            # a chat messages
            return True
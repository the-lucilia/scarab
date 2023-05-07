from threading import *
from queue import Queue
from RegionClass import Region
import datetime
import nationstates

# Supply a command queue and a response queue
class brainstem(Thread): #Inherit multithreading
    def __init__(self,mainNation,commands,responses):
        Thread.__init__(self)

        # Thread upkeep and maintenance
        assert mainNation is not None,"Main nation not supplied" # Throw a fit if an operator nation has not been supplied
        self.mainNation = mainNation
        self.commands = commands #Inbound commands from frontend
        self.responses = responses #Outbound responses to frontend
        self.state = None # Current state - e.g. tracking a target for updating
        self.command = None # Currently handled command, or None/idle if none

        # Update status
        self.regions = [] # This should be passed to us on bot start, but we can refresh it as needed
        self.regionsAge = datetime.datetime.now().timestamp() # Timestamp of the last time the regionlist was refreshed
        self.position = 0 # Last known position of update within the list

        # Targetting info
        self.endos = 0 # Endorsements available
        self.tracked = None # Currently tracked trigger (REGION CLASS)
        self.target = None # Currently selected target (REGION CLASS)
        self.point = None # Designated point

        self.start()

    def detectUpdate(self):
        if self.regions:
            firstUpd = nationstates.get_update(regions[0])
            lastUpd = nationstates.get_update(regions[1])

            if int(lastUpd) < int(firstUpd): #If firstUpd is larger than lastUpd, update has hit First update but not Last update - only ever happens during update
                return True
            else:
                return False


    def boot(self):
        pass

    def idle(self):
        pass 

    def run(self):
        while True:
            if self.commands.empty():
                if self.state == None or self.state == "idle":
                    self.idle() # Wait for news, in the meantime, tend to our local database
                elif self.state == "boot":
                    self.boot()

            else: #Override comes in from high command
                command = self.commands.get()
                if command == "quit":
                    self.responses.put("done")
                    self.commands.task_done() #Signal task completed
                    break # Exit loop forevermore
                
                # TODO:
                # - Fetch me a target
                # - 

                self.commands.task_done() #Signal task completed


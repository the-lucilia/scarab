from threading import *
from queue import Queue
from RegionClass import Region
from RegionBlock import RegionBlock
import nationstates
import datetime
import time

class codes:
    # Control loop->Brainstem (commands) are always even
    # Brainstem->CL (responses) are always odd
    # Commands are shipped as a tuple, with element 0 holding the code and subsequent elements (if any) holding parameters
    # They are also grouped into commands and responses for clarity

    class commands:
        EXIT = 0 # Request the brainstem to gracefully shut down. No arguments
        BEGINTAG = 2 # Initiate a tag raid.
        ENDTAG = 4 # Terminate the tag raid.
        GETTARG = 6 # Get a target. 1 arg: endorsements
        SKIPTARG = 8 # Skip the target, if any.
        OVERRIDETARG = 10 # Override the target with a custom target. 1 arg: target
        FETCHTRIGGER = 12 # Request a trigger for a target. 2 args: First, time delay. Second, target, or None. If none, default to last supplied target. 

        # These three are all different ways to watch a trigger - immediately, after a dynamic delay, or after a fixed delay. This allows flexibility in the triggering logic.
        RAWWATCHTRIGGER = 14 # Watch the specified trigger, or last supplied trigger if none. Expects: 3 on trigger update. 
        WATCHTRIGGER = 16 # Same as RAWWATCHTRIGGER, but attempt to adapt GO time to update speed. (EXPERIMENTAL AT BEST)
        TIMEDTRIGGER = 18 # Same as WATCHTRIGGER, but accepts a single parameter of time to delay, which is not to be modified. (e.g. Wait 2s after trigger region)

        UNTRACK = 20 # Stop tracking a target for hit status
        POINT = 22 # Inform the brainstem of an attempt at point
        PING = 24 # Request a heartbeat. One arg: time recieved
        QUERY = 26 # Perform an arbitrary query - in case we need to expand functionality

        REFRESHREGIONS = 28 # Refresh the regions list

        NEWUPDATER = 30
        GONEUPDATER = 32
        ADDROLLCALL = 34 # Add someone to roll call
        ROLLCALL = 36 # Get roll call
        INCUPD = 38 # Increment updaters by one, for some reason
        DECUPD = 40 # Dec "

        VERIFY = 42 # Send a code and nation name to the backbrain to verify

        INITUPDATERS = 44 # Send a static # of updaters, particularly at boot-time
        MANUALGO = 46 # For testing

    class responses:
        ABORT = 1 # Inform the parent process there has been a fatal error. 1 argument: None, or string containing error information
        GO = 3 # Inform the parent process the trigger conditions have been met. Parent process should send a GO signal.
        SKIPTARG = 5 # Inform the parent process the target should be skipped, usually due to unforeseen timing issues (e.g. target has updated before TIMEDTRIGGER delay)
        HOLD = 7 # Inform the parent process the target has delayed in updating longer than expected
        EXHAUSTED = 9 # Inform the parent process a target cannot be found within the allowed parameters. 1 arg: error string
        TARGET = 11 # Provide the parent process with a target to aim for
        HIT = 13 # Inform the parent process the registered point has been identified as delegate
        MISS = 15 # Inform the parent process the registered point has NOT been identified as delegate, despite updating
        ACKNOWLEDGE = 17 # Blanket acknowledgement without further data
        PONG = 19 # Respond to a heartbeat request
        ANSWER = 21 # Respond to an arbitrary query
        STATUS = 23 # Inform the bot of a status effect that may impact operations, or otherwise a message that should be passed along to the humans in the discord
        SETPOINT = 25 # Inform the discord of a decision on who is point
        UPDATERS = 27 # Inform the CC how many updaters we have. Endos is this -1
        ROLLCALLED = 29 # Inform the CC of what our roll call is
        VERIFICATION = 31 # Inform whether or not a verification for the nation named succeeded

# I may or may not have stolen this name from the Scythe triology. Fight me. 
# Supply a command queue and a response queue
class BackBrain(Thread): #Inherit multithreading
    class states:
        IDLE = 0 # Default state - nothing happening
        BOOT = 1 # Initial state - start boot

    def __init__(self,headers,commands,responses,regionBlock=None,fetchRegions=False):
        Thread.__init__(self)

        # Thread upkeep and maintenance
        assert headers is not None,"Error: Headers not supplied" #Require headers to exist
        self.headers = headers #HTTP headers
#        print(self.headers)
        self.commands = commands #Inbound commands from frontend 
        self.responses = responses #Outbound responses to frontend

        self.state = None # Current state - e.g. tracking a target for updating
        self.command = None # Currently handled command, or None/idle if none

        # Update status
#        if fetchRegions:
#            nationstates.downloadRegions()
#        if not regionBlock:
#            self.regionBlock = RegionBlock() # This should be passed to us on bot start, but we can refresh it as needed
#        else:
#            self.regionBlock = regionBlock # Accept custom regionlist
        self.regionBlock = regionBlock

        self.regionsAge = datetime.datetime.now().timestamp() # Timestamp of the last time the regionlist was refreshed
        self.position = 0 # Last known position of update within the list

        # Targeting info
        self.updaters = 0 # Updaters available. Endos is this number -1 (we need a point)
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
#        self.responses.put((codes.responses.STATUS,"Backbrain up and running"))

        while True:
            if self.commands.empty():
                if self.state == None or self.state == "idle":
                    self.idle() # Wait for news, in the meantime, tend to our local database
                elif self.state == "boot":
                    self.boot()

            else: #Override comes in from high command
                command = self.commands.get()
                if command[0] == codes.commands.EXIT: #(0,) 
                    self.responses.put((codes.responses.ACKNOWLEDGE,)) # Shutdown in progress
                    self.responses.put((codes.responses.STATUS,"Shutting down")) # Inform users of system shutdown
                    self.commands.task_done() #Signal task completed
                    break # Exit loop forevermore

                elif command[0] == codes.commands.PING:
                    self.responses.put((codes.responses.PONG,command[1])) #Send the gotten time right back to it
                
                elif command[0] == codes.commands.NEWUPDATER:
                    self.updaters += 1
                    self.responses.put((codes.responses.UPDATERS,self.updaters)) # How many do we have?

                elif command[0] == codes.commands.GONEUPDATER:
                    self.updaters -= 1
                    if self.updaters < 0:
                        self.updaters = 0
                    self.responses.put((codes.responses.UPDATERS,self.updaters)) # How many do we have?

                elif command[0] == codes.commands.VERIFY:
                    if nationstates.verify_nation(command[2],command[3],headers=self.headers):
                        self.responses.put((codes.responses.VERIFICATION,command[1], command[2], True))
                    else:
                        self.responses.put((codes.responses.VERIFICATION,command[1], command[2], False))

                elif command[0] == codes.commands.INITUPDATERS:
                    self.updaters = command[1]
                    if self.updaters > 0:
                        self.responses.put((codes.responses.UPDATERS, self.updaters))

                elif command[0] == codes.commands.MANUALGO:
                    self.responses.put((codes.responses.GO,))

                # TODO: Impliment each and every command code, one by one. 
                # This will be painful.

                self.commands.task_done() #Signal task completed


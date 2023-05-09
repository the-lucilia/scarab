import aiohttp
import discord
from discord.ext import tasks, commands
from queue import Queue
from backbrain import BackBrain, codes

async def MakeEmbed(title:str, prompt: str):
    embed = discord.Embed(
        title=title,
        description=prompt,
        color=0x8ee6dd,
    )

    return embed

class CorpusCallosum(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.headers = {
            "User-Agent": "SCARAB/0.1, devved by nation=hesskin_empire and nation=Volstrostia"
        }

        self.commands = Queue()
        self.responses = Queue()

        self.channel = await bot.fetch_channel(1039736266893299843)  #TODO: Rework this! Hardcoding channels is for looooosers

        self.backbrain = BackBrain(self.headers, self.commands, self.responses) # Backbrain autostarts on invokation
        self.brainstem.start()

    def cog_unload(self):
        self.commands.put((codes.commands.EXIT,)) # Task the backbrain to shut down
        self.brainstem.cancel() # Terminate brainstem loop
        
    @tasks.loop(seconds=0.05) # No idea if it will accept values < 1, but 1 second is too much variability for our needs. 
    async def brainstem(self): #So named because it's the bridge between the brain and the rest of the world
        while not self.responses.empty:
            task = self.responses.get()
            
            if task[0] == codes.responses.PONG: #Handle pong response
                self.channel.send("PONG")

            self.responses.task_done()

    @commands.command()
    async def ping(self):
        self.commands.put((codes.commands.PING,))

async def setup(bot):
    await bot.add_cog(CorpusCallosum(bot))

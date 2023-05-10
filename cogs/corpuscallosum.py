#import aiohttp
import discord
from discord.ext import tasks, commands
from queue import Queue
from backbrain import BackBrain, codes
import datetime

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
        
        print("Starting Backbrain")
    
        self.backbrain = BackBrain(self.headers, self.commands, self.responses) # Backbrain autostarts on invokation
        self.brainstem.start()

#    @commands.Cog.listener()
    async def cog_unload(self):
        print("Unloading Corpus Callosum")
        await self.flatline()

#    @commands.Cog.listener() # event
    async def cog_load(self):
        self.channel = await self.bot.fetch_channel(1039736266893299843)  #TODO: Rework this! Hardcoding channels is for looooosers
        await self.channel.send(embed = await MakeEmbed("Backbrain is Online","Awaiting tagging commands"))

    async def flatline(self):
        print("Shutting down backbrain")
        self.commands.put((codes.commands.EXIT,)) # Task the backbrain to shut down
        #self.brainstem.cancel() # Terminate brainstem loop
        
    @tasks.loop(seconds=0.05) # No idea if it will accept values < 1, but 1 second is too much variability for our needs. 
    async def brainstem(self): #So named because it's the bridge between the brain and the rest of the world
#        print("We meet again")
        if not self.responses.empty():
            task = self.responses.get()
            if task[0] == codes.responses.PONG: #Handle pong response
                difference = datetime.datetime.now(tz=datetime.timezone.utc) - task[1] # Sent reply at
                await self.channel.send(embed=await MakeEmbed("PONG",f"Round-trip time: {difference.microseconds / 1000}ms"))

            elif task[0] == codes.responses.UPDATERS:
                await self.channel.send(embed=await MakeEmbed("UPDATERS",f"Updater count: {task[1]}"))

            self.responses.task_done()

    @commands.command()
    async def ping(self,ctx):
#        print(f"Registered a ping at {time.time()}")
        self.commands.put( (codes.commands.PING,ctx.message.created_at) ) # Sent at



    # MOVED FROM STAGING - we need to track endo
    @commands.command(aliases=["present"])
    async def here(self, ctx):
        user = ctx.message.author
        present = discord.utils.get(ctx.guild.roles, name="present")
        if present not in user.roles:
            await user.add_roles(present)
#            await ctx.send(embed=await MakeEmbed("ROLED",f"Roled: {ctx.message.author}"))
            self.commands.put((codes.commands.NEWUPDATER, ctx.message.author)) # Send a new updater along
        else:
            await user.remove_roles(present)
#            await ctx.send(embed=await MakeEmbed("UNROLED",f"Unroled: {ctx.message.author}"))
            self.commands.put((codes.commands.GONEUPDATER, ctx.message.author)) # Send a new updater along


async def setup(bot):
    await bot.add_cog(CorpusCallosum(bot))

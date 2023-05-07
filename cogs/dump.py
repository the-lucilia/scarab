import aiohttp
import discord
from discord.ext import tasks, commands
import os
import gzip

class dump(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(hours=24, reconnect=True)
    async def dump(self):
        print(f"Starting Process. . .")
        if os.path.exists("regions.xml"):
            print("regions.xml exists, deleting.")
            os.remove("regions.xml")
            print("regions.xml deleted.")
        else:
            print("Downloading Dump")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://www.nationstates.net/pages/regions.xml.gz",
                    headers={
                        "User-Agent": f"SCARAB accession for regional daily dump, devved by nation=ghazi-rhaman_ammar"
                    },
                ) as dumpfile:
                    print("regions.xml.gz downloaded!")
                    print(f"Status: {dumpfile.status}")
                    with open("regions.xml.gz", "wb") as df:
                        async for chunk in dumpfile.content.iter_chunked(1024 * 1024):
                            df.write(chunk)
                    try:
                        print("Extracting regions.xml.gz")
                        with gzip.open("regions.xml.gz", "rb") as f:
                            with open("regions.xml", "wb") as df:
                                df.write(f.read())
                        print("regions.xml extracted!")
                    except Exception as e:
                        print(f"Error (gzip): {e}")
        except Exception as e:
            print(f"Error (aiohttp): {e}")

    @commands.command(aliases=["Dump"])
    @discord.app_commands.checks.has_any_role(
        "command"
    )  # Needs Update Command Role!
    async def start_dump(self, ctx):
        self.dump.start()  # This simply starts the above "dump" loop - which runs once a day to maintain
        # a XML file of the newest daily dump! (Could also set it to be done at a certain time each day if needed,
        # unsure if required atm though)


'''
    @commands.command()
    @discord.app_commands.checks.has_role("command")
    async def check_update(self, ctx):
'''

async def setup(bot):
    await bot.add_cog(dump(bot))

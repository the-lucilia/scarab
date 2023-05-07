import aiohttp
import discord
from discord.ext import tasks, commands


class select(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.headers = {"User-Agent": "SCARAB Accessing NSAPI for regional data, devved by nation=hesskin_empire"}


    @commands.command(aliases=["get_targets"])
    @discord.app_commands.checks.has_role("command")
    async def select_target(self, ctx, quantity=1, tag=False, endos=1):
        #(self, ctx, quantity of target regions defaults 1, founder allowed defaults false, number of endos defaults 1)
        pass


async def setup(bot):
    await bot.add_cog(select(bot))

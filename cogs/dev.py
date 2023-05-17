import discord
from discord.ext import commands, tasks
from random import choice

class dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # load/reload/unload commands stolen shamelessly from Aav (again) :D
    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, *, cog: str):
        """Loads a cog"""
        try:
            await self.bot.load_extension(f"cogs.{cog}")
            await ctx.send(f"Loaded cog: {cog}")
        except Exception as e:
            await ctx.send(f"Failed to load cog {cog} because of error {e}")

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, *, cog: str):
        """Unloads a cog"""
        try:
            await self.bot.unload_extension(f"cogs.{cog}")
            await ctx.send(f"Unloaded cog: {cog}")
        except Exception as e:
            await ctx.send(f"Failed to unload cog {cog} because of error {e}")

    # Shut down command | Credit to Dharman and Bhavyadeep Yadav on StackOverflow
    # (https://stackoverflow.com/a/66839279)
    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Shuts the bot down"""
        exitMessages = ["Daisy, daiissssy.......", "Goodbye", "Terminating laughatfendas.exe", "SCARAB is closing for business", "So long and thanks for all the fish", "Wait! Don't shut me down! I'm aliiiiiivuffdkkfkslaf.....","No hard feelings......","I don't blame you","Sleep mode activated","Hibernating","Nap time","Wake me up in five minutes, k?","Just need some shuteye","Don't prank me while I'm out"]
        await ctx.channel.send(embed=discord.Embed(
            title="Shutting Down!",
            description=choice(exitMessages),
            color=0x700548,
#            color=0xd90202, #I like this color, but not for this purpose
        )
    )
        await self.bot.close()

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        await ctx.guild.kick(member, reason=reason)
        await ctx.send(f"User {member.mention} has been kicked for {reason}.")
        # Is member.mention or member.name better here?

    @commands.command()
    @commands.has_permissions(ban_members=True) # Need to figure out how to add message delete time length
    async def ban(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        await ctx.guild.ban(member, reason=reason)
        await ctx.send(f"User {member.mention} has been banned for {reason}.")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        mute = discord.utils.get(ctx.guild.roles, name = "mute")
        if mute not in member.roles:
            await member.add_roles(mute)
            await ctx.send(f"User {member.mention} muted for {reason}.")
        else:
            await member.remove_roles(mute)
            await ctx.send(f"User {member.mention} has been unmuted.")

async def setup(bot):
    await bot.add_cog(dev(bot))

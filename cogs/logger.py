import discord
from discord.ext import commands, tasks
from datetime import datetime as dt


class logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel = None
        self.current_datetime = dt.now()  # Gets current datetime object
        self.current_date = f"{self.current_datetime.month}/{self.current_datetime.day}/{self.current_datetime.year}"  # Sets the date
        self.current_time = f"{self.current_datetime.hour}:{self.current_datetime.minute}"  # sets the time
        self.current_dt = f"{self.current_date} {self.current_time}"

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def log_setup(self, ctx, *, channel: discord.TextChannel):
        self.log_channel = channel
        await ctx.send(f"Setting {channel} as the logging channel.")
        await channel.send(f"This channel has been set as the logging channel.")

    @commands.Cog.listener("on_member_join")  # Sets it to be a listener for events
    async def Join(self, member):  # Passes the member
        guild = member.guild  # sets guild to be the members guild
        if guild.system_channel:  # If there is a system channel for that guild
            channel = guild.system_channel  # then sets that to the "channel"
            await channel.send(f"Welcome to the server, {member.mention}!")  # Sents a welcome message
        if self.log_channel:  # If there is a log channel
            await self.log_channel.send(
                f"{member} has joined the server at {self.current_dt}.")  # Sends it there as well

    @commands.Cog.listener("on_member_remove")
    async def Leave(self, member):
        guild = member.guild
        if guild.system_channel:
            channel = guild.system_channel
            await channel.send(f"Goodbye, {member}!")
        if self.log_channel:
            await self.log_channel.send(f"{member} left.")

    @commands.Cog.listener("on_message_delete")
    async def Delete(self, message):
        if self.log_channel:
            channel = self.log_channel  # Sets the channel to the log channel
            await channel.send(
                f"Deleted Message: {message.content} at {self.current_dt} by {message.author} in #{message.channel}")
            # Sends the content of the message, current times, the original author and what channel it was in

    @commands.Cog.listener("on_message_edit")
    async def Edit(self, before, after):
        if self.log_channel:
            channel = self.log_channel
            await channel.send(
                f"Edited message: {before.content} to {after.content} at {self.current_dt} by {after.author} in #{before.channel}")


async def setup(bot):
    await bot.add_cog(logger(bot))

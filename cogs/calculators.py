import discord
from discord.ext import commands
import math as ma


class Calculator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def InfCalc(self, ctx, days: float, endorsements: int, current: int):
        """Days, Endorsements, Current Influence. Calculates the influence at the end of set days."""
        influence = (2 * endorsements * days) + (2 * days) + current
        await ctx.send(f"The influence for the target nation would be {influence} after {days} days "
                       f"with {endorsements} endos")

    @commands.command()
    async def EndoCalc(self, ctx, influence: int, days: float, current: int):
        """Influence, Days, Current Influence. Calculates the endorsements to hit target inf in set days."""
        endorsements = ((influence - current) / (2 * days)) - 1
        await ctx.send(f"The amount of endorsements needed to get {influence} influence in {days} "
                       f"days is {endorsements}.")

    @commands.command()
    async def DayCalc(self, ctx, endorsements: int, influence: int, current: int):
        """Endorsements, Influence, Current Influence. Calculates the days until target influence is
        hit with set endorsements."""
        days = (influence - current) / (2 * endorsements + 2)
        await ctx.send(f"The amount of days to get {influence} influence with {endorsements} endorsements is {days}.")

    @commands.command()
    async def RoBan(self, ctx, t_current: int, current: int, t_endorsements: int, endorsements: int):
        """Target's Current Influence, Officer's Current Influence, Target's Endorsements, Officer's Endorsements.
        calculates the amount of days needed before a regional officer can ban a target nation."""
        days = (t_current - current) / (2 * t_endorsements - 2 * endorsements)
        await ctx.send(f"The amount of days for the BCRO to ban the target nation is {days}.")

    @commands.command()
    async def DelBan(self, ctx, t_current: int, current: int, t_endorsements: int, endorsements: int):
        """Target's Current Influence, Delegate's Current Influence, Target's Endorsements, Delegate's Endorsements.
        Calculates the amout of days needed before a regional delegate can ban a target nation."""
        days = (t_current - 2 * current) / (-2 * t_endorsements + 4 * endorsements + 2)
        await ctx.send(f"The amount of days for the BCRO to ban the target nation is {days}.")

    @commands.command()
    async def StabDecay(self, ctx, stable: int):
        """Desired stabilized influence. Calculates the amount of endorsements needed to hit target influence."""
        endorsements = ma.ceil(stable / 360) - 1
        await ctx.send(f"The endorsement count needed to have a total of {stable} inf is {endorsements}.")

    @commands.command()
    async def EndoDecay(self, ctx, endorsements: int):
        """Target nation's endorsements. Calculates the stabilized influence with set endorsements."""
        stable = 360 * endorsements + 360
        await ctx.send(f"The stable influence after six months with {endorsements} endorsements is {stable}.")


async def setup(bot):
    await bot.add_cog(Calculator(bot))

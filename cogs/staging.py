import discord
from discord.ext import commands, tasks


class staging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["jp", "JP", "JumpPoint", "jumppoint", "Jump_Point"])
    async def jump_point(self, ctx):
        jp_embed = discord.Embed(
            title = "Our jump point is:",
            description=(
                f"[Suspicious](https://www.nationstates.net/region=suspicious)"),
            color = 0x8EE6DD,
            )
        await ctx.send(embed=jp_embed)

    @commands.command(aliases=["present"])
    async def here(self, ctx):
        user = ctx.message.author
        present = discord.utils.get(ctx.guild.roles, name="present")
        if present not in user.roles:
            await user.add_roles(present)
            await ctx.send("ROLED")
        else:
            await user.remove_roles(present)
            await ctx.send("UNROLED")

    @commands.command(aliases=["rs", "silence"])
    @commands.has_any_role("command")
    async def radio_silence(self, ctx):
        silence = discord.utils.get(ctx.guild.roles, name="silence")
        for member in ctx.guild.members:
            for role in member.roles:
                if role.name == "present":
                    await member.add_roles(silence)
                    print(f"{member.name} silenced!")
        await ctx.send("**RADIO SILENCE**")

    @commands.command(aliases=["ers", "end_rs", "speak"])
    @commands.has_any_role("command")
    async def end_radio_silence(self, ctx):
        silence = discord.utils.get(ctx.guild.roles, name="silence")
        for member in ctx.guild.members:
            for role in member.roles:
                if role.name == silence:
                    await member.remove_roles(silence)
                    print(f"{member.name} may now SPEAK")
        await ctx.send("**RADIO SILENCE IS NOW OVER**")


async def setup(bot):
    await bot.add_cog(staging(bot))

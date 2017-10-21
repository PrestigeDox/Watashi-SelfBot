import discord
from discord.ext import commands

class ErrorFormatter:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='error', hidden=True)
    async def error_formatter(self, ctx, *, err: str):
        """ Send a nice embed error with a message
        Usage: In other cogs
        cmd = bot.get_command('error')
        await ctx.invoke(cmd, err='error message here')
        """
        em = discord.Embed(title=':x: Error', color=discord.Color.dark_red(), description=err)
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(ErrorFormatter(bot))
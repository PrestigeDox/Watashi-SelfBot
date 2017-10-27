import asyncio
from discord.ext import commands


class Clean:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['clear', 'purge'])
    async def clean(self, ctx, limit: int=None, sleep: float=1.0):
        """ Cleanse the channel of your messages """
        await ctx.message.delete()
        async for msg in ctx.channel.history(limit=limit, before=ctx.message):
            if msg.author == self.bot.user:
                await msg.delete()
                await asyncio.sleep(sleep)


def setup(bot):
    bot.add_cog(Clean(bot))

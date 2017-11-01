import asyncio
from discord.ext import commands


class Clean:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['clear', 'purge'])
    async def clean(self, ctx, limit: int=None, delay: float=1.0):
        """ Cleanse the channel of your messages """
        await ctx.message.delete()

        # Go over each message in the channel's history before your current message, delete it if it's from you
        async for msg in ctx.channel.history(limit=limit, before=ctx.message):
            if msg.author == self.bot.user:
                await msg.delete()
                await asyncio.sleep(delay)


def setup(bot):
    bot.add_cog(Clean(bot))

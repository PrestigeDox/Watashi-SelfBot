import discord
from discord.ext import commands


class TinyURL:
    def __init__(self, bot):
        self.bot = bot
        self.aiohttp_session = bot.aiohttp_session

    @commands.command()
    async def tinyurl(self, ctx, link: str = None):
        """ Convert A URL To A Shorter TinyURL """
        if link is None:
            return await ctx.error('Please provide a link to shorten!')

        api_tiny = 'http://tinyurl.com/api-create.php?url='

        async with self.aiohttp_session.get(api_tiny + link) as tiny:
            shortenurl = await tiny.read()

        shortenurl = f'<{shortenurl.decode("utf-8")}>'
        await ctx.message.edit(content=shortenurl)


def setup(bot):
    bot.add_cog(TinyURL(bot))

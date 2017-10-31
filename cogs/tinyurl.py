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

        shortenurl = shortenurl.decode("utf-8")
        emb = discord.Embed(colour=self.bot.user_color)
        emb.add_field(name="\U0001f30d Original Link",
                      value=link, inline=False)
        emb.add_field(name="Shortened Link \U0001f517",
                      value=shortenurl, inline=False)
        await ctx.message.edit(embed=emb)


def setup(bot):
    bot.add_cog(TinyURL(bot))

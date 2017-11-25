import discord
from discord.ext import commands
from bs4 import BeautifulSoup


class Images:
    def __init__(self, bot):
        self.bot = bot
        self.urls = ['http://random.cat/', 'http://random.dog/']
        self.aiohttp_session = bot.aiohttp_session
        self.color = bot.user_color

    @commands.command()
    async def cat(self, ctx):
        """ A cat from random.cat """
        # Get page source.
        async with self.aiohttp_session.get(self.urls[0]) as r:
            html = await r.text()

        # Make some really 'beautiful' soup.
        soup = BeautifulSoup(html, 'lxml')

        # Cat.
        cat = self.urls[0] + soup.select('img#cat')[0].attrs['src']

        # Create embed response.
        msg = f':cat2: Random Cat\n{cat}'

        await ctx.message.edit(content=msg)

    @commands.command()
    async def dog(self, ctx):
        """ A dog from random.dog """
        # random.dog is a bit special, it gives you a video sometimes ill just make another request if its a video
        while True:
            async with self.aiohttp_session.get(self.urls[1]) as r:
                html = await r.text()
            soup = BeautifulSoup(html, 'lxml')
            if not soup.select('img#dog-img'):
                continue
            dog = self.urls[1] + soup.select('img#dog-img')[0].attrs['src']
            break

        # Create embed response.
        msg = f':dog2: Random dog\n{dog}'

        await ctx.send(content=msg)


def setup(bot):
    bot.add_cog(Images(bot))

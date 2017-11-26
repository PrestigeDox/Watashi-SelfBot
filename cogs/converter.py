import discord
from discord.ext import commands
from bs4 import BeautifulSoup
from urllib.parse import quote_plus


class Converter:
    def __init__(self, bot):
        self.bot = bot
        self.aiohttp_session = bot.aiohttp_session
        self.url = 'https://google.com/search'
        self.headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR '
                          '2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; MS-RTC LM 8; '
                          'InfoPath.3; .NET4.0C; .NET4.0E) chromeframe/8.0.552.224',
            'Accept-Language': 'en-us',
            'Cache-Control': 'no-cache'
            }

    @commands.command()
    async def convert(self, ctx,  *, query=None):
        """ Calculate some expressions! """
        # Handle no query being provided
        if query is None:
            return await ctx.error('Please provide a query!')

        from_unit = query.split()[0]
        to_unit = query.split()[1]

        try:
            val = float(query.split()[2])
        except ValueError:
            return await ctx.error('Invalid query.')

        # Doing this in the f-string later would become f-string-ception and that doesn't work
        qstr = quote_plus(f'{val} {from_unit} to {to_unit}')

        # Tries its best to imitate a real browser visit, an old user-agent is used to make scraping easier
        async with self.aiohttp_session.get(f'{self.url}?q={qstr}&source=hp', headers=self.headers) as r:
            html = await r.text()

        # Beautiful soup
        soup = BeautifulSoup(html, 'lxml')

        # The span inside div._Qeb has the result for the expression, if it doesnt exist google doesn't like
        # your expression or its just invalid
        if not soup.select('div#ires div._Qeb span'):
            return await ctx.error('Could not convert expression.')

        # Values with units
        from_val = soup.select("div#ires div._Qeb span")[0].text.split()[0]
        to_val = soup.select("div#ires div._Peb")[0].text.split()[0]

        await ctx.message.edit(content=f"{from_val}{from_unit} = {to_val}{to_unit}")


def setup(bot):
    bot.add_cog(Converter(bot))

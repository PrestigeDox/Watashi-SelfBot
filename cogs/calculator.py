import discord
from discord.ext import commands
from bs4 import BeautifulSoup
from urllib.parse import quote_plus


class Calculator:
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

    @commands.command(aliases=['calc'])
    async def calculate(self, ctx, *, query: str=None):
        """ Calculate some expressions! """
        # Handle no query being provided
        if query is None:
            return await ctx.error('Please provide a query!')

        params = {'q': quote_plus(query.replace(" ", "")), 'source': 'hp'}

        # Tries its best to imitate a real browser visit, an old user-agent is used to make scraping easier
        async with self.aiohttp_session.get(self.url, params=params, headers=self.headers) as r:
            html = await r.text()

        # Beautiful soup
        soup = BeautifulSoup(html, 'lxml')

        # The span inside div#topstuff has the result for the expression, if it doesnt exist google doesn't like
        # your expression or its just invalid
        if not soup.select('div#topstuff span.nobr'):
            return await ctx.error('Could not calculate expression!')

        result = soup.select('div#topstuff span.nobr')[0].text

        # Create Embed response
        em = discord.Embed(color=self.bot.user_color)
        em.add_field(name="Expression", value=query)
        em.add_field(name="Result", value=result.split('=')[1].strip())
        em.set_author(name="Calculator", icon_url="https://maxcdn.icons8.com/Share/icon/Science/calculator1600.png")

        await ctx.message.edit(embed=em)


def setup(bot):
    bot.add_cog(Calculator(bot))

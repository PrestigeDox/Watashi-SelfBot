import discord
from discord.ext import commands
from bs4 import BeautifulSoup


class Weather:
    def __init__(self, bot):
        self.bot = bot
        self.url = 'https://www.bing.com/search?q=weather+in'
        self.headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR '
                          '2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; MS-RTC LM 8; '
                          'InfoPath.3; .NET4.0C; .NET4.0E) chromeframe/8.0.552.224'}
        self.color = bot.user_color
        self.aiohttp_session = bot.aiohttp_session

    @commands.command()
    async def weather(self, ctx,  *, query: str = None):
        """ Search Bing for weather """

        await ctx.message.delete()

        # Handle no query being provided.
        if query is None:
            return await ctx.invoke(self.bot.get_command('error'), delete_after=1.0, err='Please provide a query!')

        # Get page source with custom headers.
        async with self.aiohttp_session.get(self.url+query.replace(' ', '+'), headers=self.headers) as r:
            html = await r.text()

        # Make some really 'beautiful' soup.
        soup = BeautifulSoup(html)

        # Using a very old user agent, scraping is made very trivial.
        # If it can't find title with that selector, location is probably bogus or there's no available info about it.
        try:
            title = soup.select('div.wtr_locTitle')[0].text
        except IndexError:
            return await ctx.invoke(self.bot.get_command('error'), delete_after=1.0, err='Unable to provide weather '
                                                                                         'for this location!')

        icon = soup.select('div.wtr_currIcon img')[0].attrs['src']
        temp = soup.select('div.wtr_condiTemp')[0].text.strip('F')
        precipitation = soup.select('div.wtr_currPerci')[0].text.split()[1]
        wind = soup.select('div.wtr_currWind')[0].text.split(':')[1].strip()
        humidity = soup.select('div.wtr_currHumi')[0].text.split(':')[1].strip()
        caption = soup.select('div.wtr_caption')[0].text
        daytime = soup.select('div.wtr_dayTime')[0].text

        # Create embed response
        em = discord.Embed(title='Weather in '+title,
                           description=caption,
                           color=self.self.color)

        em.add_field(name='Temperature', value=temp)
        em.add_field(name='Precipitation', value=precipitation, inline=True)
        em.add_field(name="Wind", value=wind, inline=True)
        em.add_field(name="Humidity", value=humidity)
        em.add_field(name="Time and Date", value=daytime)
        em.set_thumbnail(url=icon)

        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Weather(bot))

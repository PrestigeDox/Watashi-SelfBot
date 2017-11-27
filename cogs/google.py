import discord
import json

from discord.ext import commands
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from urllib.parse import urlparse
from urllib.parse import parse_qs


class Google:
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
        self.image_headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235"
                          "7.134 Safari/537.36",
            'Accept-Language': 'en-us',
            'Cache-Control': 'no-cache'
            }

    @commands.group(name="google", aliases=['g'], invoke_without_command=True)
    async def google(self, ctx, *, query: str=None):
        """ Search Google for a query """
        # Handle no query being provided
        if query is None:
            return await ctx.error('Please provide a query!')

        # 'google_embed' is dependent on a test that checks whether google has embedded any external data on the page
        # 'result_nums' is the no. of results to display when there is no embedded data
        google_embed = False
        params = {'q': quote_plus(query), 'source': 'hp'}
        results_num = 3

        # Tries its best to imitate a real browser visit, an old user-agent is used to make scraping easier
        async with self.aiohttp_session.get(self.url, params=params, headers=self.headers) as r:
            html = await r.text()

        # Beautiful soup
        soup = BeautifulSoup(html, 'lxml')

        # Get links and their brief descriptions, only upto 4 are taken at a time, it should've been three, but
        # if you read the code, it tries to work around an extra entry that is just 'Images for '.
        # URLs on google search are redirected through 'google.com/url?url=xxxxx' , this uses cgi and urlparse to
        # grab only the 'url' URL parameter and get rid of the other parameters google passes for logging etc to
        # 'google.com/url'
        result_links = [parse_qs(urlparse(x.attrs['href'])[4])['url'][0] for x in soup.select('div.g h3.r a')[:4] if
                        '/search' not in x.attrs['href'] and not x.text == '']
        result_desc = [x.text for x in soup.select('div#ires div.g div.s span.st')[:4] if
                       '/search' not in x.text and not x.text == '']

        # 'hp-xpdbox' is the class for google's embedded data, if this exists, google_embed is changed to True
        # and results are changed to 2
        if soup.select('div.hp-xpdbox div._tXc'):
            google_embed = True
            embed_title = [a.text for a in soup.select('div._B5d')][0]
            try:
                embed_type = [a.text for a in soup.select('div._Pxg')][0]
            except IndexError:
                embed_type = None
            embed_details = [a.text for a in soup.select('div._tXc span')][0]
            results_num -= 1

            # Embedded data might not always have an image, this works around that
            img = None
            try:
                img = [img.attrs.get('src') for img in soup.select('div._i8d img')][0]
            except IndexError:
                pass

        # Create embed if google_embed is true
        if google_embed:
            msg = f"**{embed_title}**"
            if embed_type is not None:
                msg += f" ({embed_type})"
            msg += f"\n\n{embed_details}\n"
            if img:
                msg += f"**Image:**\n{img}"

        results = "\n\n".join([f'<{link}>\n{desc}' for link, desc in list(zip(result_links, result_desc))[:results_num]])

        if google_embed:
            await ctx.message.edit(content=f"**Results for {query}:**\n{results}\n\n{msg}")
        else:
            await ctx.message.edit(content=f"**Results for {query}:**\n{results}")

    @google.command(name="images", aliases=['img', 'image'])
    async def images(self, ctx, *, query: str=None):
        """ Search Google for Images """
        # Handle empty query
        if query is None:
            return await ctx.error('Please provide a query!')

        # Using these specific headers and "lnms" as source, will provide divs with "rg_meta" classes,
        # The modern image search page being JS rendered, data in these divs are jsons with raw image URLs
        # Old image search pages, only have thumbnails and a direct link to websites
        params = {'q': quote_plus(query), 'source': 'lmns', 'tbm': 'isch'}
        async with self.aiohttp_session.get(self.url, params=params, headers=self.image_headers) as r:
            html = await r.text()

        # Healthy
        soup = BeautifulSoup(html, 'lxml')

        # Go over 4 items, json.loads the item text, and grab "ou" probably stands for "original url"
        images = []
        for i, item in enumerate(soup.select('div.rg_meta')[:4]):
            js = json.loads(item.text)
            images.append((f"{i+1}. {js['st']} - {js['s']}", js["ou"]))
        newl = '\n'
        await ctx.message.edit(content=f"```py\n{newl.join([x[0] for x in images])}"
                                       f"\n# Choose the appropriate number or type 0 to leave\n```")

        def check(m):
            return m.author == ctx.author and m.content.isdigit() and m.channel == ctx.channel
        message = await self.bot.wait_for('message', check=check)
        if message.content == "0":
            await message.delete()
            return await ctx.message.delete()
        choice = int(message.content) - 1
        await message.delete()
        await ctx.message.edit(content=images[choice][1])


def setup(bot):
    bot.add_cog(Google(bot))

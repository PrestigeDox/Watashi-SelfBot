import discord
from discord.ext import commands
from bs4 import BeautifulSoup

class Define:
    def __init__(self, bot):
        self.bot = bot
        self.aiohttp_session = bot.aiohttp_session
        self.url = 'https://google.com/search'
        self.headers = {'User-Agent':
                        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) ' 
                        'Chrome/41.0.2228.0 Safari/537.36'***REMOVED***
        self.parts_of_speech = {'noun': 'n.', 'verb': 'v.', 'adjective': 'adj.', 'adverb': 'adv.',
                                'interjection': 'interj.', 'conjunction': 'conj.', 'preposition': 'prep.',
                                'pronoun': 'pron.'***REMOVED***

    @commands.command(aliases=['def'])
    async def define(self, ctx, word: str):
        """ Define a word """
        params = {'q': f'define+{word***REMOVED***', 'source': 'hp'***REMOVED***

        async with self.aiohttp_session.get(self.url, params=params, headers=self.headers) as r:
            html = await r.text()

        soup = BeautifulSoup(html, 'lxml')

        try:
            defn_list = [x.text for x in soup.find_all('div', attrs={'data-dobid': 'dfn'***REMOVED***)]
            pos_list = [x.span.text for x in soup.find_all('div', attrs={'class': 'lr_dct_sf_h'***REMOVED***)]

        except AttributeError:
            print('Unable to find definition. Ensure you do not have to do a Google captcha.')
            return await ctx.invoke(self.bot.get_command('error'), err=f'Unable to find a definition for `{word***REMOVED***`.')

        await ctx.send(f'{defn_list***REMOVED***\n{pos_list***REMOVED***')


def setup(bot):
    bot.add_cog(Define(bot))

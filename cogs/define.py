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
                        'Chrome/41.0.2228.0 Safari/537.36'}
        self.parts_of_speech = {'noun': 'n.', 'verb': 'v.', 'adjective': 'adj.', 'adverb': 'adv.',
                                'interjection': 'interj.', 'conjunction': 'conj.', 'preposition': 'prep.',
                                'pronoun': 'pron.'}

    @commands.command(aliases=['def'])
    async def define(self, ctx, word: str):
        """ Define a word """
        params = {'q': f'define+{word}', 'source': 'hp'}

        async with self.aiohttp_session.get(self.url, params=params, headers=self.headers) as r:
            html = await r.text()

        soup = BeautifulSoup(html, 'lxml')

        try:
            defn = soup.find('div', attrs={'data-dobid': 'dfn'}).span.text
            pos = self.parts_of_speech[soup.find('div', attrs={'class': 'lr_dct_sf_h'}).span.text]

        except AttributeError:
            print('Unable to find definition. Ensure you do not have to do a Google captcha.')
            return await ctx.invoke(self.bot.get_command('error'), err=f'Unable to find a definition for `{word}`.')

        await ctx.send(f'{word} _{pos}_ {defn}')


def setup(bot):
    bot.add_cog(Define(bot))

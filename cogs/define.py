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
        """ Find the definition of a word """
        params = {'q': f'define+{word}', 'source': 'hp'}

        async with self.aiohttp_session.get(self.url, params=params, headers=self.headers) as r:
            html = await r.text()

        soup = BeautifulSoup(html, 'lxml')

        try:
            defn = soup.find('div', attrs={'data-dobid': 'dfn'}).text
            pos = soup.find('div', attrs={'class': 'lr_dct_sf_h'}).span.text
            syn_list = [x.text for x in soup.find_all(
                'span', attrs={'class': '_Yht'})]

        except AttributeError:
            print(
                'Unable to find definition. Ensure you do not have to do a Google captcha.')
            return await ctx.invoke(self.bot.get_command('error'), err=f'Unable to find a definition for `{word}`.')

        # Create embed
        em = discord.Embed(title=word.capitalize(),
                           color=discord.Color.blurple())
        em.add_field(name='Definition',
                     value=f'_{self.parts_of_speech[pos]}_, {defn}')

        if len(syn_list) != 0:
            em.add_field(name='Synonyms', value=', '.join(
                syn_list[:5]), inline=False)

        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Define(bot))

import discord
from discord.ext import commands
from bs4 import BeautifulSoup


class Define:
    def __init__(self, bot):
        self.bot = bot
        self.aiohttp_session = bot.aiohttp_session
        self.color = bot.user_color
        self.url = 'https://google.com/search'
        self.headers = {'User-Agent':
                        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/41.0.2228.0 Safari/537.36'}
        self.parts_of_speech = {'noun': 'n.', 'verb': 'v.', 'adjective': 'adj.', 'adverb': 'adv.',
                                'interjection': 'interj.', 'conjunction': 'conj.', 'preposition': 'prep.',
                                'pronoun': 'pron.', 'contraction': 'cont.'}

    @commands.command(aliases=['def'])
    async def define(self, ctx, word: str):
        """ Find the definition of a word """
        params = {'q': f'define+{word}', 'source': 'hp'}

        # Request page source with custom headers and params from above
        async with self.aiohttp_session.get(self.url, params=params, headers=self.headers) as r:
            html = await r.text()

        # Soup
        soup = BeautifulSoup(html, 'lxml')

        # Looks for google's embedded word data, raised AttributeError is caught to inform of possible reasons
        # to why no definition was found
        try:
            defn = soup.find('div', attrs={'data-dobid': 'dfn'}).text
            pos = soup.find('div', attrs={'class': 'lr_dct_sf_h'}).span.text
            syn_list = [x.text for x in soup.find_all('span', attrs={'class': '_Yht'})]

        except AttributeError:
            print('Unable to find definition. Ensure you do not have to do a Google captcha.')
            return await ctx.error(f'Unable to find a definition for `{word}`.')

        # Create embed
        em = discord.Embed(title=word.capitalize(), color=self.color)
        em.add_field(name='Definition', value=f'_{self.parts_of_speech[pos]}_, {defn}')
        msg = f"**{word.capitalize()}:**\n_{self.parts_of_speech[pos]}_, {defn}"
        if len(syn_list) != 0:
            msg += f"\n**Synonyms:**\n{', '.join(syn_list[:5])}"

        await ctx.message.edit(content=msg)


def setup(bot):
    bot.add_cog(Define(bot))

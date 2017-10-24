import discord
from discord.ext import commands
from bs4 import BeautifulSoup


class Translate:
    def __init__(self, bot):
        self.bot = bot
        self.url = 'https://translate.google.com/m'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 '
                                      '(KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
        self.aiohttp_session = bot.aiohttp_session
        self.abv_dict = {'Afrikaans': 'af', 'Irish': 'ga', 'Albanian': 'sq', 'Italian': 'it', 'Arabic': 'ar',
                         'Japanese': 'ja', 'Azerbaijani': 'az', 'Kannada': 'kn', 'Basque': 'eu', 'Korean': 'ko',
                         'Bengali': 'bn', 'Latin': 'la', 'Belarusian': 'be', 'Latvian': 'lv', 'Bulgarian': 'bg',
                         'Lithuanian': 'lt', 'Catalan': 'ca', 'Macedonian': 'mk', 'Chinese Simplified': 'zh-CN',
                         'Malay': 'ms', 'Chinese Traditional': 'zh-TW', 'Maltese': 'mt', 'Croatian': 'hr', 'Norwegian': 'no',
                         'Czech': 'cs', 'Persian': 'fa', 'Danish': 'da', 'Polish': 'pl', 'Dutch': 'nl', 'Portuguese': 'pt',
                         'English': 'en', 'Romanian': 'ro', 'Esperanto': 'eo', 'Russian': 'ru', 'Estonian': 'et',
                         'Serbian': 'sr', 'Filipino': 'tl', 'Slovak': 'sk', 'Finnish': 'fi', 'Slovenian': 'sl',
                         'French': 'fr', 'Spanish': 'es', 'Galician': 'gl', 'Swahili': 'sw', 'Georgian': 'ka',
                         'Swedish': 'sv', 'German': 'de', 'Tamil': 'ta', 'Greek': 'el', 'Telugu': 'te',
                         'Gujarati': 'gu', 'Thai': 'th', 'Haitian Creole': 'ht', 'Turkish': 'tr', 'Hebrew': 'iw',
                         'Ukrainian': 'uk', 'Hindi': 'hi', 'Urdu': 'ur', 'Hungarian': 'hu', 'Vietnamese': 'vi',
                         'Icelandic': 'is', 'Welsh': 'cy', 'Indonesian': 'id', 'Yiddish': 'yi'}

    @staticmethod
    def get_translation(html: str):
        """ Small helper method to scrape and return translations """
        soup = BeautifulSoup(html, 'lxml')
        try:
            return soup.find('div', attrs={'class': 't0'}).text
        except AttributeError:
            return None

    @commands.group(invoke_without_command=True, aliases=['tr'])
    async def translate(self, ctx, from_lang: str, to_lang: str, *, query: str):
        """ Translate some text to another language

        Specify the two-letter language code before your query
        i.e. 'en' for English or 'es' for Spanish
        Example: <prefix>translate en es I am very hungry, please help """

        inverted_abv_dict = {v: k for k, v in self.abv_dict.items()}
        err_cmd = self.bot.get_command('error')

        if len(to_lang) + len(from_lang) != 4:
            return await ctx.invoke(err_cmd,
                                    err='Language code must be 2 characters long.',
                                    del_msg=ctx.message)

        if to_lang not in inverted_abv_dict:
            return await ctx.invoke(err_cmd,
                                    err=f'Language abbreviation `{to_lang}` not found.',
                                    del_msg=ctx.message)

        if from_lang not in inverted_abv_dict:
            return await ctx.invoke(err_cmd,
                                    err=f'Language abbreviation `{from_lang}` not found.',
                                    del_msg=ctx.message)

        # Delete the original message because the information is contained in the embed anyway
        await ctx.message.delete()

        # Params for the request
        params = {'sl': from_lang, 'hl': to_lang, 'q': query}

        async with self.aiohttp_session.get(self.url, headers=self.headers, params=params) as r:
            html = await r.text()

        # Parse the HTML for a translation
        trans_text = self.get_translation(html)

        if trans_text is None:
            return await ctx.invoke(self.bot.get_command('error'),
                                    err=f"Couldn't find a translation for `{query}`.",
                                    del_msg=ctx.message)

        # Create embed response
        em = discord.Embed(title='Translation',
                           description=f'{inverted_abv_dict[from_lang]} -> {inverted_abv_dict[to_lang]}',
                           color=self.bot.embed_colour)

        em.add_field(name='Original Text', value=f'`{query}`')
        em.add_field(name='Translated', value=f'`{trans_text}`')

        await ctx.send(embed=em)

    @translate.command(name='abbreviations', aliases=['abv', 'ab'])
    async def list_abv(self, ctx, *, query: str=None):
        """ Get a GIANT list of abbreviations, or search for one (recommended) """
        em = discord.Embed(color=self.bot.embed_colour)

        # Sends a giant spammy list
        if query is None:
            em.add_field(name='Language - Abbreviation', value='\n'.join([f'{x} - `{self.abv_dict[x]}`'
                                                                          for x in self.abv_dict.keys()]))
            return await ctx.send(embed=em)

        query = query.title()
        closest_match = None

        # Finds the closest item to a search
        if query not in self.abv_dict:
            closest_match = min(self.abv_dict, key=lambda v: len(set(query) ^ set(v)))

        # Create an embed for style points
        if closest_match:
            em.title = 'Closest Abbreviation'
            em.description = f'{closest_match} - `{self.abv_dict[closest_match]}`'
        else:
            em.title = 'Matching Abbreviation'
            em.description = f'{query} - `{self.abv_dict[query]}`'

        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Translate(bot))

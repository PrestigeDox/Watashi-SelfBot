import columnize
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
        self.color = bot.user_color
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

        if len(to_lang) + len(from_lang) != 4:
            return await ctx.error('Language code must be 2 characters long.')

        if to_lang not in inverted_abv_dict:
            return await ctx.error(f'Language abbreviation `{to_lang}` not found.')

        if from_lang not in inverted_abv_dict:
            return await ctx.error(f'Language abbreviation `{from_lang}` not found.')

        # Params for the request
        params = {'sl': from_lang, 'hl': to_lang, 'q': query}

        async with self.aiohttp_session.get(self.url, headers=self.headers, params=params) as r:
            html = await r.text()

        # Parse the HTML for a translation
        trans_text = self.get_translation(html)

        if trans_text is None:
            return await ctx.error(f'Could not find a translation for `{query}`.')

        msg = f'**{inverted_abv_dict[from_lang]} -> {inverted_abv_dict[to_lang]}**\n'
        msg += f'`{query}` -> `{trans_text}`'

        await ctx.message.edit(content=msg)

    @translate.command(name='abbreviations', aliases=['abv', 'ab'])
    async def list_abv(self, ctx, *, query: str=None):
        """ Get a GIANT list of abbreviations, or search for one (recommended) """
        em = discord.Embed(color=self.color)

        # Sends a giant spammy list
        if query is None:
            abv_list = columnize.columnize([f'{x} - `{self.abv_dict[x]}`' for x in self.abv_dict], displaywidth=100)
            return await ctx.message.edit(content=f"**Abbreviations:**\n{abv_list}")

        query = query.title()
        closest_match = None

        # Finds the closest item to a search
        if query not in self.abv_dict:
            closest_match = min(self.abv_dict, key=lambda v: len(set(query) ^ set(v)))

        if closest_match:
            msg = '**Closest Abbreviation**'
            msg += f'{closest_match} - `{self.abv_dict[closest_match]}`'
        else:
            msg = '**Matching Abbreviation**'
            msg += f'{query} - `{self.abv_dict[query]}`'

        await ctx.message.edit(content=msg)


def setup(bot):
    bot.add_cog(Translate(bot))

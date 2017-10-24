import re
from discord.ext import commands


class Aesthetic:
    def __init__(self, bot):
        self.bot = bot
        self.pattern = re.compile('[^a-z0-9*() ]')

    @commands.command(aliases=['aesthet', 'at'])
    async def aesthetic(self, ctx, *, a_text):
        """Larger Text Converter"""
        ascii_to_wide = dict((i, chr(i + 0xfee0)) for i in range(0x21, 0x7f))
        ascii_to_wide.update({0x20: u'\u3000', 0x2D: u'\u2212'})

        await ctx.message.edit(content='{}'.format(a_text.translate(ascii_to_wide)))

    @commands.command(aliases=['tinyfont', 'small', 'smallfont'])
    async def tiny(self, ctx, *, text: str = None):
        """Tiny Text Converter"""
        await ctx.message.delete()
        lower_text = text.lower()

        # The above pattern removes any characters which don't have a tiny counterpart
        text_list = list(re.sub(self.pattern, '', lower_text))

        char_map = {'a': '\u1d43', 'b': '\u1d47', 'c': '\u1d9c', 'd': '\u1d48', 'e': '\u1d49', 'f': '\u1da0',
                    'g': '\u1d4d', 'h': '\u02b0', 'i': '\u1da6', 'j': '\u02b2', 'k': '\u1d4f', 'l': '\u02e1',
                    'm': '\u1d50', 'n': '\u207f', 'o': '\u1d52', 'p': '\u1d56', 'q': '\u146b', 'r': '\u02b3',
                    's': '\u02e2', 't': '\u1d57', 'u': '\u1d58', 'v': '\u1d5b', 'w': '\u02b7', 'x': '\u02e3',
                    'y': '\u02b8', 'z': '\u1dbb', '1': '\\xb9', '2': '\\xb2', '3': '\\xb3', '4': '\u2074',
                    '5': '\u2075', '6': '\u2076', '7': '\u2077', '8': '\u2078', '9': '\u2079', '0': '\u2070', '*': '*',
                    '(': '\u207d', ')': '\u207e', ' ': '\u202f'}

        # Substitute big letters for small
        for idx, char in enumerate(text_list):
            text_list[idx] = char_map[char]

        await ctx.channel.send(''.join(text_list))


def setup(bot):
    bot.add_cog(Aesthetic(bot))

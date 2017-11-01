import string
from discord.ext import commands


class Aesthetic:
    def __init__(self, bot):
        self.bot = bot
        self.tiny_table = str.maketrans(string.ascii_lowercase, 'ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖ٩ʳˢᵗᵘᵛʷˣʸᶻ')
        self.flip_table = str.maketrans(string.ascii_lowercase, '\u0250q\u0254p\u01dd\u025f\u0183\u0265\u0131\u027e'
                                                                '\u029e\u05df\u026fuodb\u0279s\u0287n\u028c\u028dx'
                                                                '\u028ez')

    @commands.command(aliases=['aesthet', 'at'])
    async def aesthetic(self, ctx, *, a_text: str = None):
        """ Larger Text Converter """

        # Handle no text being provided
        if a_text is None:
            return await ctx.error('Please provide text to convert!')

        ascii_to_wide = dict((i, chr(i + 0xfee0)) for i in range(0x21, 0x7f))
        ascii_to_wide.update({0x20: u'\u3000', 0x2D: u'\u2212'})

        await ctx.message.edit(content=f'{a_text.translate(ascii_to_wide)}')

    @commands.command(aliases=['tinyfont', 'small', 'smallfont'])
    async def tiny(self, ctx, *, text: str = None):
        """ Tiny Text Converter """

        # Handle no text being provided
        if text is None:
            return await ctx.error('Please provide text to convert!')

        # Convert text to lowercase and use the tiny_table translation table to translate text.
        await ctx.message.edit(content=text.lower().translate(self.tiny_table))

    @commands.command()
    async def textflip(self, ctx, *, text: str = None):
        """ Upside Down Text """

        # Handle no text being provided
        if text is None:
            return await ctx.error('Please provide text to convert!')

        # Convert text to lowercase and use the flip_table translation table to translate text.
        await ctx.message.edit(content=text.lower().translate(self.flip_table)[::-1])


def setup(bot):
    bot.add_cog(Aesthetic(bot))

import string
from discord.ext import commands


class Aesthetic:
    def __init__(self, bot):
        self.bot = bot
        self.tiny_table = str.maketrans(string.ascii_lowercase, 'ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖ٩ʳˢᵗᵘᵛʷˣʸᶻ')

    @commands.command(aliases=['aesthet', 'at'])
    async def aesthetic(self, ctx, *, a_text):
        """ Larger Text Converter """
        ascii_to_wide = dict((i, chr(i + 0xfee0)) for i in range(0x21, 0x7f))
        ascii_to_wide.update({0x20: u'\u3000', 0x2D: u'\u2212'})

        await ctx.message.edit(content='{}'.format(a_text.translate(ascii_to_wide)))

    @commands.command(aliases=['tinyfont', 'small', 'smallfont'])
    async def tiny(self, ctx, *, text: str = None):
        """ Tiny Text Converter """
        await ctx.message.delete()

        textlower = text.lower()
        dvl = textlower.translate(self.tiny_table)
        await ctx.channel.send(dvl)


def setup(bot):
    bot.add_cog(Aesthetic(bot))

import discord
from discord.ext import commands


class Aesthetic:
    def __init__(self, bot):
        self.bot = bot

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
        textlower = text.lower()
        dvl = textlower.replace('a', 'ᵃ').replace('b', 'ᵇ').replace('c', 'ᶜ').replace('d', 'ᵈ') \
            .replace('e', 'ᵉ').replace('f', 'ᶠ').replace('g', 'ᵍ').replace('h', 'ʰ') \
            .replace('i', 'ⁱ').replace('j', 'ʲ').replace('k', 'ᵏ').replace('l', 'ˡ') \
            .replace('m', 'ᵐ').replace('n', 'ⁿ').replace('o', 'ᵒ').replace('p', 'ᵖ') \
            .replace('q', '٩').replace('r', 'ʳ').replace('s', 'ˢ').replace('t', 'ᵗ') \
            .replace('u', 'ᵘ').replace('v', 'ᵛ').replace('w', 'ʷ').replace('x', 'ˣ') \
            .replace('y', 'ʸ').replace('z', 'ᶻ')
        await ctx.channel.send(dvl)


def setup(bot):
    bot.add_cog(Aesthetic(bot))

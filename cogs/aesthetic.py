import discord
from discord.ext import commands


class Aesthetic:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['aesthet', 'at'])
    async def aesthetic(self, ctx, *, a_text):
        ascii_to_wide = dict((i, chr(i + 0xfee0)) for i in range(0x21, 0x7f))
        ascii_to_wide.update({0x20: u'\u3000', 0x2D: u'\u2212'***REMOVED***)
        await ctx.message.edit(content='{***REMOVED***'.format(a_text.translate(ascii_to_wide)))


def setup(bot):
    bot.add_cog(Aesthetic(bot))

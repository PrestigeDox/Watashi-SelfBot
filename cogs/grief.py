'''
Griefing on a server can lead to a ban.
When you get banned via using this cog
the owners of this bot are not liable
under the MIT licese. It may lead to
the disabling of your account.
'''

import discord
from discord.ext import commands


class Grief:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def spam(self, ctx, amount: int = 10, *, message: str = None):
        if message == None:
            await ctx.message.delete()
            emb = discord.Embed(colour=self.bot.red)
            emb.add_field(name=":x: Error",
                          value="Message is a missing variable")
            await ctx.send(embed=emb)
        else:
            await ctx.message.delete()
            for x in range(amount):
                await ctx.send(message)

    @commands.command()
    async def dmspam(self, ctx, amount: int = 10, user: discord.Member = None, *, message: str = None):
        if user == None:
            await ctx.message.delete()
            emb = discord.Embed(colour=self.bot.red)
            emb.add_field(name=":x: Error", value="User is a missing variable")
            await ctx.send(embed=emb)
        elif message == None:
            await ctx.message.delete()
            emb = discord.Embed(colour=self.bot.red)
            emb.add_field(name=":x: Error",
                          value="Message is a missing variable")
            await ctx.send(embed=emb)
        else:
            await ctx.message.delete()
            for x in range(amount):
                await user.send(message)


def setup(bot):
    bot.add_cog(Grief(bot))

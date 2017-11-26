import discord
import urbandictionary as ud
from discord.ext import commands


class UrbanDictionary:
    def __init__(self, bot):
        self.bot = bot
        self.color = bot.user_color

    @commands.group(invoke_without_command=True, aliases=['ud', 'urbandict'])
    async def urban(self, ctx, *, query: str):
        """ Check UrbanDictionary for the meaning of a word """
        try:
            resultlst = await self.bot.loop.run_in_executor(None, ud.define, query)
            item = resultlst[0]
        except IndexError:
            return await ctx.error(f'Unable to find definition for `{query}`.')

        msg = f"**Word:**\n{item.word}\n"
        msg += f"**Definition:**\n{item.definition}\n"
        msg += f"**Example(s)**\n{item.example}"
        await ctx.message.edit(content=msg)

    @urban.command(aliases=['-r'])
    async def random(self, ctx):
        """ Get a Random Word and its Meaning from UrbanDictionary """
        item = await self.bot.loop.run_in_executor(None, ud.random)

        item = item[0]
        msg = f"**Word:**\n{item.word}\n"
        msg += f"**Definition:**\n{item.definition}\n"
        msg += f"**Example(s)**\n{item.example}"
        await ctx.message.edit(content=msg)


def setup(bot):
    bot.add_cog(UrbanDictionary(bot))

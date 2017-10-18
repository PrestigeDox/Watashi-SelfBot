import discord
import urbandictionary as ud
from discord.ext import commands


class UrbanDictionary:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, aliases=['ud', 'urbandict'])
    async def urban(self, ctx, *, query: str):
        await ctx.message.delete()
        try:
            resultlst = await self.bot.loop.run_in_executor(None, ud.define, query)
            item = resultlst[0]
        except:
            return
        await ctx.send('**{0}**:\n\n{1}\n\n**Examples**:\n\n{2}'.format(item.word, item.definition, item.example))

    @urban.command(aliases=['-s'])
    async def search(self, ctx, *, query: str):
        await ctx.message.delete()
        resultlst = await self.bot.loop.run_in_executor(None, ud.define, query)

        msg = str()
        for number, option in enumerate(resultlst[:4]):
            msg += "{0}. {1}\n".format(number + 1, option.word)
        em = discord.Embed(title="Results", description=msg,
                           color=self.bot.embed_colour)
        em.set_footer(text="Type 'exit' to leave the menu.")
        menumsg = await ctx.send(embed=em)

        def check(m):
            return m.author == ctx.message.author and m.channel == ctx.message.channel and m.content.isdigit()
        response = await self.bot.wait_for('message', check=check)

        try:
            if response.content.lower() == 'exit':
                await response.delete()
                await menumsg.delete()
                return
            else:
                await response.delete()
                await menumsg.delete()
                item = resultlst[int(response.content) - 1]
        except IndexError:
            return

        await ctx.send('**{0}**:\n\n{1}\n\n**Examples**:\n\n{2}'.format(item.word, item.definition, item.example))

    @urban.command(aliases=['-r'])
    async def random(self, ctx):
        await ctx.message.delete()
        item = await self.bot.loop.run_in_executor(None, ud.random)

        await ctx.send('**{0}**:\n\n{1}\n\n**Examples**:\n\n{2}'.format(item[0].word, item[0].definition, item[0].example))


def setup(bot):
    bot.add_cog(UrbanDictionary(bot))

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
        except:
            return await ctx.error(f'Unable to find definition for `{query}`.')

        em = discord.Embed(color=self.color)
        em.set_author(name="\U0001f4d6 Urban Dictionary")
        em.add_field(name="Word", value=item.word, inline=False)
        em.add_field(name="Definition", value=item.definition, inline=False)
        em.add_field(name="Example(s)", value=item.example, inline=False)
        await ctx.message.edit(embed=em, content=None)

    @urban.command(aliases=['-s'])
    async def search(self, ctx, *, query: str):
        """ Search UrbanDictoinary for a Specific Word """

        # TODO:
        # Re-evaluate this command
        # Reason: very spammy and not necessarily intuitive for the user
        resultlst = await self.bot.loop.run_in_executor(None, ud.define, query)

        msg = str()
        for number, option in enumerate(resultlst[:4]):
            msg += "{0}. {1}\n".format(number + 1, option.word)
        em = discord.Embed(title="Results", description=msg, color=self.color)
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

        em = discord.Embed(color=self.color)
        em.set_author(name="\U0001f4d6 Urban Dictionary")
        em.add_field(name="Word", value=item.word)
        em.add_field(name="Definition", value=item.definition)
        em.add_field(name="Example(s)", value=item.example)
        await ctx.message.edit(embed=em, content=None)

    @urban.command(aliases=['-r'])
    async def random(self, ctx):
        """ Get a Random Word and its Meaning from UrbanDictionary """
        item = await self.bot.loop.run_in_executor(None, ud.random)

        em = discord.Embed(color=self.color)
        em.set_author(name="\U0001f4d6 Urban Dictionary")
        em.add_field(name="Word", value=item[0].word)
        em.add_field(name="Definition", value=item[0].definition)
        em.add_field(name="Example(s)", value=item[0].example)
        await ctx.message.edit(embed=em, content=None)


def setup(bot):
    bot.add_cog(UrbanDictionary(bot))

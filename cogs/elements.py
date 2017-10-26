import discord
import cogs.table as table
from discord.ext import commands


class Elements:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="periodic", aliases=['element'])
    async def elements(self, ctx, *,  query=None):
        """Get Info About The Elements"""

        await ctx.message.delete()

        # Handle error if no search query was provided
        if query is None:
            return await ctx.invoke(self.bot.get_command('error'), err='Please provide a query!')

        # Check user input against the table's entries
        element = table.element(query)
        if element is None:
            return await ctx.invoke(self.bot.get_command('error'), err='This Element does not exist!')

        em = discord.Embed(color=self.bot.embed_colour)
        em.title = "\U0001f52c Periodic Table"
        em.add_field(name="Element", value=element.name)
        em.add_field(name="Symbol", value=element.symbol)
        em.add_field(name="Atomic Number", value=element.atomic)
        em.add_field(name="Mass", value=element.mass)

        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Elements(bot))

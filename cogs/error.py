import discord
from discord.ext import commands


class ErrorFormatter:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='error', hidden=True)
    async def error_formatter(self, ctx, delete_after=10.0, err: str=None, del_msg: discord.Message=None):
        """ Send a nice embed error with a message

        Usage:
        class Foo:
            def __init__(self, bot):
                self.bot = bot

            @commands.command()
            async def bar(self, ctx, *, baz):
                # some error happened
                await ctx.invoke(self.bot.get_command('error'),
                                 del_msg=ctx.message, delete_after=1.0,
                                 err='error message here')
        """
        if del_msg is not None:
            await del_msg.delete()

        em = discord.Embed(title=':x: Error', color=discord.Color.dark_red(), description=err)
        await ctx.send(embed=em, delete_after=delete_after)


def setup(bot):
    bot.add_cog(ErrorFormatter(bot))
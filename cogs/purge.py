import discord
from discord.ext import commands

# TODO: Rate limiting for more user-like deletion

class Purge:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['flush'])
    async def purge(self, ctx, num_msg: int):
        """ Remove a certain number of your messages """
        def check(message):
            return message.author.id == self.bot.user.id

        try:
            await ctx.channel.purge(check=check, limit=num_msg)
        except Exception as e:
            return await ctx.invoke(bot.get_command('error'), err=e)


def setup(bot):
    bot.add_cog(Purge(bot))
    

import discord
from discord.ext import commands


class Presence:
    def __init__(self, bot):
        self.bot = bot
        self.cmd = bot.get_command

    @commands.group(invoke_without_command=True, aliases=['pres'])
    async def presence(self, ctx, *, game_name: str=None):
        """ Change your discord presence
        Usage: provide a game name as a shortcut to presence game OR
        Provide no input and no subcommand to clear your playing status """
        if game_name is not None:
            return await ctx.invoke(self.cmd('presence game'), game_name=game_name)

        return await ctx.invoke(self.cmd('presence clear'))

    @presence.command(aliases=['g', 'play', 'playing'])
    async def game(self, ctx, *, game_name: str):
        """ Set your "playing" status

        This is redundant. You can shortcut by calling <prefix>presence <your game here> """
        await self.bot.change_presence(game=discord.Game(name=game_name))
        await ctx.message.edit(content="Changed presence!")

    @presence.group(aliases=['stream', 'streaming'])
    async def twitch(self, ctx, game_name: str, twitch_channel_name: str):
        """ Set your status to streaming with a twitch channel name
        NOTE: Your game name must be double-quoted if it is longer than 1 word with spaces """
        await self.bot.change_presence(game=discord.Game(name=game_name,
                                                         type=1,
                                                         url=f'https://www.twitch.tv/{twitch_channel_name}'))
        await ctx.message.edit(content="Changed to streaming!")

    @presence.command(aliases=['cls', 'clean', 'remove', 'rmv'])
    async def clear(self, ctx):
        """ Reset your status, game, and streaming URL """
        await self.bot.change_presence(game=discord.Game(name='', type=0, url=''))
        await ctx.message.edit(content="Presence cleared!")


def setup(bot):
    bot.add_cog(Presence(bot))

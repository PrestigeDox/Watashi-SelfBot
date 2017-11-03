import asyncio
import discord
import inspect
import os

from discord.ext import commands


class Base:
    def __init__(self, bot):
        self.bot = bot
        self.color = bot.user_color
        self.session = bot.aiohttp_session

    @commands.command(aliases=['pingpong'])
    async def ping(self, ctx):
        """ Pong! """
        ping_time = self.bot.latency * 1000
        emb = discord.Embed(title=f'\U0001f3d3 Pong {ping_time:.2f}ms', colour=self.color)
        await ctx.message.edit(content=None, embed=emb)

    @commands.command(aliases=['type'])
    async def typing(self, ctx, *, duration: float=10.0):
        """ Pretend that you're typing for a duration """
        await ctx.message.delete()

        async with ctx.channel.typing():
            await asyncio.sleep(duration)

    @commands.command(aliases=['emb'])
    async def embed(self, ctx, *, message: str=None):
        """ Create an embed """
        if message is None:
            return await ctx.error('You must add something to embed.')

        emb = discord.Embed(title=message, colour=self.color)
        await ctx.message.edit(content=None, embed=emb)

    @commands.command(name='custom_emojis', aliases=['emojis'])
    async def get_custom_emojis(self, ctx):
        """ Check All The Emojis On A Server """
        emojis = '\n'.join(['{1} `:{0}:`'.format(e.name, str(e)) for e in ctx.message.guild.emojis])

        if len(emojis) > 2000:
            return await ctx.error('Too many emojis to send!')
        if len(emojis) == 0:
            return await ctx.error('No custom emojis to display.')

        await ctx.message.edit(content=emojis)

    @commands.command(aliases=['logout', 'quit', 'exit'])
    async def exitbot(self, ctx):
        """ Close Watashi """
        emb = discord.Embed(title="Watashi Logging Out!", colour=self.color)
        await ctx.message.edit(embed=emb)
        await self.bot.logout()

    @commands.command()
    async def count(self, ctx, start: int, end: int):
        """ Count numbers from a given start point """
        for x in range(start, end + 1):
            await ctx.message.edit(content=x)
            await asyncio.sleep(1.2)

    @commands.command()
    async def source(self, ctx, *, command):
        """ Get The Source Code For Any Command """

        # Try to get the command by name, if it doesn't exist, AttributeError is actually called from trying to access
        # 'callback', which either way serves the purpose and an error is sent.
        try:
            cmd = self.bot.get_command(command).callback
        except AttributeError:
            return await ctx.error(f'Command `{command}` does not exist.')

        # If the command exists, getsourcelines returns a tuple with starting line and lines as a list
        # starting line number is taken as it is, and end_line is calculated by adding the length of all lines to
        # 'starting_line'.
        lines = inspect.getsourcelines(cmd)
        starting_line = lines[1]
        end_line = starting_line + len(lines[0])

        # 'os.path.basename', handles extracting filename regardless of operating system and the slashes used for paths.
        file = os.path.basename(inspect.getsourcefile(cmd))

        # Create Embed Response.
        emb = discord.Embed(colour=self.color)
        emb.add_field(name="Command", value=command.title(), inline=False)
        emb.add_field(name="Source", value='<https://github.com/PrestigeDox/Watashi-SelfBot/tree/master/cogs/'
                                           f'{file}#L{starting_line}-L{end_line}>', inline=False)

        return await ctx.message.edit(embed=emb)


def setup(bot):
    bot.add_cog(Base(bot))

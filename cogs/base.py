import asyncio
import discord
import inspect
from discord.ext import commands


class Base:
    def __init__(self, bot):
        self.bot = bot
        self.color = bot.user_color
        self.cmd = bot.get_command
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
            return await ctx.invoke(self.cmd('error'), err='You must add something to embed')

        emb = discord.Embed(title=message, colour=self.color)
        await ctx.message.edit(content=None, embed=emb)

    @commands.command(name='custom_emojis', aliases=['emojis'])
    async def get_custom_emojis(self, ctx):
        """ Check All The Emojis On A Server """

        await ctx.message.delete()

        emojis = '\n'.join(['{1} `:{0}:`'.format(e.name, str(e)) for e in ctx.message.guild.emojis])

        if len(emojis) > 2000:
            return await ctx.invoke(self.bot.get_command('error'), delete_after=2.0, err='Too many emojis!')

        await ctx.send(emojis)

    @commands.command(aliases=['logout', 'quit', 'exit'])
    async def exitbot(self, ctx):
        """ Close Watashi """
        await ctx.message.delete()

        emb = discord.Embed(title="Watashi Logging Out!", colour=self.color)
        await ctx.send(embed=emb)
        await self.bot.logout()

    @commands.command()
    async def count(self, ctx, start: int, amount: int):
        """ Count numbers from a given start point """
        await ctx.message.delete()

        for x in range(amount):
            await ctx.send(str(start))
            start += 1
            asyncio.sleep(2)

    @commands.command()
    async def source(self, ctx, *, command):
        """ Get The Source Code For Any Command """
        await ctx.message.delete()

        source = str(inspect.getsource(self.bot.get_command(command).callback))

        async with self.session.post("https://hastebin.com/documents", data=source) as resp:
            data = await resp.json()

        h_key = data['key']

        emb = discord.Embed(colour=self.color)
        emb.add_field(name="Command", value=command.upper(), inline=False)
        emb.add_field(name="Source", value=f'<https://hastebin.com/{h_key}.py>', inline=False)

        return await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Base(bot))

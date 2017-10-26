import asyncio
import discord
from discord.ext import commands
import inspect
import string


class Base:
    def __init__(self, bot):
        self.bot = bot
        self.color = bot.user_color
        self.session = bot.aiohttp_session
        self.cmd = bot.get_command

    @commands.command(aliases=['pingpong'])
    async def ping(self, ctx):
        """Pong!"""
        await ctx.message.delete()
        ping_time = self.bot.latency * 1000

        emb = discord.Embed(
            title=f'\U0001f3d3 Pong {ping_time:.2f}ms', colour=self.color)

        await ctx.send(embed=emb)

    @commands.command(aliases=['type'])
    async def typing(self, ctx, duration: float=10.0):
        """Pretend that you're always typing"""
        async with ctx.channel.typing():
            await asyncio.sleep(duration)

    @commands.command(aliases=['emb'])
    async def embed(self, ctx, *, message: str=None):
        """Create a basic embed"""
        if message is None:
            return await ctx.invoke(self.cmd('error'), err='You need a message to embed.', del_msg=ctx.message)

        else:
            await ctx.message.delete()
            emb = discord.Embed(title=message, colour=self.color)
            await ctx.send(embed=emb)

    @commands.command(aliases=['status'])
    async def presence(self, ctx, mode, *, message: str = None):
        """Change your status (Stream, Online...)"""

        change = 1

        if message == None:
            change = 0
            emb = discord.Embed(colour=self.color)
            emb.add_field(name='Options',
                          value='Stream, Online, Idle, DND or Invis')
            await ctx.send(embed=emb)

        else:
            if mode.lower() == "stream" or mode.lower() == "twitch":
                await self.bot.change_presence(status=discord.Status.online, game=discord.Game(name=message, type=1, url="https://www.twitch.tv/{}".format(message)), afk=True)
                colour = self.bot.colors.purple
                status = "Stream"
            elif mode.lower() == "online" or mode.lower() == "on":
                await self.bot.change_presence(status=discord.Status.online, game=discord.Game(name=message), afk=True)
                colour = self.bot.colors.lightgreen
                status = "Online"
            elif mode.lower() == "idle":
                await self.bot.change_presence(status=discord.Status.idle, game=discord.Game(name=message), afk=True)
                colour = self.bot.colors.orange
                status = "Idle"
            elif mode.lower() == "dnd" or mode.lower() == "disturb" or mode.lower() == "donotdisturb":
                await self.bot.change_presence(status=discord.Status.dnd, game=discord.Game(name=message), afk=True)
                colour = self.bot.colors.red
                status = "Do Not Disturb"
            elif mode.lower() == "invisible" or mode.lower() == "invis":
                await self.bot.change_presence(status=discord.Status.invisible, game=discord.Game(name=message), afk=True)
                colour = self.bot.colors.grey
                status = "Invisible"
            else:
                change = 0
                emb = discord.Embed(colour=self.color)
                emb.add_field(name='Options',
                              value='Stream, Online, Idle, DND or Invis')
                await ctx.send(embed=emb)

        if change == 1:
            emb = discord.Embed(colour=colour)
            emb.add_field(name='Status', value=status, inline=False)
            emb.add_field(name='Message', value=message, inline=False)
            await ctx.send(embed=emb)
        else:
            pass

    @commands.command()
    async def emojis(self, ctx):
        """Check All The Emojis On A Server"""
        await ctx.message.delete()
        try:
            await ctx.send('\n'.join(['{1} `:{0}:`'.format(e.name, str(e)) for e in ctx.message.guild.emojis]))
        except:
            await ctx.send("Too many emojis!")

    @commands.command(aliases=['logout', 'quit', 'exit'])
    async def exitbot(self, ctx):
        """Close Watashi"""
        await ctx.message.delete()
        emb = discord.Embed(title="Watashi Logging Out!", colour=self.color)
        await ctx.send(embed=emb)
        await self.bot.logout()

    @commands.command()
    async def count(self, ctx, startnumber: int, amount: int):
        await ctx.message.delete()
        start = startnumber
        for x in range(amount):
            await ctx.send(str(start))
            start = start + 1
            asyncio.sleep(2)

    @commands.command()
    async def source(self, ctx, *, command):
        """Get The Source Code For Any Command"""
        await ctx.message.delete()
        source = str(inspect.getsource(self.bot.get_command(command).callback))

        async with self.session.post("https://hastebin.com/documents", data=source) as resp:
            data = await resp.json()

        h_key = data['key']

        emb = discord.Embed(colour=self.color)
        emb.add_field(name="Command", value=string.capwords(
            command), inline=False)
        emb.add_field(
            name="Source", value=f'<https://hastebin.com/{h_key}.py>', inline=False)
        return await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Base(bot))

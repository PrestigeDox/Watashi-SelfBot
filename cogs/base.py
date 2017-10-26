import asyncio
import discord
import inspect
from discord.ext import commands


class Base:
    def __init__(self, bot):
        self.bot = bot
        self.color = bot.user_color
        self.session = bot.aiohttp_session

    @commands.command(aliases=['pingpong'])
    async def ping(self, ctx):
        """Pong!"""
        await ctx.message.delete()
        ping_time = self.bot.latency * 1000

        emb = discord.Embed(title=f'\U0001f3d3 Pong {ping_time:.2f}ms', colour=self.color)

        await ctx.send(embed=emb)

    @commands.command(aliases=['type'])
    async def typing(self, ctx, *, duration: float = None):
        """Pretend That Your Always Typing"""
        if not duration:
            duration = 10
        async with ctx.channel.typing():
            await asyncio.sleep(duration)
            return

    @commands.command(aliases=['emb'])
    async def embed(self, ctx, *, message: str = None):
        """Create A Basic Embed"""
        if message == None:
            await ctx.message.delete()
            await ctx.send(":x: You need a message to embed")
        else:
            await ctx.message.delete()
            emb = discord.Embed(title=message, colour=self.color)
            await ctx.send(embed=emb)

    @commands.command(aliases=['embadv', 'embadvanced', 'embedadv'])
    async def embedadvanced(self, ctx, *, msg: str = None):
        """Make An Advanced Embed"""
        if msg:
            if msg != '':
                ptext = title = description = image = thumbnail = color = footer = author = None
                timestamp = discord.Embed.Empty
                embed_values = msg.split('|')
                for i in embed_values:
                    if i.strip().lower().startswith('ptext='):
                        ptext = i.strip()[6:].strip()
                    elif i.strip().lower().startswith('title='):
                        title = i.strip()[6:].strip()
                    elif i.strip().lower().startswith('description='):
                        description = i.strip()[12:].strip()
                    elif i.strip().lower().startswith('desc='):
                        description = i.strip()[5:].strip()
                    elif i.strip().lower().startswith('image='):
                        image = i.strip()[6:].strip()
                    elif i.strip().lower().startswith('thumbnail='):
                        thumbnail = i.strip()[10:].strip()
                    elif i.strip().lower().startswith('colour='):
                        color = i.strip()[7:].strip()
                    elif i.strip().lower().startswith('color='):
                        color = i.strip()[6:].strip()
                    elif i.strip().lower().startswith('footer='):
                        footer = i.strip()[7:].strip()
                    elif i.strip().lower().startswith('author='):
                        author = i.strip()[7:].strip()
                    elif i.strip().lower().startswith('timestamp'):
                        timestamp = ctx.message.created_at
                    else:
                        if description is None and not i.strip().lower().startswith('field='):
                            description = i.strip()

                if color:
                    if color.startswith('#'):
                        color = color[1:]
                    if not color.startswith('0x'):
                        color = '0x' + color

                if ptext is title is description is image is thumbnail is color is footer is author is None and 'field=' not in msg:
                    await ctx.message.delete()
                    return await ctx.send(content=None,
                                                       embed=discord.Embed(description=msg))

                if color:
                    em = discord.Embed(timestamp=timestamp, title=title, description=description, color=int(color, 16))
                else:
                    em = discord.Embed(timestamp=timestamp, title=title, description=description)
                for i in embed_values:
                    if i.strip().lower().startswith('field='):
                        field_inline = True
                        field = i.strip().lstrip('field=')
                        field_name, field_value = field.split('value=')
                        if 'inline=' in field_value:
                            field_value, field_inline = field_value.split('inline=')
                            if 'false' in field_inline.lower() or 'no' in field_inline.lower():
                                field_inline = False
                        field_name = field_name.strip().lstrip('name=')
                        em.add_field(name=field_name, value=field_value.strip(), inline=field_inline)
                if author:
                    if 'icon=' in author:
                        text, icon = author.split('icon=')
                        if 'url=' in icon:
                            em.set_author(name=text.strip()[5:], icon_url=icon.split('url=')[0].strip(), url=icon.split('url=')[1].strip())
                        else:
                            em.set_author(name=text.strip()[5:], icon_url=icon)
                    else:
                        if 'url=' in author:
                            em.set_author(name=author.split('url=')[0].strip()[5:], url=author.split('url=')[1].strip())
                        else:
                            em.set_author(name=author)

                if image:
                    em.set_image(url=image)
                if thumbnail:
                    em.set_thumbnail(url=thumbnail)
                if footer:
                    if 'icon=' in footer:
                        text, icon = footer.split('icon=')
                        em.set_footer(text=text.strip()[5:], icon_url=icon)
                    else:
                        em.set_footer(text=footer)
                await ctx.send(content=ptext, embed=em)
        try:
            await ctx.message.delete()
        except:
            pass

    @commands.command(aliases=['status'])
    async def presence(self, ctx, mode, *, message: str = None):
        """Change your status (Stream, Online...)"""

        change = 1
        change2 = 1

        if mode.lower() == "none" or mode.lower() == "clear":
            await self.bot.change_presence(game=None, afk=True)
            emb = discord.Embed(colour=self.color)
            emb.add_field(name='Status', value="Presence has been cleared", inline=False)
            await ctx.send(embed=emb)
            change2 = 0
            pass
        if message == None:
            if change2 == 0:
                pass
            else:
                change = 0
                emb = discord.Embed(colour=self.color)
                emb.add_field(name='Options',
                              value='Stream, Online, Idle, DND or Invis')
                await ctx.send(embed=emb)

        else:
            if mode.lower() == "stream" or mode.lower() == "twitch":
                await self.bot.change_presence(status=discord.Status.online, game=discord.Game(name=message, type=1, url="https://www.twitch.tv/{}".format(message)), afk=True)
                colour = 0xBF55EC
                status = "Stream"
            elif mode.lower() == "online" or mode.lower() == "on":
                await self.bot.change_presence(status=discord.Status.online, game=discord.Game(name=message), afk=True)
                colour = 0x00ff00
                status = "Online"
            elif mode.lower() == "idle":
                await self.bot.change_presence(status=discord.Status.idle, game=discord.Game(name=message), afk=True)
                colour = 0xff9900
                status = "Idle"
            elif mode.lower() == "dnd" or mode.lower() == "disturb" or mode.lower() == "donotdisturb":
                await self.bot.change_presence(status=discord.Status.dnd, game=discord.Game(name=message), afk=True)
                colour = 0xff0f00
                status = "Do Not Disturb"
            elif mode.lower() == "invisible" or mode.lower() == "invis":
                await self.bot.change_presence(status=discord.Status.invisible, game=discord.Game(name=message), afk=True)
                colour = 0xB0B0B0
                status = "Invisible"
            else:
                change = 0
                emb = discord.Embed(colour=self.color)
                emb.add_field(name='Options',
                              value='Stream, Online, Idle, DND or Invis')
                await ctx.send(embed=emb)

        if change == 1:
            emb = discord.Embed(colour=self.color)
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
    async def count(self, ctx, start: int, amount: int):
        await ctx.message.delete()
        for x in range(amount):
            await ctx.send(str(start))
            start += 1
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
        emb.add_field(name="Command", value=command.upper(), inline=False)
        emb.add_field(name="Source", value=f'<https://hastebin.com/{h_key}.py>', inline=False)
        return await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Base(bot))

import discord
from discord.ext import commands
import time


class Base:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['pingpong'])
    async def ping(self, ctx):
        await ctx.message.delete()
        pingtime = self.bot.latency * 1000
        pingtimerounded = int(pingtime)
        totalstring = str(pingtimerounded) + 'ms'
        emb = discord.Embed(title='\U0001f3d3 Pong ' +
                            totalstring, colour=self.bot.embed_colour)
        await ctx.send(embed=emb)

    @commands.command(aliases=['emb'])
    async def embed(self, ctx, *, message: str = None):
        if message == None:
            await ctx.message.delete()
            await ctx.send(":x: You need a message to embed")
        else:
            await ctx.message.delete()
            emb = discord.Embed(title=message, colour=self.bot.embed_colour)
            await ctx.send(embed=emb)

    @commands.command(aliases=['embadv', 'embadvanced', 'embedadv'])
    async def embedadvanced(self, ctx, *, msg: str = None):
        '''
        Code through this project has all been made by our dev team.
        This section of code was taken from another bot and then edited and,
        improved to work with Watashi. We than the creators of Appus bot
        Who I got permission from to use this code. I'm lazy af so cba
        to make my own version so just edited theirs ; )
        '''
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

        change = 1

        if message == None:
            change = 0
            emb = discord.Embed(colour=self.bot.embed_colour)
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
                emb = discord.Embed(colour=self.bot.embed_colour)
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
        await ctx.message.delete()
        try:
            await ctx.send('\n'.join(['{1} `:{0}:`'.format(e.name, str(e)) for e in ctx.message.guild.emojis]))
        except:
            await ctx.send("Too many emojis!")

    @commands.command(aliases=['logout', 'quit', 'exit'])
    async def exitbot(self, ctx):
        await ctx.message.delete()
        emb = discord.Embed(title="Watashi Logging Out!", colour=self.bot.embed_colour)
        await ctx.send(embed=emb)
        await self.bot.logout()

    @commands.command()
    async def count(self, ctx, startnumber: int, amount: int):
        await ctx.message.delete()
        start = startnumber
        for x in range(amount):
            await ctx.send(str(start))
            start = start + 1
            time.sleep(1)

def setup(bot):
    bot.add_cog(Base(bot))

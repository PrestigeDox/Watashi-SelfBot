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
        await ctx.message.edit(content=f'\U0001f3d3 Pong {ping_time:.2f}ms')

    @commands.command(aliases=['type'])
    async def typing(self, ctx, *, duration: float=10.0):
        """ Pretend that you're typing for a duration """
        await ctx.message.delete()

        async with ctx.channel.typing():
            await asyncio.sleep(duration)

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
        await ctx.message.edit("Watashi Logging Out!")
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

        return await ctx.message.edit(f'{command.title()}\n<https://github.com/PrestigeDox/Watashi-SelfBot/tree'
                                      f'/master/cogs/{file}#L{starting_line}-L{end_line}>')

    @commands.group(invoke_without_command=True)
    async def quote(self, ctx, message_id: int = None, *, reply: str = None):
        """ Quote a message by using its ID """

        # Check for message_id, if it wasn't passed, return
        if message_id is None:
            return await ctx.error('Provide a message id please')

        # Just for the sake of good UX, im giving each error its own except block and message
        try:
            # Credit to Spy for this, its quite clever
            obj = discord.Object(id=message_id + 1)
            async for mess in ctx.channel.history(limit=1, before=obj):
                if mess.id == message_id:
                    message = mess
                else:
                    return await ctx.error("Message doesn't exist")
        except discord.NotFound:
            return await ctx.error("Message doesn't exist")
        except discord.Forbidden:
            return await ctx.error("You do not have the permissions to request this message")
        except discord.HTTPException:
            return await ctx.error("Couldn't retrieve the message")

        # DMChannel doesn't have a name attr, not doing any fancy ternary op, its already messy
        if not isinstance(ctx.channel, discord.DMChannel):
            at = f'#{ctx.channel.name} | {message.created_at.strftime("%a, %d %b %Y at %I:%M%p")}'
        else:
            at = f'{message.created_at.strftime("%a, %d %b %Y at %I:%M%p")}'
        await ctx.message.delete()

        head = f"**{message.author.display_name}#{message.author.discriminator}** - *{at}*"

        await ctx.message.edit(conent=f'{head}\n{message.content}')

        # Optional reply
        if reply is not None:
            await ctx.send(reply)

    @quote.command(name='fake')
    async def fake(self, ctx, message_id: int = None, *, fake_text: str = None):
        """ Make a fake quote with custom text referring to a real message by ID """
        # Check for message_id, if it wasn't passed, return
        if message_id is None:
            return await ctx.error('Provide a message id please')

        # Fake quote needs fake text, if you didn't provide it why were you using this
        if fake_text is None:
            return await ctx.error('Provide text to substitute please')

        # Just for the sake of good UX, im giving each error its own except block and message
        try:
            # Credit to Spy for this, its quite clever
            obj = discord.Object(id=message_id + 1)
            async for mess in ctx.channel.history(limit=1, before=obj):
                if mess.id == message_id:
                    message = mess
                else:
                    return await ctx.error("Message doesn't exist")
        except discord.NotFound:
            return await ctx.error("Message doesn't exist")
        except discord.Forbidden:
            return await ctx.error("You do not have the permissions to request this message")
        except discord.HTTPException:
            return await ctx.error("Couldn't retrieve the message")

        # DMChannel doesn't have a name attr, not doing any fancy ternary op, its already messy
        if not isinstance(ctx.channel, discord.DMChannel):
            at = f'#{ctx.channel.name} | {message.created_at.strftime("%a, %d %b %Y at %I:%M%p")}'
        else:
            at = f'{message.created_at.strftime("%a, %d %b %Y at %I:%M%p")}'
        await ctx.message.delete()

        head = f"**{message.author.display_name}#{message.author.discriminator}** - *{at}*"

        await ctx.message.edit(content=f'{head}\n{fake_text}')


def setup(bot):
    bot.add_cog(Base(bot))

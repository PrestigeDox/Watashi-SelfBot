import discord
from discord.ext import commands
import asyncio

class Animate:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, aliases=['anim'])
    async def animate(self, ctx, *, file):
        """Animated Text Files onto Discord"""
        try:
            with open(f'animations/{file}.txt') as a:
                anim = a.read().splitlines()
        except FileNotFoundError:
            return await ctx.send('File not found.')
        except IOError:
            return await ctx.send('Cannot open file.')

        interval = anim[0]
        for line in anim[1:]:
            await ctx.message.edit(content=line)
            await asyncio.sleep(float(interval))


def setup(bot):
    bot.add_cog(Animate(bot))

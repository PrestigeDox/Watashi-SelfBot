import asyncio
from discord.ext import commands


class Animate:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['anim'])
    async def animate(self, ctx, *, file):
        """ Animate Text Files onto Discord """
        try:
            with open(f'animations/{file}.txt') as a:
                anim = a.read().splitlines()
        except FileNotFoundError:
            return await ctx.error('File not found.')
        except IOError:
            return await ctx.error('Cannot open file.')

        interval = anim[0]
        for line in anim[1:]:
            await ctx.message.edit(content=line)
            await asyncio.sleep(float(interval))


def setup(bot):
    bot.add_cog(Animate(bot))

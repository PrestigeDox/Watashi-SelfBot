#!/bin/env python
import asyncio
from discord.ext import commands


class Clean:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['clear'])
    async def clean(self, ctx, *, limit: int = 30):
        await ctx.message.delete()
        async for msg in ctx.channel.history(limit=limit, before=ctx.message):
            if msg.author == self.bot.user:
                await msg.delete()
                await asyncio.sleep(1.2)

def setup(bot):
    bot.add_cog(Clean(bot))

#!/bin/env python
import asyncio
from discord.ext import commands


class Clean:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['clear'])
    async def clean(self, ctx, *, limit = None):
    	await ctx.message.delete()
        if not limit:
            limit = 30
        async for msg in ctx.channel.history(limit=limit, before=ctx.message):
        	if msg.author == self.bot.user:
        		await msg.delete()
        		await asyncio.sleep(1.2)


def setup(bot):
    bot.add_cog(Clean(bot))

import discord
from discord.ext import commands


class WatashiContext(commands.Context):
    async def error(self, err: str, delete_after: float=5.0):
        em = discord.Embed(title=':x: Error',
                           color=discord.Color.dark_red(),
                           description=err.format())

        await self.message.edit(embed=em, delete_after=delete_after)

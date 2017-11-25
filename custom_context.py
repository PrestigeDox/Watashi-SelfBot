import discord
from discord.ext import commands


class WatashiContext(commands.Context):
    async def error(self, err: str, delete_after: float=5.0):
        await self.message.edit(f":x: Error!\n{err.format()}", delete_after=delete_after)

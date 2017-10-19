import discord
from discord.ext import commands
import pyfiglet

class Figlet:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['ascii', 'fig', 'asc'])
    async def figlet(self, ctx, *, message: str):
        await ctx.message.delete()
        try:
            await ctx.send(f'```http\n{pyfiglet.figlet_format(message)}```')
        except discord.HTTPException:
            emb = discord.Embed(colour=self.bot.red)
            emb.add_field(name=":x: Error", value="Message is too large")
            await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(Figlet(bot))
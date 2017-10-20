import discord
from discord.ext import commands
from urllib.request import urlopen


class TinyURL:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tinyurl(self, ctx, link: str = None):
        await ctx.message.delete()
        if str == None:
            await ctx.send("Retard add a link")
        else:
            apitiny = 'http://tinyurl.com/api-create.php?url='
            shortenurl = urlopen(apitiny + link).read().decode("utf-8")
            emb = discord.Embed(colour=self.bot.embed_colour)
            emb.add_field(name="Original Link", value=link, inline=False)
            emb.add_field(name="Shortened Link", value=shortenurl, inline=False)
            await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(TinyURL(bot))
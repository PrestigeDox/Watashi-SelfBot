import discord
from discord.ext import commands
import unicodedata


class Coding:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['python'])
    async def py(self, ctx, *, code: str):
        await ctx.message.delete()
        await ctx.send("```py\n{}```".format(code))

    @commands.command()
    async def css(self, ctx, *, code: str):
        await ctx.message.delete()
        await ctx.send("```css\n{}```".format(code))

    @commands.command(aliases=['html5'])
    async def html(self, ctx, *, code: str):
        await ctx.message.delete()
        await ctx.send("```html\n{}```".format(code))

    @commands.command()
    async def ini(self, ctx, *, code: str):
        await ctx.message.delete()
        await ctx.send("```ini\n{}```".format(code))


    @commands.command()
    async def c(self, ctx, *, code: str):
        await ctx.message.delete()
        await ctx.send("```c\n{}```".format(code))

    @commands.command()
    async def codeblock(self, ctx, *, code: str):
        await ctx.message.delete()
        await ctx.send("```\n{}```".format(code))

    @commands.command(aliases=['onecodeblock'])
    async def linecodeblock(self, ctx, *, code: str):
        await ctx.message.delete()
        await ctx.send("``\n{}```".format(code))

    @commands.command()
    async def charinfo(self, ctx, *, characters: str):
        await ctx.message.delete()
        if len(characters) > 25:
            return await ctx.send(f'Too many characters ({len(characters)}/25)')

        digit = f'{ord(characters):x}'
        name = unicodedata.name(characters, 'Name not found.')
        
        emb = discord.Embed(colour=self.bot.embed_colour)
        emb.set_author(name="Charinfo For {}".format(characters))
        emb.add_field(name="Name", value=name, inline=False)
        emb.add_field(name="Char", value=f'\\U{digit:>08}', inline=False)
        emb.add_field(name="Link", value=f'<http://www.fileformat.info/info/unicode/char/{digit}>')
        await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(Coding(bot))

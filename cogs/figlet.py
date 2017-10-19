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
            emb.add_field(name=":x: Error", value="Message is too large!")
            await ctx.send(embed=emb)

    @commands.command(aliases=['asciislant', 'figslant', 'ascslant'])
    async def figletslant(self, ctx, *, message: str):
        await ctx.message.delete()
        f = pyfiglet.Figlet(font='slant')
        try:
            await ctx.send(f'```http\n{f.renderText(message)}```')
        except discord.HTTPException:
            emb = discord.Embed(colour=self.bot.red)
            emb.add_field(name=":x: Error", value="Message is too large!")
            await ctx.send(embed=emb)

    @commands.command(aliases=['asciibulbhead', 'figbulbhead', 'ascbulbhead'])
    async def figletbulbhead(self, ctx, *, message: str):
        await ctx.message.delete()
        f = pyfiglet.Figlet(font='bulbhead')
        try:
            await ctx.send(f'```http\n{f.renderText(message)}```')
        except discord.HTTPException:
            emb = discord.Embed(colour=self.bot.red)
            emb.add_field(name=":x: Error", value="Message is too large!")
            await ctx.send(embed=emb)

    @commands.command(aliases=['ascii3d', 'fig3d', 'asc3d'])
    async def figlet3d(self, ctx, *, message: str):
        await ctx.message.delete()
        f = pyfiglet.Figlet(font='larry3d')
        try:
            await ctx.send(f'```http\n{f.renderText(message)}```')
        except discord.HTTPException:
            emb = discord.Embed(colour=self.bot.red)
            emb.add_field(name=":x: Error", value="Message is too large!")
            await ctx.send(embed=emb)

    @commands.command(aliases=['asciirectangle', 'figrectangle', 'ascrectangle'])
    async def figletrectangle(self, ctx, *, message: str):
        await ctx.message.delete()
        f = pyfiglet.Figlet(font='rectangles')
        try:
            await ctx.send(f'```http\n{f.renderText(message)}```')
        except discord.HTTPException:
            emb = discord.Embed(colour=self.bot.red)
            emb.add_field(name=":x: Error", value="Message is too large!")
            await ctx.send(embed=emb)

    @commands.command(aliases=['asciiscript', 'figscript', 'ascscript'])
    async def figletscript(self, ctx, *, message: str):
        await ctx.message.delete()
        f = pyfiglet.Figlet(font='slscript')
        try:
            await ctx.send(f'```http\n{f.renderText(message)}```')
        except discord.HTTPException:
            emb = discord.Embed(colour=self.bot.red)
            emb.add_field(name=":x: Error", value="Message is too large!")
            await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(Figlet(bot))
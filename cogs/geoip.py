import asyncio
import discord
from discord.ext import commands
import inspect
import aiohttp

class Geoip:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['geolocate', 'iptogeo', 'iptolocation', 'ip2geo', 'ip'])
    async def geoip(self, ctx, *, ipaddr: str = "1.3.3.7"):
        await ctx.message.delete()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://freegeoip.net/json/{ipaddr}') as resp:
                data = await resp.json()
            emb = discord.Embed(colour=self.bot.embed_colour)
            emb.add_field(name="IP", value=data['ip'], inline=True)
            emb.add_field(name="Country", value=data['country_name'], inline=True)
            emb.add_field(name="Country Code", value=data['country_code'], inline=True)
            emb.add_field(name="Region Name", value=data['region_name'], inline=True)
            emb.add_field(name="Region Code", value=data['region_code'], inline=True)
            emb.add_field(name="City", value=data['city'], inline=True)
            emb.add_field(name="Zip Code", value=data['zip_code'], inline=True)
            emb.add_field(name="Time Zone", value=data['time_zone'], inline=True)
            emb.add_field(name="Latitude", value=data['latitude'], inline=True)
            emb.add_field(name="Longitude", value=data['longitude'], inline=True)
            return await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(Geoip(bot))
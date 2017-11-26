import discord
from discord.ext import commands


class Geoip:
    def __init__(self, bot):
        self.bot = bot
        self.session = bot.aiohttp_session
        self.color = bot.user_color

    @commands.command(aliases=['geolocate', 'iptogeo', 'iptolocation', 'ip2geo', 'ip'])
    async def geoip(self, ctx, *, ipaddr: str = "1.3.3.7"):
        """ Convert an IP/URL to a GeoLocation """
        try:
            async with self.session.get(f'https://freegeoip.net/json/{ipaddr}') as resp:
                data = await resp.json()
        except:
            return await ctx.error('Could not get information on IP or website address.')

        # Create embed
        em = discord.Embed(color=self.color)

        # Fields which may be potentially empty
        fields = [
            {'name': 'IP', 'value': data['ip']},
            {'name': 'Country', 'value': data['country_name']},
            {'name': 'Country Code', 'value': data['country_code']},
            {'name': 'Region Name', 'value': data['region_name']},
            {'name': 'Region Code', 'value': data['region_code']},
            {'name': 'City', 'value': data['city']},
            {'name': 'Zip Code', 'value': data['zip_code']},
            {'name': 'Time Zone', 'value': data['time_zone']},
            {'name': 'Latitude', 'value': data['latitude']},
            {'name': 'Longitude', 'value': data['longitude']}
        ]

        msg = str()
        # Only add fields which are actually filled
        for field in fields:
            if field['value']:
                msg += f"**{field['name']}:** {field['value']}"

        return await ctx.message.edit(content=msg)


def setup(bot):
    bot.add_cog(Geoip(bot))

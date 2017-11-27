import discord
import datetime
from discord.ext import commands


class Info:
    def __init__(self, bot):
        self.bot = bot
        self.cmd = bot.get_command
        self.color = bot.user_color

    @commands.command()
    async def whois(self, ctx, member: discord.Member = None):
        """ Get Info On A Member """
        if member is None:
            member = ctx.guild.get_member(ctx.author.id)

        msg = f"Whois for *{member.display_name}*\n"
        msg += f"**Roles:**\n{', '.join([f'`{r.name}`' for r in member.roles])}\n"
        msg += f"**Status:**\n" f"**Playing** {member.game.name if member.game else ''}\n"
        msg += f"**Color:**\n{str(member.color)}\n"
        msg += f"**Joined on:**\n{member.joined_at.date()}\n"
        msg += f"**Avatar url:**\n{member.avatar_url}"

        try:
            await ctx.message.edit(content=msg)
        except discord.HTTPException:
            await ctx.error('Too much information to send.')

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        """ Get A Member's Avatar """
        await ctx.message.edit(content=f"{member.avatar_url if member else ctx.author.avatar_url}")

    @commands.command(aliases=['about', 'selfbot', 'bot'])
    async def info(self, ctx):
        """ Get Info/Statistics On The Bot """

        github = 'https://github.com/PrestigeDox/Watashi-SelfBot'
        discord_link = '<https://discord.gg/JAcAEU5>'

        pingtime = int(self.bot.latency * 1000)

        # Get member stats
        total_members = sum(1 for _ in self.bot.get_all_members())
        online_members = len({m.id for m in self.bot.get_all_members()
                              if m.status is discord.Status.online})
        unique_members = len(self.bot.users)

        # Get channel stats
        voice_channels = []
        text_channels = []
        for guild in self.bot.guilds:
            voice_channels.extend(guild.voice_channels)
            text_channels.extend(guild.text_channels)
        dm_channels = self.bot.private_channels

        # Prettily format the uptime
        uptime = (datetime.datetime.now() - self.bot.starttime)
        hours, rem = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(rem, 60)
        days, hours = divmod(hours, 24)

        # Create the embed
        msg = "**Watashi SelfBot**\n"
        msg += "Watashi Selfbot was made to enhance the experience of "\
               "Discord users who wanted to speed up daily processes. Watashi has a multitude of commands "\
               "which you can use and we regularly update the bot to add more commands and improve existing "\
               "commands! Make sure to join our Discord server to keep up with Watashi related announcements!\n"

        msg += "**Uptime \U0001f550:** "\
               f'{days}D {hours}H {minutes}M {seconds}S\n'
        msg += "**Ping Time \U0001f3d3:**  " f'{pingtime}ms\n'

        msg += f"**Servers \U00002694:**  {len(self.bot.guilds)}\n"

        msg += f"**Cogs \U00002699:**  {len(self.bot.cogs)}\n"
        msg += f"**Commands \U0001f50e:**  {len(self.bot.commands)}\n"
        msg += f"**GitHub \U0001f516:**\n{github}\n"
        msg += f"**Discord \U0001f47e:**\n{discord_link}\n"
        await ctx.message.edit(content=msg)

def setup(bot):
    bot.add_cog(Info(bot))

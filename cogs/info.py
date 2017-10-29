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
            memberholder = ctx.message.author.id
            member = ctx.guild.get_member(memberholder)
            emb = discord.Embed(colour=self.color)
            emb.set_author(name="Whois for {}".format(member.display_name),
                           icon_url=member.avatar_url)
            emb.set_thumbnail(url=member.avatar_url)
            emb.add_field(name="**ID**", value=member.id)
            emb.add_field(name="**Roles**",
                          value=", ".join([r.name for r in member.roles]))
            emb.add_field(
                name="**Status**", value="**Playing** {}".format(member.game.name if member.game else ""))
            emb.add_field(name="**Color**", value=str(member.color))
            emb.add_field(name="**Joined on**", value=member.joined_at.date())
            emb.add_field(name="**Avatar url**",
                          value="[Here]({})".format(member.avatar_url))
        else:
            emb = discord.Embed(colour=self.color)
            emb.set_author(name="Whois for {}".format(member.display_name),
                           icon_url=member.avatar_url)
            emb.set_thumbnail(url=member.avatar_url)
            emb.add_field(name="**ID**", value=member.id)
            emb.add_field(name="**Roles**",
                          value=", ".join([r.name for r in member.roles]))
            emb.add_field(
                name="**Status**", value="**Playing** {}".format(member.game.name if member.game else ""))
            emb.add_field(name="**Color**", value=str(member.color))
            emb.add_field(name="**Joined on**", value=member.joined_at.date())
            emb.add_field(name="**Avatar url**",
                          value="[Here]({})".format(member.avatar_url))
        try:
            await ctx.send(embed=emb)
        except discord.HTTPException:
            await ctx.invoke(self.cmd('error'), err='Too much information to send.')

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        """ Get A Member's Avatar """
        await ctx.message.delete()
        emb = discord.Embed(colour=self.color)
        emb.set_author(name="Avatar for {}".format(member.display_name),
                       icon_url=member.avatar_url)
        emb.add_field(name="**Avatar url**",
                      value="[Here]({})".format(member.avatar_url))
        emb.set_thumbnail(url=member.avatar_url)

        await ctx.send(embed=emb)

    @commands.command(aliases=['about', 'selfbot', 'bot'])
    async def info(self, ctx):
        """ Get Info/Statistics On The Bot """

        github = '[Click Here](https://github.com/PrestigeDox/Watashi-SelfBot)'
        discord_link = '[Click Here](https://discord.gg/JAcAEU5)'

        pingtime = int(self.bot.latency * 1000)

        users = 0
        for i in self.bot.get_all_members():
            users = users + 1

        memberstot = sum(1 for _ in self.bot.get_all_members())
        memberson = len({m.id for m in self.bot.get_all_members()
                         if m.status is discord.Status.online})
        membersuni = len(self.bot.users)

        voice_channels = []
        text_channels = []
        for guild in self.bot.guilds:
            voice_channels.extend(guild.voice_channels)
            text_channels.extend(guild.text_channels)
        textchannels = len(text_channels)
        voicechannels = len(voice_channels)
        dmchannels = len(self.bot.private_channels)

        uptime = (datetime.datetime.now() - self.bot.starttime)
        hours, rem = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(rem, 60)
        days, hours = divmod(hours, 24)

        currentstatus = str(ctx.author.status).title()

        emb = discord.Embed(colour=self.color)
        emb.set_author(name="Watashi SelfBot", icon_url=ctx.author.avatar_url)
        emb.add_field(name="About", value="Watashi Selfbot was made to enhance the experience of "
                      "Discord users who wanted to speed up daily processes. Watashi has a multitude of commands "
                      "which you can use and we regularly update the bot to add more commands and improve existing "
                      "commands! Make sure to join our Discord server to keep up with Watashi related announcements!",
                      inline=False)
        emb.add_field(name="Uptime \U0001f550",
                      value=f'{days}D {hours}H {minutes}M {seconds}S', inline=True)
        emb.add_field(name="Ping Time \U0001f3d3",
                      value=f'{pingtime}ms', inline=True)
        emb.add_field(name="Servers \U00002694",
                      value=len(self.bot.guilds), inline=True)
        emb.add_field(name="Users \U0001f476",
                      value=f'Total: {memberstot}\nUnique: {membersuni}\nOnline: {memberson}', inline=True)
        emb.add_field(name="Channels \U00002328",
                      value=f'Text: {textchannels}\nVoice: {voicechannels}\nDM: {dmchannels}', inline=True)
        emb.add_field(name="Status \U0001f47e",
                      value=f'Presence: {currentstatus}\nPlaying: {ctx.author.game}', inline=True)
        emb.add_field(name="Cogs \U00002699",
                      value=len(self.bot.cogs), inline=True)
        emb.add_field(name="Commands \U0001f50e",
                      value=len(self.bot.commands), inline=True)
        emb.add_field(name="GitHub \U0001f516", value=github, inline=True)
        emb.add_field(name="Discord \U0001f47e",
                      value=discord_link, inline=True)

        await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Info(bot))

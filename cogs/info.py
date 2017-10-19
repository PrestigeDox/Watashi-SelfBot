import discord
from discord.ext import commands


class Info:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def whois(self, ctx, member: discord.Member = None):
        if member == None:
            memberholder = ctx.message.author.id
            member = ctx.guild.get_member(memberholder)
            emb = discord.Embed(colour=self.bot.embed_colour)
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
            emb = discord.Embed(colour=self.bot.embed_colour)
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
        except:
            await ctx.send("Too much info...")

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        await ctx.message.delete()
        emb = discord.Embed(colour=self.bot.embed_colour)
        emb.set_author(name="Avatar for {}".format(member.display_name),
                           icon_url=member.avatar_url)
        emb.add_field(name="**Avatar url**",
                          value="[Here]({})".format(member.avatar_url))
        emb.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=emb)

    @commands.command(aliases=['about', 'selfbot', 'bot'])
    async def info(self, ctx):

        github = '[Click Here](https://github.com/PrestigeDox/Watashi-SelfBot)'
        discord = '[Click Here](https://discord.gg/JAcAEU5)'

        await ctx.message.delete()
        emb = discord.Embed(colour=self.bot.embed_colour)
        emb.set_author(name="Watashi SelfBot", icon_url=member.avatar_url)
        emb.add_field(name="About", value="Bot Description", inline=False)
        emb.add_field(name="Uptime", value="Time Here", inline=False)
        emb.add_field(name="Ping Time", value="Ping Time", inline=True)
        emb.add_field(name="Users", value="Users Between Servers", inline=True)
        emb.add_field(name="Servers", value="Servers your in", inline=True)
        emb.add_field(name="Text Channels", value="Amount of Text Channels", inline=True)
        emb.add_field(name="Voice Channels", value="Amount of Voice Channels", inline=True)
        emb.add_field(name="Presence", value="Your Presence", inline=True)
        emb.add_field(name="Playing", value="What Your Playing", inline=True)
        emb.add_field(name="GitHub", value=github, inline=True)
        emb.add_field(name="Discord", value=discord, inline=True)
        await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(Info(bot))

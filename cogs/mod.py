import discord
from discord.ext import commands


# This bit allows you to more easily unban members via ID or name#discrim
# Taken mostly from R. Danny
# https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/mod.py#L83-L94
class BannedMember(commands.Converter):
    async def convert(self, ctx, arg):
        bans = await ctx.guild.bans()

        try:
            member_id = int(arg)
            user = discord.utils.find(lambda u: u.user.id == member_id, bans)
        except ValueError:
            user = discord.utils.find(lambda u: str(u.user) == arg, bans)

        if user is None:
            return None

        return user


class Mod:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['k'])
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """ Kick a member from the server """
        try:
            await ctx.guild.kick(member, reason=reason)
        except commands.errors.BadArgument:
            return await ctx.error('User not found.')

        await ctx.message.edit(content=f'Member `{member}` kicked.\nReason: `{reason}`.')

    @commands.command(aliases=['kb'])
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """ Ban a member from the server """
        try:
            await ctx.guild.ban(member, reason=reason, delete_message_days=0)
        except commands.errors.BadArgument:
            return await ctx.error('User not found.')

        await ctx.message.edit(content=f'Member `{member}` banned.\nReason: `{reason}`.')

    @commands.command(aliases=['ub'])
    async def unban(self, ctx, member: BannedMember, *, reason=None):
        """ Unban a member from the server
        Since you can't highlight them anymore use their name#discrim or ID """
        try:
            await ctx.guild.unban(member.user, reason=reason)
        except AttributeError:
            return await ctx.error('User not presently banned.')

        await ctx.message.edit(content=f'Member `{member.user}` unbanned.\nReason: `{reason}`.')


def setup(bot):
    bot.add_cog(Mod(bot))

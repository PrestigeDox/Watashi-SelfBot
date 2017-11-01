import discord
import random
from discord.ext import commands


class Games:
    def __init__(self, bot):
        self.bot = bot
        self.color = bot.user_color
        self.eight_responses = [
            'It is certain.',
            'It is decidedly so.',
            'Without a doubt.',
            'Yes definitely.',
            'You may rely on it.',
            'As I see it, yes.',
            'Most likely.',
            'Outlook good.',
            'Yes.',
            'Signs point to yes.',
            'Reply hazy try again.',
            'Ask again later.',
            'Better not tell you now.',
            'Cannot predict now.',
            'Concentrate and ask again.',
            "Don't count on it.",
            'My reply is no.',
            'My sources say no.',
            'Outlook not so good.',
            'Very doubtful.'
        ]
        self.coins = ["Heads", "Tails"]

    @commands.command(name="8ball")
    async def eight_ball(self, ctx, *, query: str):
        """ Let the mystical 8ball evaluate your question """
        emb = discord.Embed(title=':8ball: Magic 8ball', colour=0x00080A)
        emb.add_field(name="Question", value=query)
        emb.add_field(name="Reply", value=random.choice(self.eight_responses), inline=False)
        await ctx.message.edit(embed=emb, content=None)

    @commands.command(name="flip", aliases=["coinflip"])
    async def coin_flip(self, ctx):
        """ Toss a coin """
        result = random.randint(0, 1)

        emb = discord.Embed( title='Coin Flip', description=self.coins[result], colour=self.color)
        emb.set_thumbnail(url="http://researchmaniacs.com/Random/Images/Quarter-Tails.png" if result else "http://researchmaniacs.com/Random/Images/Quarter-Heads.png")
        await ctx.message.edit(embed=emb, content=None)

    @commands.command(aliases=["choice"])
    async def choose(self, ctx, *, query: str):
        """ Let the bot choose between multiple options! """
        choice = random.choice(query.split('|'))
        emb = discord.Embed(title=":round_pushpin: Choices", colour=self.color)
        emb.add_field(name="Choice between", value=query.replace('|', ' or '))
        emb.add_field(name="Result", value=choice, inline=False)

        await ctx.message.edit(embed=emb, content=None)


def setup(bot):
    bot.add_cog(Games(bot))

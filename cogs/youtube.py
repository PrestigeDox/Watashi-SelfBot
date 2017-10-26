import discord
from discord.ext import commands
from bs4 import BeautifulSoup


class Youtube:
    def __init__(self, bot):
        self.bot = bot
        self.uri = 'https://youtube.com/results'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 '
                                      '(KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

    @staticmethod
    def get_yt_items(html: str) -> list:
        """ Little wrapper for the bs4 stuff """
        soup = BeautifulSoup(html, 'lxml')

        # The super long class def'n here is required to only catch videos, and not users / channels
        return [(x.text, f"https://youtube.com{x['href']}")
                for x in soup.find_all('a', {'class': 'yt-uix-tile-link '
                                                      'yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link '})]

    @commands.command(aliases=['yt'])
    async def youtube(self, ctx, *, query: str):
        """ Search for a few youtube videos """
        async with self.bot.aiohttp_session.get(self.uri,
                                                headers=self.headers,
                                                params={'search_query': query.replace(' ', '+')}) as r:
            html = await r.text()

        items = self.get_yt_items(html)

        if len(items) == 0:
            return await ctx.invoke(self.bot.get_command('error'), err=f'No YouTube videos found for `{query}`.')

        # Create a neat embed
        em = discord.Embed(color=discord.Color.dark_red())
        em.set_author(name="YouTube Search",
                      icon_url="https://www.seeklogo.net/wp-content/uploads/2016/06/YouTube-icon.png")

        em.add_field(name='Results', value='\n'.join(
            f'{idx + 1}. [{x[0]}]({x[1]})' for idx, x in enumerate(items[:5])))

        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Youtube(bot))

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
            return await ctx.error(f'No YouTube videos found for `{query}`.')

        msg = f"Results\n" + '\n'.join(f'{idx + 1}. {x[0]} - <{x[1]}>' for idx, x in enumerate(items[:5]))

        await ctx.message.edit(content=msg)


def setup(bot):
    bot.add_cog(Youtube(bot))

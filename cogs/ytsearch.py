import discord
import functools
import youtube_dl

from discord.ext import commands


class YoutubeSearch:
    def __init__(self, bot):
        self.bot = bot
        self.options = {
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0'
        }
        self.ytdl = youtube_dl.YoutubeDL(self.options)

    @commands.command(name="ytsearch", aliases=['yt'])
    async def yt_search(self, ctx, *,  query: str = None):
        """Search YouTube Without An API Key"""

        await ctx.message.delete()

        # Handle error if no search query was provided
        if query is None:
            return await ctx.invoke(self.bot.get_command('error'), err='Please provide a query!')

        # Handle user provided limit using "|" as a separator
        if '|' in query:
            try:
                items = int(query.split('|')[0])
                query = query.split('|')[1].strip()
            except ValueError:
                return await ctx.invoke(self.bot.get_command('error'), err='Incorrect Syntax!')
        else:
            items = 4

        # Handle too many items being asked for by selecting 6 in min()
        if not items == 4:
            items = min(6, items)

        # This uses ytdl syntax of "search{number of items}:{query}"
        # Items are 4 by default, the user can specify their limit
        results = await self.bot.loop.run_in_executor(None, functools.partial(self.ytdl.extract_info,
                                                                              f'ytsearch{items}:{query}',
                                                                              download=False))
        results = results['entries']

        em = discord.Embed(color=self.bot.embed_colour)
        em.set_author(name="YouTube Search",
                      icon_url="https://www.seeklogo.net/wp-content/uploads/2016/06/YouTube-icon.png")

        # Create a list with format of each listing as "index. [Title](video_link) by [Uploader](uploader_link)"
        em.add_field(name="Results", value='\n'.join(
            [f"{num}. [{item['title']}]({item['webpage_url']}) by [{item['uploader']}]({item['uploader_url']})" for
             num, item in enumerate(results, 1)]))

        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(YoutubeSearch(bot))

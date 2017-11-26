#!/bin/env python

import discord
from discord.ext import commands


class Wiki:
    def __init__(self, bot):
        self.bot = bot
        self.color = bot.user_color
        self.search_uri = 'http://en.wikipedia.org/w/api.php?action=opensearch&format=json&search={}'
        self.random_uri = 'https://en.wikipedia.org/w/api.php'
        self.rand_params = {'action': 'query', 'list': 'random', 'format': 'json', 'rnnamespace': 0, 'rnlimit': 1}
        self.headers = {
            'user-agent': 'Watashi-Bot/0.1a - A fantastic selfbot (https://github.com/PrestigeDox/Watashi-SelfBot)'
        }
        self.aiohttp_session = bot.aiohttp_session

    @commands.command(name='wiki', aliases=['wi'])
    async def wiki_search(self, ctx, *, query=None):
        """Search Something Through Wiki"""

        # Determine whether we want a random article
        if not query:
            async with self.aiohttp_session.get(self.random_uri, headers=self.headers, params=self.rand_params) as r:
                rand_resp = await r.json()

            query = rand_resp['query']['random'][0]['title']

        # Spaces -> +
        formatted_query = query.replace(' ', '+')

        # Get wiki page
        async with self.aiohttp_session.get(self.search_uri.format(formatted_query), headers=self.headers) as r:
            wiki_info = await r.json()

        # No result found
        if not wiki_info[1]:
            return await ctx.error(f"Sorry, I couldn't find anything matching `{query}`.")

        msg = str()

        if wiki_info[2][0] == '':
            msg += '**Disambiguation / Redirect Page**\n'

        msg += f"{wiki_info[3][0]}"

        await ctx.message.edit(content=msg)


def setup(bot):
    bot.add_cog(Wiki(bot))

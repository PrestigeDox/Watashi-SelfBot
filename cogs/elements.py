#!/bin/env python

import discord
import json

from discord.ext import commands


class Elements:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def element(self, ctx, *, query=None):
        """ Search for elements by name or atomic number """

        await ctx.message.delete()

        # Handle no query being provided.
        if query is None:
            return await ctx.invoke(self.bot.get_command('error'), delete_after=1.0, err='Please provide a query!')

        # Users element set to none for checks further down
        u_element = None

        # Check if query is a number, if yes then it'll be looked up by atomic number
        if query.isdigit():
            atomic_mode = True
        else:
            atomic_mode = False

        # Load up the periodic table
        with open('data/PeriodicTableJSON.json') as json_table:
            periodic_table = json.load(json_table)

        for element in periodic_table['elements']:

            # Lookup by atomic number
            if atomic_mode:
                if element["number"] == int(query):
                    u_element = element
                    break

            # Lookup by name
            else:
                if element["name"].lower() == query.lower():
                    u_element = element
                    break

        # Handle invalid query with an error message
        if u_element is None:
            return await ctx.invoke(self.bot.get_command('error'), delete_after=1.0, err="Your query didn't match any "
                                                                                         "elements!")
        # Create the embed response
        em = discord.Embed(title=u_element["name"],
                           description=f'{u_element["appearance"].title()}, {u_element["category"].title()}',
                           color=self.bot.user_color)
        em.add_field(name="Symbol", value=u_element["symbol"])
        em.add_field(name="Named By", value=u_element["named_by"])
        em.add_field(name="Atomic Mass", value=str(u_element["atomic_mass"]))
        em.add_field(name="Phase", value=u_element["phase"])
        em.add_field(name="Period", value=str(u_element["period"]))
        em.add_field(name="Melting Point", value=f'{u_element["melt"]} K')
        em.add_field(name="Boiling Point", value=f'{u_element["boil"]} K')

        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Elements(bot))

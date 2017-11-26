#!/bin/env python

import discord
import json

from discord.ext import commands


# TODO
# Make this optional because... who needs element data?

class Elements:
    def __init__(self, bot):
        self.bot = bot
        self.subs = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        self.sups = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

    @commands.command()
    async def element(self, ctx, *, query=None):
        """ Search for elements by name or atomic number """
        # Handle no query being provided.
        if query is None:
            return await ctx.error('Please provide a query!')

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
            return await ctx.error("Query didn't match any elements!")

        msg = f'**{u_element["name"]}** '
        msg += f'({u_element["symbol"]}{str(u_element["number"]).translate(self.subs)}, '
        msg += f'{u_element["appearance"].title()}, {u_element["category"].title()})\n'
        msg += f'Named by: {u_element["named_by"]}\n'
        msg += f'Atomic Mass: {str(u_element["atomic_mass"])}\n'
        msg += f'Phase: {u_element["phase"]}\n'
        msg += f'Melting Point: {u_element["melt"]} K\n'
        msg += f'Boiling Point: {u_element["boil"]} K'

        await ctx.message.edit(content=msg)


def setup(bot):
    bot.add_cog(Elements(bot))

import discord
from discord.ext import commands


class Help:
    def __init__(self, bot):
        self.bot = bot
        self.color = bot.user_color
        self.cmd = bot.get_command
        self.pre = bot.command_prefix

    @commands.group(invoke_without_command=True)
    async def help(self, ctx, *, command_name: str=None):
        """ Shows the possible help categories """

        # Shortcut to command search
        if command_name is not None:
            return await ctx.invoke(self.cmd('help command'), cmd_name=command_name)

        desc = 'Below is a list of command categories.\n'\
               f'To get help or more information on a specific category or command, use:\n'\
               f'`{self.pre}help cat|category <category name>` for a category OR\n'\
               f'`{self.pre}help cmd|command <command name>` for a specific command.\n'\
               f'`{self.pre}help <command name>` is also a shortcut for the above.'

        # This can't go in the init because help isn't loaded last & thus misses some commands
        cog_name_list = sorted(self.bot.cogs)

        cat = ', '.join([f"`{cog}`" for cog in cog_name_list])
        await ctx.message.edit(content=f"**Help**\n{desc}\n**Categories:**\n{cat}")

    @help.command(name='category', aliases=['categories', 'ctg'])
    async def help_categories(self, ctx, *, category_name: str=None):
        """ Get brief help for each command in a specific category """
        # Handle no input
        if category_name is None:
            return await ctx.error('Category must be provided.')

        # This bit checks whether the category exists -> case insensitive
        # We need the proper name, though, so we search for the proper capitalization
        # And set category_name = to it
        if category_name.casefold() in [x.casefold() for x in self.bot.cogs]:
            category_name = min(self.bot.cogs, key=lambda v: len(set(category_name) ^ set(v)))
        else:
            return await ctx.error(f'`{category_name}` is not a category.')

        cmds = '\n'.join([f'\u2022 `{self.pre}{x.name}` - {x.short_doc}'
                         for x in self.bot.get_cog_commands(category_name)])

        await ctx.message.edit(content=f"**{category_name}:**\n{cmds}")

    @help.command(name='command', aliases=['cmd', 'commands'])
    async def help_command(self, ctx, *, cmd_name: str=None):
        """ Sends help for a specific command """

        # Get command object
        cmd_obj = self.cmd(cmd_name)

        # Handle no command found
        if cmd_obj is None:
            return await ctx.error(f'Command {cmd_name} not found')

        msg = f"**{cmd_obj.name}**:\n{cmd_obj.short_doc}"

        # Input aliases and parameters to embed
        if cmd_obj.aliases:
            msg += f"**Aliases:**\n" + '\n'.join([f'\u2022 {x}' for x in cmd_obj.aliases])
        if cmd_obj.clean_params:
            msg += f"**Parameters:**\n" + '\n'.join([f'\u2022 {x}' for x in cmd_obj.clean_params])

        # Handle group commands
        if isinstance(cmd_obj, commands.core.Group):
            msg += '**Group commands:**\n' + '\n'.join([f'\u2022 {x}' for x in cmd_obj.commands])

        # Add usage last
        msg += '**Usage:**' + f'```{self.pre}\u200b{cmd_name} '\
                              f'{" ".join([f"<{x}>" for x in cmd_obj.clean_params])}```'

        await ctx.message.edit(content=msg)


def setup(bot):
    bot.add_cog(Help(bot))

# !/bin/env python3
import json
from pathlib import Path
from discord.ext import commands

class Tag:
    def __init__(self, bot):
        self.bot = bot
        self._load_tag_file()

    @staticmethod
    def _tag_file_exists():
        """ Checks to see if there is a tag file in the proper place """
        return Path('tag_file.json').is_file()

    @staticmethod
    def _tag_file_valid():
        """ Ensures proper json file is found """
        try:
            with open('tag_file.json') as f:
                json.load(f)
        except:
            return False

        return True

    def _load_tag_file(self):
        """ Loads the tag file as a class attr """
        if self._tag_file_exists() and self._tag_file_valid():
            with open('tag_file.json') as f:
                self.tag_dict = json.load(f)
        else:
            self.tag_dict = {***REMOVED***
            print('Tag file not found. One will be created upon use.')

    def _write_tag_file(self):
        """ Writes the content of the tag_dict to the file """
        try:
            with open('tag_file.json', 'w') as f:
                json.dump(self.tag_dict, f)
        except Exception as e:
            print(f'Problem writing to tag file\n{e***REMOVED***')

    @commands.group(invoke_without_command=True)
    async def tag(self, ctx, *, tag_name: str):
        """ Retrieve a previously stored tag """
        if tag_name in self.tag_dict:
            # Increment uses
            self.tag_dict[tag_name]['uses'] += 1

            self._write_tag_file()
            self._load_tag_file()

            return await ctx.send(self.tag_dict[tag_name]['contents'])

        await ctx.send(f'Tag `{tag_name***REMOVED***` does not exist.')

    @tag.command()
    async def create(self, ctx, tag_name: str, *, tag_contents: str):
        """ Create a new tag """
        if tag_name in self.tag_dict:
            return await ctx.send(f'Tag `{tag_name***REMOVED*** already exists. Use `tag edit` to change it.')

        self.tag_dict[tag_name] = {'contents': tag_contents, 'uses': 0***REMOVED***
        # Not sure if this is necessary but it feels right, man
        self._write_tag_file()
        self._load_tag_file()

        await ctx.send(f'Tag `{tag_name***REMOVED***` successfully created.')

    @tag.command(name='delete', aliases=['del'])
    async def _delete(self, ctx, *, tag_name: str):
        """ Delete a tag you've previously created """
        if tag_name not in self.tag_dict:
            return await ctx.send(f'Tag `{tag_name***REMOVED***` does not exist.')

        del self.tag_dict[tag_name]
        self._write_tag_file()
        self._load_tag_file()

        await ctx.send(f'Tag `{tag_name***REMOVED***` deleted.')

    @tag.command()
    async def edit(self, ctx, tag_name: str, *, tag_contents: str):
        """ Edit a tag which you've previously created """
        if tag_name not in self.tag_dict:
            return await ctx.send(f'Tag `{tag_name***REMOVED***` does not exist.')

        self.tag_dict[tag_name]['contents'] = tag_contents
        self._write_tag_file()
        self._load_tag_file()

        await ctx.send(f'Tag `{tag_name***REMOVED***` succesfully edited.')

    @tag.command()
    async def search(self, ctx, *, tag_name: str):
        """ Search for the closest matching tag """
        # Lifted this tidbit from:
        # https://mail.python.org/pipermail/python-list/2010-August/586307.html
        closest_match = min(self.tag_dict, key=lambda v: len(set(tag_name) ^ set(v)))
        await ctx.send(f'Closest matching tag: `{closest_match***REMOVED***`.')

    @tag.command()
    async def list(self, ctx, *, tag_name: str):
        """ List your most used tags (up to 5) """
        pass


def setup(bot):
    bot.add_cog(Tag(bot))

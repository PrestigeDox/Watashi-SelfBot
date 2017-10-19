import asyncio
import traceback
import textwrap
import io
from contextlib import redirect_stdout
from discord.ext import commands

class Eval:
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.sessions = set()

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    def get_syntax_error(self, e):
        if e.text is None:
            return f'```py\n{e.__class__.__name__***REMOVED***: {e***REMOVED***\n```'
        return f'```py\n{e.text***REMOVED***{"^":>{e.offset***REMOVED******REMOVED***\n{e.__class__.__name__***REMOVED***: {e***REMOVED***```'

    @commands.command(hidden=True, name='pyval')
    @commands.is_owner()
    async def _eval(self, ctx, *, body: str):
        """Evaluates a code"""

        env = {
            'bot': self.bot,
            'ctx': ctx,
            '_': self._last_result
        ***REMOVED***

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")***REMOVED***'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__***REMOVED***: {e***REMOVED***\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value***REMOVED***{traceback.format_exc()***REMOVED***\n```')
        else:
            value = stdout.getvalue()

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value***REMOVED***\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value***REMOVED***{ret***REMOVED***\n```')

    @commands.command(name='eval', hidden=True)
    @commands.is_owner()
    async def shell_access(self, ctx, *, cmd):
        """ Access the commandline from the bot """

        process = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE)
        stdout, stderr = await process.communicate()

        try:
            if stdout:
                await ctx.send(f'`{cmd***REMOVED***`\n```{stdout.decode().strip()***REMOVED***```')
            elif stderr:
                await ctx.send(f'`{cmd***REMOVED***`\n```{stderr.decode().strip()***REMOVED***```')
            else:
                await ctx.send(f'`{cmd***REMOVED***` produced no output')

        except Exception as e:
            await ctx.send(f'Unable to send output\n```py\n{e***REMOVED***```')


def setup(bot):
    bot.add_cog(Eval(bot))

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

    @staticmethod
    def cleanup_code(content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    @staticmethod
    def get_syntax_error(e):
        if e.text is None:
            return f'```py\n{e.__class__.__name__}: {e}\n```'
        return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'

    @commands.command()
    async def pyval(self, ctx, *, body: str):
        """Evaluate some python code"""

        env = {
            'bot': self.bot,
            'ctx': ctx,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.error(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.error(f'```py\n{value}{traceback.format_exc()}\n```', delete_after=15.0)
        else:
            value = stdout.getvalue()

            if ret is None:
                if value:
                    await ctx.message.edit(content=f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.message.edit(content=f'```py\n{value}{ret}\n```')

    @commands.command(name='eval')
    async def shell_access(self, ctx, *, cmd):
        """Access the commandline from the bot"""

        process = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE)
        stdout, stderr = await process.communicate()

        try:
            if stdout:
                await ctx.send(f'`{cmd}`\n```{stdout.decode().strip()}```')
            elif stderr:
                await ctx.send(f'`{cmd}`\n```{stderr.decode().strip()}```')
            else:
                await ctx.send(f'`{cmd}` produced no output')

        except Exception as e:
            await ctx.error(f'Unable to send output\n```py\n{e}```', delete_after=15.0)


def setup(bot):
    bot.add_cog(Eval(bot))

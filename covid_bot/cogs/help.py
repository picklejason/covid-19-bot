import logging

import discord
from discord.ext import commands

from covid_bot.const import BOT_SHORT_NAME
from covid_bot.utils.codes import EMOJI_CODES
from covid_bot.utils.help import (
    add_help, clear_help, get_help, list_aliases, list_commands
)
from covid_bot.utils.time import utcnow

logger = logging.getLogger(__name__)

BOT_INFO = (
 f'Use **{BOT_SHORT_NAME} help** for more info on commands \n'
)
BOT_SAUCE = (
 f'{EMOJI_CODES["github"]} '
 '[Github](https://github.com/jwiggins/coronavirus-bot)'
)
HELP_DESCRIPTION = (
 'Data from [Corona Statistics](https://coronastatistics.live/)\n'
)
HELP_INFO = (
 'Return additional info about the bot such as server and user count'
)


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Add help data for subcommands here
        add_help('info', ['about'], HELP_INFO)

    def total_users(self):
        users = 0
        for s in self.bot.guilds:
            users += len(s.members)
        return users

    @commands.command(name='help', aliases=['h', 'commands'])
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def help(self, ctx, command='__all'):
        """ Give a little help
        """
        if command == '__all':
            # No command specified
            embed = discord.Embed(
                title='Bot Help',
                description=HELP_DESCRIPTION,
                colour=discord.Colour.red(),
                timestamp=utcnow(),
            )
            # Tell em what we've got
            commands = ', '.join(f'`{c}`' for c in list_commands())
            embed.add_field(
                name=f'Usage: ```{BOT_SHORT_NAME} help <command>```',
                value=f'Commands: {commands}',
                inline=False,
            )
            embed.add_field(name='Bot Source Code', value=BOT_SAUCE)
        else:
            # Help for a specific command
            embed = discord.Embed(
                title=f'Help for "{command}":',
                colour=discord.Colour.red(),
                timestamp=utcnow(),
            )
            aliases = list_aliases(command)
            if aliases:
                embed.add_field(
                    name='Aliases:',
                    value=', '.join(f'`{a}`' for a in aliases),
                    inline=False,
                )
            embed.add_field(
                name='Description:',
                value=get_help(command),
                inline=False,
            )
        await ctx.send(embed=embed)

    @commands.command(name='info', aliases=['about'])
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def info(self, ctx):
        embed = discord.Embed(
            title='Bot Info',
            description=HELP_DESCRIPTION + BOT_INFO,
            colour=discord.Colour.red(),
            timestamp=utcnow()
        )
        embed.add_field(
            name='Command Prefix',
            value=f'`{BOT_SHORT_NAME} ` or `@mention`'
        )

        users = self.total_users()
        embed.add_field(
            name='Servers',
            value=f'{len(self.bot.guilds)}',
        )
        embed.add_field(
            name='Users',
            value=f'{users}'
        )
        embed.add_field(name='Bot Source Code', value=BOT_SAUCE)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def ping(self, ctx):
        embed = discord.Embed(
            title='Ping',
            description=f'🏓 Pong! \n `{round(self.bot.latency * 1000)}ms`',
            colour=discord.Colour.red(),
            timestamp=utcnow(),
        )
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """ Triggers when wrong command or is inputted
        """
        if isinstance(error, commands.CommandNotFound):
            message = ctx.message.content
            logger.info(f'Invalid command use "{message}"')
        elif isinstance(error, commands.CommandOnCooldown):
            message = (
                'To prevent spam, the command has been rate limited to 3 '
                'times every 10 seconds'
            )
            logger.info(
                f'Rate limit reached by {ctx.message.author}'
                f'({ctx.message.author.id}) in {ctx.message.guild}'
                f'({ctx.message.guild.id})'
            )
            await ctx.send(message)

    @commands.command(name='reload', aliases=['r'])
    @commands.is_owner()
    async def reload(self, ctx, extension=None):
        if extension is None:
            self.bot.unload()
            clear_help()
            self.bot.load()
            await ctx.send('Reloaded All')
        else:
            # XXX: Make sure these didn't get broken in the move
            self.bot.unload_extension(f'covid_bot.cogs.{extension.title()}')
            self.bot.load_extension(f'covid_bot.cogs.{extension.title()}')
            await ctx.send(f'Reloaded {extension.title()}')


def setup(bot):
    bot.add_cog(Help(bot))

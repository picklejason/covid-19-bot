import asyncio
import logging
import os
import pkgutil

import discord
from discord.ext import commands
from discord.ext.commands import when_mentioned_or
from discord.utils import find

import covid_bot.cogs as cogs
from covid_bot.const import (
    HELLO_MESSAGE, HELP_DONATE, HELP_INVITE, HELP_SAUCE, ICON_URL
)
from covid_bot.utils.codes import EMOJI_CODES

logger = logging.getLogger(__name__)


def configure_logging():
    root_logger = logging.getLogger()
    formatter = logging.Formatter(
        '%(asctime)s:%(levelname)s:%(name)s: %(message)s'
    )

    file_handler = logging.handlers.RotatingFileHandler(
        filename='covid.log', mode='w', backupCount=10
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)
    root_logger.setLevel(logging.DEBUG)

    return file_handler


class Coronavirus(commands.AutoShardedBot):
    """ This is the main bot class
    """
    def __init__(self):
        super().__init__(
            command_prefix=when_mentioned_or('.c '),
            activity=discord.Game(name='Loading...'),
        )
        self.remove_command('help')
        self.load()

    def load(self):
        for info in pkgutil.walk_packages(cogs.__path__, cogs.__name__ + '.'):
            name = info.name
            try:
                self.load_extension(name)
                logger.info(f'{name} loaded successfully')
            except Exception:
                logger.exception(f'{name} failed to load')

    def unload(self):
        for info in pkgutil.walk_packages(cogs.__path__, cogs.__name__ + '.'):
            name = info.name
            try:
                self.unload_extension(name)
                logger.info(f'{name} unloaded successfully')
            except Exception:
                logger.exception(f'{name} failed to unload')

    async def on_ready(self):
        await self.wait_until_ready()
        while True:
            await bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name=f'{len(bot.guilds)} servers | .c help',
                ),
            )
            self.unload_extension('covid_bot.cogs.stats')
            self.load_extension('covid_bot.cogs.stats')
            logger.info('Reloaded Stats')
            await asyncio.sleep(600)

    async def on_guild_join(self, guild: discord.Guild):
        general = find(lambda x: x.name == 'general', guild.text_channels)
        if general and general.permissions_for(guild.me).send_messages:
            embed = discord.Embed(
                description=HELLO_MESSAGE,
                colour=discord.Colour.red()
            )
            embed.set_author(
                name='Coronavirus (COVID-19)',
                url='https://discord.gg/tVN2UTa',
                icon_url=ICON_URL,
            )
            embed.add_field(
                name='Command Prefix',
                value='`.c ` or `@mention`',
            )
            users = 0
            for s in self.guilds:
                users += len(s.members)

            embed.add_field(
                name='Servers | Shards',
                value=(
                    f'{EMOJI_CODES["server"]} '
                    f'{len(self.guilds)} | {len(self.shards)}'
                ),
            )
            embed.add_field(
                name='Users',
                value=f'{EMOJI_CODES["user"]} {users}',
            )
            embed.add_field(
                name='Bot Source Code',
                value=HELP_SAUCE,
            )
            embed.add_field(
                name='Bot Invite',
                value=HELP_INVITE,
            )
            embed.add_field(
                name='Donate',
                value=HELP_DONATE,
            )
            embed.set_footer(text='Made by PickleJason#5293')
            await general.send(embed=embed)


if __name__ == '__main__':
    handler = configure_logging()
    bot = Coronavirus()
    bot.run(os.environ['DISCORD_TOKEN'])
    handler.doRollover()

import logging
import logging.handlers
import os
import pkgutil

import discord
from discord.ext import commands
from discord.ext.commands import when_mentioned_or
from discord.utils import find

import covid_bot.cogs as cogs
from covid_bot.const import (
    BOT_LONG_NAME, BOT_SHORT_NAME, HELLO_MESSAGE, ICON_URL
)

logger = logging.getLogger(__name__)
MAIN_CHANNEL = os.environ.get('DISCORD_BOT_CHANNEL', 'general')


def configure_logging():
    root_logger = logging.getLogger()
    formatter = logging.Formatter(
        '%(asctime)s:%(levelname)s:%(name)s: %(message)s'
    )

    file_handler = logging.handlers.RotatingFileHandler(
        filename='covid.log', mode='w', backupCount=3
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)
    root_logger.setLevel(logging.DEBUG)

    return file_handler


class Coronavirus(commands.Bot):
    """ This is the main bot class
    """
    def __init__(self):
        super().__init__(
            command_prefix=when_mentioned_or(
                f'{BOT_SHORT_NAME} ', f'{BOT_SHORT_NAME.title()} '
            ),
            activity=discord.Game(name='Loading...'),
        )
        self.remove_command('help')
        self.load()

    def load(self):
        for info in pkgutil.walk_packages(cogs.__path__, cogs.__name__ + '.'):
            name = info.name
            try:
                self.load_extension(name)
                logger.debug(f'{name} loaded successfully')
            except Exception:
                logger.exception(f'{name} failed to load')

    def unload(self):
        for info in pkgutil.walk_packages(cogs.__path__, cogs.__name__ + '.'):
            name = info.name
            try:
                self.unload_extension(name)
                logger.debug(f'{name} unloaded successfully')
            except Exception:
                logger.exception(f'{name} failed to unload')

    async def on_ready(self):
        await self.wait_until_ready()
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f'{len(bot.guilds)} servers | {BOT_SHORT_NAME} help',
            ),
        )

    async def on_guild_join(self, guild: discord.Guild):
        channel = find(lambda x: x.name == MAIN_CHANNEL, guild.text_channels)
        if channel and channel.permissions_for(guild.me).send_messages:
            embed = discord.Embed(
                description=HELLO_MESSAGE,
                colour=discord.Colour.red()
            )
            embed.set_author(
                name=f'{BOT_LONG_NAME}',
                url='https://github.com/jwiggins/coronavirus-bot/',
                icon_url=ICON_URL,
            )
            embed.add_field(
                name='Command Prefix',
                value=f'`{BOT_SHORT_NAME} ` or `@mention`',
            )
            embed.set_footer(text='Made by PickleJason#5293 and Arsonist Cult')
            await channel.send(embed=embed)


if __name__ == '__main__':
    handler = configure_logging()
    bot = Coronavirus()
    bot.run(os.environ['DISCORD_TOKEN'])
    handler.doRollover()

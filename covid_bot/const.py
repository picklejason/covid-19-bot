import os

from covid_bot.utils.codes import EMOJI_CODES

# These names are used throughout
BOT_SHORT_NAME = os.environ.get('DISCORD_BOT_SHORT_NAME', '.cov')
BOT_LONG_NAME = os.environ.get('DISCORD_BOT_LONG_NAME', 'COVID-19')


HELLO_MESSAGE = (
 f'Thanks for inviting me! | Use **{BOT_SHORT_NAME} help** for more info on '
 'commands'
)

HELP_DESCRIPTION = (
 'Data from [Corona Statistics](https://coronastatistics.live/)\n'
 '__Documentation for all commands__'
)
HELP_GRAPH = ''
HELP_INFO = (
 'Return additional info about the bot such as server and user count'
)
HELP_LEADERBOARD = (
 'Show a "leaderboard" of countries with the highest numbers of '
 'cases/deaths/etc\n'
 f'__Example:__ **{BOT_SHORT_NAME} leaderboard**\n'
 'If you want to get fancy, you can add a sorting qualifier to the end of '
 'the command. Available qualifiers are: `cases`, `todayCases`, `deaths`, '
 '`todayDeaths`, `recovered`, `active`, `critical`, `casesPerOneMillion`, '
 '`deathsPerOneMillion`.\n'
 f'__Example:__ **{BOT_SHORT_NAME} leaderboard deaths**'
)
HELP_SAUCE = (
 f'{EMOJI_CODES["github"]} '
 '[Github](https://github.com/jwiggins/coronavirus-bot)'
)
HELP_STAT = (
 'Show **Confirmed** (new cases), **Deaths** (new deaths) and **Recovered**\n'
 '•For any country you may type the **full name** or '
 '**[ISO 3166-1 codes](https://en.wikipedia.org/wiki/ISO_3166-1)**\n'
 f'__Example:__ **{BOT_SHORT_NAME} stat Italy** | **{BOT_SHORT_NAME} stat IT**'
 f' | **{BOT_SHORT_NAME} stat ITA**\n'
 '•If the country or state\'s full name is two words, enclose them in '
 '**quotation marks**\n'
 f'__Example:__ **{BOT_SHORT_NAME} stat "South Korea"** | '
 f'**{BOT_SHORT_NAME} stat US "New York"**\n'
 '•If you would like stats on a specific **state (full name or abbreviated)** '
 'in the US, put it after the country name\n'
 f'__Example:__ **{BOT_SHORT_NAME} stat US California** or '
 f'**{BOT_SHORT_NAME} stat US CA**'
)

ICON_URL = 'https://images.discordapp.net/avatars/683462722368700526/70c1743a2d87a44116f857a88bb107e0.png?size=512'  # noqa: E501

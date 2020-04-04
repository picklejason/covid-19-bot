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
 'Data from [Worldometer](https://www.worldometers.info/coronavirus/) '
 'and [Johns Hopkins CSSE](https://github.com/CSSEGISandData/COVID-19)\n'
 '__Documentation for all commands__'
)
HELP_STAT = (
 'Show **Confirmed** (new cases), **Deaths** (new deaths) and **Recovered**\n'
 'React with 📈 for a linear graph or 📉 for a log graph\n'
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
HELP_GRAPH = (
 'Display graph for a single country or multiple countries, choose between '
 'graph type and case type | Same rules for country names apply \n'
 f'__Example:__ **{BOT_SHORT_NAME} graph log deaths '
 'nl deu ita usa chn kor jpn esp**'
)
HELP_INFO = (
 'Return additional info about the bot such as server and user count'
)
HELP_SAUCE = (
 f'{EMOJI_CODES["github"]} '
 '[Github](https://github.com/jwiggins/coronavirus-bot)'
)
ICON_URL = 'https://images.discordapp.net/avatars/683462722368700526/70c1743a2d87a44116f857a88bb107e0.png?size=512'  # noqa: E501

from covid_bot.utils.codes import EMOJI_CODES

HELLO_MESSAGE = (
 'Thanks for inviting me! | Use **.c help** for more info on commands'
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
 '__Example:__ **.c stat Italy** | **.c stat IT** | **.c stat ITA**\n'
 '•If the country or state\'s full name is two words, enclose them in '
 '**quotation marks**\n'
 '__Example:__ **.c stat "South Korea"** | **.c stat US "New York"**\n'
 '•If you would like stats on a specific **state (full name or abbreviated)** '
 'in the US, put it after the country name\n'
 '__Example:__ **.c stat US California** or **.c stat US CA**'
)
HELP_GRAPH = (
 'Display graph for a single country or multiple countries, choose between '
 'graph type and case type | Same rules for country names apply \n'
 '__Example:__ **.c graph log deaths nl deu ita usa chn kor jpn esp**'
)
HELP_REDDIT = (
 'Return posts of given category from '
 '[r/Coronavirus](https://www.reddit.com/r/Coronavirus/)\n'
 'Shows 5 posts at a time (up to first 15) Use ⬅️ and ➡️ to scroll through\n'
 '**<category>** - `Hot` | `New` | `Top`'
)
HELP_INFO = (
 'Return additional info about the bot such as server and user count'
)
HELP_SAUCE = (
 f'{EMOJI_CODES["github"]} '
 '[Github](https://github.com/picklejason/coronavirus-bot)'
)
HELP_INVITE = (
 f'{EMOJI_CODES["discord"]} '
 '[Link](https://discordapp.com/api/oauth2/authorize?client_id=683462722368700526&permissions=59456&scope=bot)'  # noqa: E501
)
HELP_DONATE = (
 f'{EMOJI_CODES["kofi"]} [Ko-fi](https://ko-fi.com/picklejason)'
)

ICON_URL = 'https://images.discordapp.net/avatars/683462722368700526/70c1743a2d87a44116f857a88bb107e0.png?size=512'  # noqa: E501

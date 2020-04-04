import json

import requests

import discord
from discord.ext import commands

API_GATEWAY = "https://api.coronastatistics.live/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:70.0) Gecko/20100101 Firefox/70.0',  # noqa: E501
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',  # noqa: E501
    'Accept-Language': 'en-US,en;q=0.5',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': '',
    'Upgrade-Insecure-Requests': '1',
}


class Stats(commands.Cog):
    """ Show me some numbers

    Data sources:
    List of countries can be assembled with:
    https://api.coronastatistics.live/countries

    List of cases by country sorted:
    https://api.coronastatistics.live/countries?sort=todayCases

    Cases timeline for specific country:
    https://api.coronastatistics.live/timeline/{country}

    Cases timeline for global:
    https://api.coronastatistics.live/timeline/global
    """

    def __init__(self, bot):
        self.bot = bot

        # create requests session
        self._session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=5,
            pool_maxsize=5,
            max_retries=10
        )
        self._session.mount('https://', adapter)
        self._session.mount('http://', adapter)

    def _make_country_list(self, country):
        """ TODO """
        pass

    def _get_global_timeline(self, country):
        """ TODO """
        pass

    def _get_country_timeline(self, country):
        """ TODO """
        pass

    def _get_country_today(self, country):
        """ Get a dictionary object containing all of the information for today
        for a specific country
        """
        content = self._fetch_from_gateway('countries', sort='todayCases')
        info = list(
            filter(lambda i: i['country'].lower() == country.lower(), content)
        )
        if len(info) != 1:
            raise ValueError(f'Bad country: found {len(info)} options')

        return info[0]

    def _fetch_from_gateway(self, *args, **kwargs):
        """ Fetch content from the API_GATEWAY by appending *args to the path
        and **kwargs used as query items
        """
        if len(kwargs.keys()) > 0:
            queries = '?' + ','.join([f'{k}={v}' for k, v in kwargs.items()])
        else:
            queries = ''

        url = API_GATEWAY + '/'.join(args) + queries
        with self._session.get(url) as r:
            cont_type = r.headers['Content-Type']
            resp = r.text

        if 'json' in cont_type:
            resp = json.loads(resp)

        return resp

    def _embed_response(self, *args, **kwargs):
        embed = discord.Embed(
            description=kwargs['description'],
            colour=discord.Colour.red()
        )
        for content in kwargs['content']:
            embed.add_field(
                name=content['name'],
                value=content['value'],
            )

        return embed

    #########################################################
    #   ------------- ASYNC EVENT ENDPOINTS -------------   #
    #########################################################

    @commands.command(name='stat')
    async def stats(self, context, location: str):
        """ embed stats for a given country / all countries into discord.Embed
        object and send to channel
        """
        response = {
            'description': f'called command "stats" with arg "{location}"',
            'content': []
        }
        try:
            info = self._get_country_today(location)
        except Exception as e:
            response['content'].append({'name': 'error', 'value': str(e)})
        else:
            response['content'].append(
                {
                    'name': 'cases',
                    'value': info['cases'],
                }
            )

        await context.send(embed=self._embed_response(**response))


def setup(bot):
    bot.add_cog(Stats(bot))


if __name__ == '__main__':
    # DEBUG and testing
    import code
    s = Stats(None)
    code.interact(local=dict(globals(), **locals()))

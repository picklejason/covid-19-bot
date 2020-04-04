import json

import requests

import discord
from discord.ext import commands

from covid_bot.utils.graphing import Graph

API_GATEWAY = "https://api.coronastatistics.live/"
# country dict keys
C_KEYS = ['cases', 'todayCases', 'deaths', 'todayDeaths', 'recovered', 'active', 'critical', 'casesPerOneMillion', 'deathsPerOneMillion']


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

	def _get_country_list(self):
		""" TODO """
		content = self._get_countries_table()
		countries = [i['country'] for i in content if 'country' in i]
		return countries

	def _get_global_timeline(self):
		""" gets the timeline of cases/deaths/recovered for global """
		return self._fetch_from_gateway('timeline', 'global')

	def _plot_timeline(self, timeline, log=False, **kwargs):
		""" plots a timeline """
		g = Graph(timeline, log=log)
		g.plot_all()
		return g.save()

	def _get_country_timeline(self, country):
		""" gets the timeline of cases/deaths/recovered for country """
		content = self._fetch_from_gateway('timeline', country)['data']
		data = {}
		for i in content['timeline']:
			data[i['date']] = {
				'cases'		:	i['cases'],
				'recovered'	:	i['recovered'],
				'deaths'	:	i['deaths']
			}
		return data

	def _get_country_today(self, country):
		""" Get a dictionary object containing all of the information for today
		for a specific country
		"""
		content = self._get_countries_table()
		info = list(
			filter(lambda i: i['country'].lower() == country.lower(), content)
		)
		if len(info) != 1:
			raise ValueError(f'Bad country: found {len(info)} options')

		return info[0]

	def _get_top_countries(self, sorted_by, n=10):
		""" returns country information for the top n [10] countries sorted by query
		"""
		return self._get_countries_table(sorted_by=sorted_by)[:n]

	def _get_countries_table(self, sorted_by='todayCases'):
		""" get a list of dictionaries containing all data for countries sorted by query
		"""
		return self._fetch_from_gateway('countries', sort=sorted_by)

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

	def _response_template(self, descr):
		return {
			'description': descr,
			'content': []
		}

	#########################################################
	#   ------------- ASYNC EVENT ENDPOINTS -------------   #
	#########################################################

	@commands.command(name='stats', aliases=['stat'])
	async def stats(self, context, location: str):
		""" embed stats for a given country / all countries into discord.Embed
		object and send to channel
		"""
		response = self._response_template(f'**COVID-19 stats for {location.title()}**')
		try:
			info = self._get_country_today(location)
		except Exception as e:
			response['content'].append({'name': 'error', 'value': str(e)})
		else:
			for k, v in info.items():
				if k == 'country':	# don't add country lol
					continue
				response['content'].append(
					{
						'name'	:	k.title(),
						'value' :	v
					}
				)

		await context.send(embed=self._embed_response(**response))

	@commands.command(name='leaderboard', aliases=['lb', 'leadboard', 'lboard'])
	async def leaderboard(self, context, sorting='cases'):
		""" make a leaderboard for key in C_KEYS
		"""
		response = self._response_template(f'**COVID-19 leaderboard sorted by "{sorting}"**')
		if sorting in C_KEYS:
			countries = self._get_top_countries(sorted_by=sorting)
			info = "\n".join([f'**{i+1}: {k["country"]}**\n{k[sorting]}' for i, k in enumerate(countries)])
			response['content'].append(
				{
					'name'	:	'Top 10 Countries:',
					'value'	:	info
				}
			)
		else:
			response['content'].append(
				{
					'name'	:	'error:',
					'value'	:	f'Bad key "{sorting}"'
				}
			)	
		await context.send(embed=self._embed_response(**response))

	@commands.command(name='plot')
	async def plot(self, context, country='all'):
		""" make and send the desired plot
		"""
		response = self._response_template(f'**COVID-19 Graph for "{country}"**')

		if country is 'all':
			timeline = self._get_global_timeline()
			img = self._plot_timeline(timeline)
		else:
			try:
				timeline = self._get_country_timeline(country)
			except:
				response['content'].append(
					{
						'name'	:	'error:',
						'value'	:	f'Bad country "{country}"'
					}
				)
				img = None
			else:
				img = self._plot_timeline(timeline)

		await context.send(
			file=discord.File(img, filename=f'image.png'),
			embed=self._embed_response(**response)
		)


def setup(bot):
	bot.add_cog(Stats(bot))

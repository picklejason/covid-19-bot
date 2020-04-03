import asyncio
import gc
import io
import logging
import os

import discord
from discord.ext import commands
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests

from covid_bot.const import ICON_URL
from covid_bot.utils.codes import (
    ALT_NAMES, COUNTRY_CODES_2, COUNTRY_CODES_2_VALUES, COUNTRY_CODES_3,
    EMOJI_CODES, JHU_NAMES, JHU_NAMES_VALUES, US_STATE_CODES,
    US_STATE_CODES_VALUES
)
from covid_bot.utils.time import utcnow

logger = logging.getLogger(__name__)

CONFIRMED_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'  # noqa: E501
DEATHS_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'  # noqa: E501
RECOVERED_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'  # noqa: E501

WOM_URL = 'https://www.worldometers.info/coronavirus/'
US_WOM_URL = 'https://www.worldometers.info/coronavirus/country/us/'

CHROME_DISGUISE = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36'  # noqa: E501
HTTP_HEADERS = {
    'User-Agent': CHROME_DISGUISE,
    'X-Requested-With': 'XMLHttpRequest',
}

BASE_DESCRIPTION = ''
OTHER_DESCRIPTION = (
 'React with 📈 for a **linear** graph or 📉 for a **log** graph'
)

FIELD_CONFIRMED = f'{EMOJI_CODES["confirmed"]} Confirmed'
FIELD_DEATHS = f'{EMOJI_CODES["deaths"]} Deaths'
FIELD_RECOVERD = f'{EMOJI_CODES["recovered"]} Recovered'
FIELD_ACTIVE = f'{EMOJI_CODES["activecases"]} Active Cases'
FIELD_MORTALITY = f'{EMOJI_CODES["mortalityrate"]} Mortality Rate'
FIELD_RECOVERY = f'{EMOJI_CODES["recoveryrate"]} Recovery Rate'


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Parse Data
        self.confirmed_df = pd.read_csv(
            CONFIRMED_URL,
            error_bad_lines=False,
        ).dropna(
            axis=1,
            how='all',
        )
        self.deaths_df = pd.read_csv(
            DEATHS_URL,
            error_bad_lines=False,
        ).dropna(
            axis=1,
            how='all',
        )
        self.recovered_df = pd.read_csv(
            RECOVERED_URL,
            error_bad_lines=False,
        ).dropna(
            axis=1,
            how='all',
        )

        self.r = requests.get(WOM_URL, headers=HTTP_HEADERS)
        self.r1 = requests.get(US_WOM_URL, headers=HTTP_HEADERS)
        self.df_list = pd.read_html(self.r.text)
        self.us_df_list = pd.read_html(self.r1.text)
        self.df = self.df_list[0].replace(
            np.nan, 0
        ).replace(
            ',', '',
            regex=True,
        )
        self.us_df = self.us_df_list[0].replace(
            np.nan, 0
        ).replace(
            ',', '',
            regex=True,
        )

    # type: 'Country,Other', 'TotalCases', 'TotalDeaths', 'NewDeaths',
    # 'TotalRecovered', 'ActiveCases', 'Serious,Critical'
    def getLocation(self, location, type):
        key = self.df['Country,Other'].str.match(location, na=False)
        df_loc = self.df[key][type].values[0]
        return df_loc

    def getState(self, state, type):
        key = self.us_df['USAState'].str.match(state, na=False)
        df_state = self.us_df[key][type].values[0]
        return df_state

    def getTotal(self, type):
        key = self.df['Country,Other'].str.match('Total:', na=False)
        df_all = self.df[key][type].values[0]
        return df_all

    async def reaction_plot(self, graph_type, location):
        fig = plt.figure(dpi=150)
        plt.style.use('dark_background')

        data = (
            (self.confirmed_df, 'Confirmed', 'orange'),
            (self.recovered_df, 'Recovered', 'lightgreen'),
            (self.deaths_df, 'Deaths', 'red'),
        )
        kwargs = {'marker': 'o'}
        if graph_type == 'log':
            kwargs['logy'] = True

        if location == 'ALL':
            for df, label, color in data:
                ax = df.iloc[:, 4:].sum().plot(
                    label=label,
                    color=color,
                    **kwargs
                )
        else:
            col = 'Country/Region'
            for df, label, color in data:
                key = df[col].str.contains(location, na=False)
                ax = df[key].iloc[:, 4:].sum().plot(
                    label=label,
                    color=color,
                    **kwargs
                )

        if graph_type == 'linear':
            filename = './graphs/lineargraph.png'
            ax.set_ylim(0)
            plt.title('Linear Graph')

        elif graph_type == 'log':
            filename = './graphs/loggraph.png'
            ax.set_ylim(10**2)
            plt.title('Logarithmic Graph')
            plt.minorticks_off()

        ax.legend(loc='upper left', fancybox=True, facecolor='0.2')
        ax.yaxis.grid()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        locs, _ = plt.yticks()
        ylabels = []
        for l in locs:
            lab = str(int(l)).replace(
                '00000000', '00M'
            ).replace(
                '0000000', '0M'
            ).replace(
                '000000', 'M'
            ).replace(
                '00000', '00K'
            ).replace(
                '0000', '0K'
            ).replace(
                '000', 'K'
            )
            if not ('K' in lab or 'M' in lab):
                lab = '{:,}'.format(int(lab))
            ylabels.append(lab)

        plt.yticks(locs, ylabels)
        plt.savefig(filename, transparent=True)
        plt.cla()
        plt.close(fig)
        plt.close('all')
        gc.collect()

        with open(filename, 'rb') as fp:
            data = io.BytesIO(fp.read())

        return discord.File(data, filename=f'{graph_type}graph.png')

    # Statistics Command
    @commands.command(name='stat',
                      aliases=['stats', 'statistic', 's', 'cases'])
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def stat(self, ctx, location='ALL', state=''):
        # Parameter formatting | Check if country code
        if len(location) == 2 or len(location) == 3:
            location = location.upper()
        else:
            location = location.title()

        if len(state) == 2:
            state = state.upper()
        else:
            state = state.title()

        if location in COUNTRY_CODES_2:
            location = COUNTRY_CODES_2[location]
        elif location in COUNTRY_CODES_3:
            location = COUNTRY_CODES_3[location]
        elif location in ALT_NAMES:
            location = ALT_NAMES[location]

        if state in US_STATE_CODES:
            state = US_STATE_CODES[state]

        # Check if data exists for location
        if location == 'ALL' or location in COUNTRY_CODES_2_VALUES:
            # Parse and sum data
            if location == 'ALL':
                confirmed = self.getTotal('TotalCases')
                new_confirmed = self.getTotal('NewCases')
                deaths = self.getTotal('TotalDeaths')
                new_deaths = self.getTotal('NewDeaths')
                recovered = self.getTotal('TotalRecovered')
                active = self.getTotal('ActiveCases')
            elif state:
                if state in US_STATE_CODES_VALUES:
                    confirmed = self.getState(state, 'TotalCases')
                    new_confirmed = self.getState(state, 'NewCases')
                    deaths = self.getState(state, 'TotalDeaths')
                    new_deaths = self.getState(state, 'NewDeaths')
                    active = self.getState(state, 'ActiveCases')
                elif location == 'Canada':
                    def keygen(df):
                        return df['Province/State'].str.contains(
                            state, na=False
                        )
                    key = keygen(self.confirmed_df)
                    confirmed = self.confirmed_df[key].iloc[:, -1].sum()
                    prev_confirmed = self.confirmed_df[key].iloc[:, -2].sum()
                    key = keygen(self.deaths_df)
                    deaths = self.deaths_df[key].iloc[:, -1].sum()
                    prev_deaths = self.deaths_df[key].iloc[:, -2].sum()
                    key = keygen(self.recovered_df)
                    recovered = self.recovered_df[key].iloc[:, -1].sum()
                    active = confirmed - deaths - recovered
                    new_confirmed = confirmed - prev_confirmed
                    new_deaths = deaths - prev_deaths
                else:
                    await ctx.send(
                        'There is no available data for this location | '
                        'Use **.c help** for more info on commands'
                    )
            else:
                confirmed = self.getLocation(location, 'TotalCases')
                new_confirmed = self.getLocation(location, 'NewCases')
                deaths = self.getLocation(location, 'TotalDeaths')
                new_deaths = self.getLocation(location, 'NewDeaths')
                recovered = self.getLocation(location, 'TotalRecovered')
                active = self.getLocation(location, 'ActiveCases')

            if len(state) > 0:
                name = f'Coronavirus (COVID-19) Cases | {state}, {location}'
            else:
                name = f'Coronavirus (COVID-19) Cases | {location}'

            if int(new_confirmed) > 0:
                new_confirmed = f'(+{int(new_confirmed)})'
            elif new_confirmed == 0:
                new_confirmed = ''

            if int(new_deaths) > 0:
                new_deaths = f'(+{int(new_deaths)})'
            elif new_deaths == 0:
                new_deaths = ''

            if confirmed != 0:
                mortality_rate = round((deaths/confirmed * 100), 2)
                if state:
                    pass
                else:
                    recovery_rate = round((recovered/confirmed * 100), 2)

            description = BASE_DESCRIPTION if state else OTHER_DESCRIPTION
            embed = discord.Embed(
                description=description,
                colour=discord.Colour.red(),
                timestamp=utcnow(),
            )
            embed.add_field(
                name=FIELD_CONFIRMED,
                value=f'**{int(confirmed)}** {new_confirmed}',
            )
            embed.add_field(
                name=FIELD_DEATHS,
                value=f'**{int(deaths)}** {new_deaths}',
            )
            if state:
                embed.set_author(
                    name=name,
                    url=US_WOM_URL,
                    icon_url=ICON_URL,
                )
                embed.add_field(
                    name=FIELD_ACTIVE,
                    value=f'**{int(active)}**',
                )
                embed.add_field(
                    name=FIELD_MORTALITY,
                    value=f'**{mortality_rate}%**',
                )
            else:
                embed.set_author(
                    name=name,
                    url=WOM_URL,
                    icon_url=ICON_URL,
                )
                embed.add_field(
                    name=FIELD_RECOVERD,
                    value=f'**{int(recovered)}**',
                )
                embed.add_field(
                    name=FIELD_ACTIVE,
                    value=f'**{int(active)}**',
                )
                embed.add_field(
                    name=FIELD_MORTALITY,
                    value=f'**{mortality_rate}%**',
                )
                embed.add_field(
                    name=FIELD_RECOVERY,
                    value=f'**{recovery_rate}%**',
                )
            embed.set_footer(
                text='Data from Worldometer and Johns Hopkins CSSE'
            )
            msg = await ctx.send(embed=embed)

            # Graph reactions
            linear = '📈'
            log = '📉'
            graphs = [linear, log]

            def predicate(message):
                def check(reaction, user):
                    if (reaction.message.id != message.id
                            or user == self.bot.user):
                        return False
                    if reaction.emoji == linear and user == ctx.message.author:
                        return True
                    if reaction.emoji == log and user == ctx.message.author:
                        return True
                    return False
                return check

            if location in JHU_NAMES:
                location = JHU_NAMES[location]

            if state:
                pass
            else:
                for graph in graphs:
                    await msg.add_reaction(graph)

            while True:
                try:
                    react, self.user = await self.bot.wait_for(
                        'reaction_add',
                        check=predicate(msg),
                        timeout=30
                    )
                except asyncio.TimeoutError:
                    embed = discord.Embed(
                        description=BASE_DESCRIPTION,
                        colour=discord.Colour.red(),
                        timestamp=utcnow()
                        )
                    embed.set_author(
                        name=name,
                        url=WOM_URL,
                        icon_url=ICON_URL,
                    )
                    embed.add_field(
                        name=FIELD_CONFIRMED,
                        value=f'**{int(confirmed)}** {new_confirmed}',
                    )
                    embed.add_field(
                        name=FIELD_DEATHS,
                        value=f'**{int(deaths)}** {new_deaths}',
                    )
                    embed.add_field(
                        name=FIELD_RECOVERD,
                        value=f'**{int(recovered)}**',
                    )
                    embed.add_field(
                        name=FIELD_ACTIVE,
                        value=f'**{int(active)}**',
                    )
                    embed.add_field(
                        name=FIELD_MORTALITY,
                        value=f'**{mortality_rate}%**',
                    )
                    embed.add_field(
                        name=FIELD_RECOVERY,
                        value=f'**{recovery_rate}%**',
                    )
                    embed.set_footer(
                        text='Data from Worldometer and Johns Hopkins CSSE'
                    )
                    await msg.edit(embed=embed)
                    await msg.remove_reaction(linear, self.bot.user)
                    await msg.remove_reaction(log, self.bot.user)

                graph_type = ''
                if react.emoji == linear:
                    graph_type = 'linear'
                    await msg.remove_reaction(linear, self.user)
                    await msg.remove_reaction(linear, self.bot.user)
                    image = await self.reaction_plot(graph_type, location)
                    embed.set_image(url=f'attachment://{graph_type}graph.png')
                    await msg.delete()
                    await ctx.send(file=image, embed=embed)

                elif react.emoji == log:
                    graph_type = 'log'
                    await msg.remove_reaction(log, self.user)
                    await msg.remove_reaction(log, self.bot.user)
                    image = await self.reaction_plot(graph_type, location)
                    embed.set_image(url=f'attachment://{graph_type}graph.png')
                    await msg.delete()
                    await ctx.send(file=image, embed=embed)

                if os.path.exists(f'./graphs/{graph_type}graph.png'):
                    os.remove(f'./graphs/{graph_type}graph.png')

        else:
            await ctx.send(
                'There is no available data for this location | '
                'Use **.c help** for more info on commands'
            )

    @commands.command()
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def graph(self, ctx, graph_type, type, *location):
        countries = []
        # Parameter formatting | Check if country code
        for country in location:
            if len(country) == 2 or len(country) == 3:
                country = country.upper()
            else:
                country = country.title()

            if country in COUNTRY_CODES_2:
                country = COUNTRY_CODES_2[country]
            elif country in COUNTRY_CODES_3:
                country = COUNTRY_CODES_3[country]
            elif country in ALT_NAMES:
                country = ALT_NAMES[country]

            if country in JHU_NAMES:
                country = JHU_NAMES[country]

            countries.append(country)

        fig = plt.figure(dpi=150)
        plt.style.use('dark_background')

        data = {
            'confirmed': self.confirmed_df,
            'recovered': self.recovered_df,
            'deaths': self.deaths_df,
        }
        kwargs = {}
        if graph_type == 'log':
            kwargs['logy'] = True

        for country in countries:
            if (country in COUNTRY_CODES_2_VALUES
                    or country in JHU_NAMES_VALUES):
                # Plot
                df = data[type]
                key = df['Country/Region'].str.contains(country, na=False)
                ax = df[key].iloc[:, 4:].sum().plot(label=country, **kwargs)
            else:
                await ctx.send(
                    f'{country} is not a valid location',
                    delete_after=3,
                )

        if graph_type == 'linear':
            filename = './graphs/lineargraph.png'
            ax.set_ylim(0)
            plt.title(f'{type.title()} Linear Graph')

        elif graph_type == 'log':
            filename = './graphs/loggraph.png'
            ax.set_ylim(10**2)
            plt.title(f'{type.title()} Logarithmic Graph')
            plt.minorticks_off()

        ax.legend(loc='upper left', fancybox=True, facecolor='0.2')
        ax.yaxis.grid()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        locs, _ = plt.yticks()
        ylabels = []
        for l in locs:
            lab = str(int(l)).replace(
                '00000000', '00M'
            ).replace(
                '0000000', '0M'
            ).replace(
                '000000', 'M'
            ).replace(
                '00000', '00K'
            ).replace(
                '0000', '0K'
            ).replace(
                '000', 'K'
            )
            if not ('K' in lab or 'M' in lab):
                lab = '{:,}'.format(int(lab))
            ylabels.append(lab)
        plt.yticks(locs, ylabels)
        plt.savefig(filename, transparent=True)
        plt.cla()
        plt.close(fig)
        plt.close('all')
        gc.collect()
        with open(filename, 'rb') as f:
            file = io.BytesIO(f.read())
        image = discord.File(file, filename=f'{graph_type}graph.png')
        embed = discord.Embed(
            # description=BASE_DESCRIPTION,
            colour=discord.Colour.red(),
            timestamp=utcnow(),
        )

        embed.set_image(url=f'attachment://{graph_type}graph.png')
        embed.set_footer(
            text=f'Requested by {ctx.message.author}',
            icon_url=ctx.message.author.avatar_url,
        )
        await ctx.send(file=image, embed=embed)

        if os.path.exists(f'./graphs/{graph_type}graph.png'):
            os.remove(f'./graphs/{graph_type}graph.png')
        else:
            pass

    @commands.command()
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def vcset(self, ctx, channel: discord.VoiceChannel, *,
                    location='All', state=''):
        if len(location) == 2:
            location = location.upper()
        else:
            location = location.title()
        if len(state) == 2:
            state = state.upper()
        else:
            state = state.title()
        if location in COUNTRY_CODES_2:
            location = COUNTRY_CODES_2[location]
        elif location in COUNTRY_CODES_3:
            location = COUNTRY_CODES_3[location]
        elif location in ALT_NAMES:
            location = ALT_NAMES[location]
        if state in US_STATE_CODES:
            state = US_STATE_CODES[state]

        while True:
            # Check if data exists for location
            if location == 'All' or location == 'Other' or self.confirmed_df['Country/Region'].str.contains(location).any():
                # Parse Data
                if location == 'All':
                    confirmed = self.confirmed_df.iloc[:, -1].sum()
                    # deaths = self.deaths_df.iloc[:, -1].sum()
                    # recovered = self.recovered_df.iloc[:,-1].sum()
                elif location == 'Other':
                    confirmed = self.confirmed_df[~self.confirmed_df['Country/Region'].str.contains('China', na=False)].iloc[:, -1].sum()
                    # deaths = self.deaths_df[~self.deaths_df['Country/Region'].str.contains('China', na=False)].iloc[:, -1].sum()
                    # recovered = self.recovered_df[~self.recovered_df['Country/Region'].str.contains('China', na=False)].iloc[:,-1].sum()
                else:
                    confirmed = self.confirmed_df[self.confirmed_df['Country/Region'].str.match(location, na=False)].iloc[:, -1].sum()
                    # deaths = self.deaths_df[self.deaths_df['Country/Region'].str.match(location, na=False)].iloc[:, -1].sum()
                    # recovered = self.recovered_df[self.recovered_df['Country/Region'].str.match(location, na=False)].iloc[:, -1].sum()
            else:
                await ctx.send(
                    'There is no available data for this location | '
                    'Use **.c help** for more info on commands'
                )

            await channel.edit(name=f'😷 {location}: {str(confirmed)}')
            # Sleep all day
            await asyncio.sleep(24 * 60 * 60)


def setup(bot):
    bot.add_cog(Stats(bot))

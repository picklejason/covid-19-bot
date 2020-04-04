# Coronavirus Bot

This is a Discord bot written in Python with [discord.py](https://discordpy.readthedocs.io/en/latest/)
for providing info on the novel coronavirus (COVID-19) originally written by
[picklejason](https://github.com/picklejason/coronavirus-bot/).

Current features include stats showing total confirmed, deaths, and recovered cases.
A graph (linear or log) is also displayed showing confirmed cases and deaths from late
January to current day.

Data for the stats and graph are from
[Worldometer](https://www.worldometers.info/coronavirus/) and
[Johns Hopkins CSSE](https://github.com/CSSEGISandData/COVID-19)

## Usage

* The command prefix for the bot is `@mention` or some other configurable name

* Use the `help` command for further info

### Features

* React with :chart_with_upwards_trend: for a linear graph or :chart_with_downwards_trend: for a log graph

* `<bot name> stat all` Stats of all locations

* <img align="center" style="float: centrer; margin: 0 10px 0 0;" src="https://i.gyazo.com/8185b791eb2591904f6af75f420f64c8.png" height="220" width="350"/>

* <img align="center" style="float: centrer; margin: 0 10px 0 0;" src="https://i.gyazo.com/0d7175e78a006acb189f6c900d0799ca.png" height="430" width="350"/>

* `<bot name> stat <country name>` Stats of a specific country

* <img align="center" style="float: centrer; margin: 0 10px 0 0;" src="https://i.gyazo.com/45274a293bb7d422973e6b721007a440.png" height="430" width="350"/>

* `<bot name> stat <US> <state>` Stats of a specific state in the United States

* <img align="center" style="float: centrer; margin: 0 10px 0 0;" src="https://i.gyazo.com/b736a91e0143211f1f2c38e94ecf282c.png" height="220" width="350"/>

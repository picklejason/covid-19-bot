import discord
import logging
from discord.ext import commands
from datetime import datetime

logger = logging.getLogger('covid-19')

class Test(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def total_users(self):
        users = 0
        for s in self.bot.guilds:
            users += len(s.members)
        return users

    @commands.command(name='test', aliases=['t', 'check'])
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def test(self, ctx):

        embed = discord.Embed(
            title='CDC Covid-19 Self-Checker',
            description='This [HealthBot](https://covid19healthbot.cdc.gov/) helps to determine whether you should get tested.',
            colour=discord.Colour.red(),
            timestamp=datetime.utcnow()
            )
        embed.add_field(name='Bot Source Code', value='<:github:689501322969350158> [Github](https://github.com/picklejason/coronavirus-bot)') #If you self host this bot or use any part of this source code, I would be grateful if you leave this in or credit me somewhere else
        embed.add_field(name='Bot Invite', value='<:discord:689486285349715995> [Link](https://discordapp.com/api/oauth2/authorize?client_id=683462722368700526&permissions=59456&scope=bot)')
        embed.add_field(name='Donate', value='<:Kofi:689483361785217299> [Ko-fi](https://ko-fi.com/picklejason)')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Test(bot))

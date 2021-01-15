import asyncio

from discord.ext import commands

from core.interbed import InteractiveEmbed, ImageServer


def setup(bot):
    bot.add_cog(InterTest(bot))


class InterSession:
    def __init__(self, bot, imageserver, datapath, channel):
        self.counter = 0
        self.range = (1, 5)

        self.datapath = datapath

        self.interbed = InteractiveEmbed(bot, imageserver, channel)

        self.interbed.add_button(bot.guild.emojis[0], callback=self.btn_up)
        self.interbed.add_button(bot.guild.emojis[1], callback=self.btn_down)

        for i in range(self.range[0], self.range[1]+1):
            self.interbed.load_image(self.datapath/f'{i}.png')

    async def start(self):
        await self.interbed.start()

    async def btn_up(self, member):
        if self.counter >= self.range[1]:
            self.counter = self.range[0]
        else:
            self.counter += 1

        self.interbed.set_image(f'{self.counter}.png')

    async def btn_down(self, member):
        if self.counter <= self.range[0]:
            self.counter = self.range[1]
        else:
            self.counter -= 1

        self.interbed.set_image(f'{self.counter}.png')


class InterTest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.datapath = self.bot.datapath / 'viergewinnt'

        self.imageserver = ImageServer(self.bot.datapath/'InteractiveEmbed', 'sers-mahlzeit.de')
        self.sessions = []

    @commands.command()
    async def start(self, context):
        ie = InterSession(self.bot, self.imageserver, self.datapath, context.channel)
        self.sessions.append(ie)
        await ie.start()
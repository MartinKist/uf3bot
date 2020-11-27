import asyncio

from discord.ext import commands


def is_admin_check():
    async def predicate(context):
        try:
            return context.author.guild_permissions.administrator
        except AttributeError:
            return False
    return commands.check(predicate)

async def user_input(bot, channel, user):
    event = UserInputEvent(bot, channel, user)
    while True:
        return await event.queue.get()


async def c_user_input(context):
    event = UserInputEvent(context.bot, context.channel, context.user)
    while True:
        return await event.queue.get()


class UserInputEvent:
    def __init__(self, bot, channel, user):
        self.bot = bot
        self.channel = channel
        self.user = user
        self.queue = asyncio.Queue()

        self.bot.add_listener(self.on_message)

    async def on_message(self, message):
        if message.author.id == self.user.id and message.channel == self.channel:
            await self.queue.put(message)

    def __del__(self):
        self.bot.remove_listener(self.on_message)

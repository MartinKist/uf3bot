import random

from discord.ext import commands

from core.audio import VoiceHandler
from core.utils import send_more, is_admin


# TODO: vermutlich broken
def setup(bot):
    bot.voice = VoiceHandler(bot)
    bot.add_cog(SoundBoard(bot))


class SoundBoard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.soundspath = self.bot.datapath/'MP3'
        self.temppath = self.bot.temppath

        self.soundfiles = {}

        self.sus_session = None
        self.listening_mode_active = False
        self.on_join_mode_active = False

        self.bot.add_listener(self.on_message)
        self.bot.add_listener(self.on_voice_state_update)

    def load_sounds(self):
        for sound in self.soundspath.iterdir():
            if sound.name.endswith('.mp3'):
                self.soundfiles.update({sound.name[:-4]: sound})

    async def play_sound(self, member, sound_name_in):
        self.load_sounds()
        for sound_name, sound_path in self.soundfiles.items():
            if sound_name.lower() == sound_name_in.lower():
                await self.bot.voice.play(member, sound_path)

    async def play_random_sound(self, member):
        sound_name = random.choice(list(self.soundfiles))
        await self.bot.voice.play(member, self.soundfiles[sound_name])

    @commands.command()
    async def play(self, context, *sound_name_in: str):
        if len(sound_name_in) == 0:
            await self.play_random_sound(context.author)
        else:
            await self.play_sound(context.author, sound_name_in[0])

    @commands.command(name='lm')
    @is_admin()
    async def listener_mode(self, context):
        self.listening_mode_active = not self.listening_mode_active

        if self.listening_mode_active:
            await context.channel.send(f'_Listening mode enabled_')
        else:
            await context.channel.send(f'_Listening mode disabled_')

    @commands.command(name='oj')
    @is_admin()
    async def on_join_mode(self, context):
        self.on_join_mode_active = not self.on_join_mode_active

        if self.on_join_mode_active:
            await context.channel.send(f'_On join enabled_')
        else:
            await context.channel.send(f'_On join disabled_')

    @commands.command()
    async def stop(self, context):
        if self.bot.voice.vc:
            await self.bot.voice.disconnect()

    @commands.command()
    async def list(self, context):
        self.load_sounds()
        out = ''
        for sound_name in self.soundfiles:
            out += '\n' + sound_name
        await send_more(context.channel, out)

    async def on_message(self, message):
        if not self.listening_mode_active or message.author == self.bot.user:
            return

        self.load_sounds()
        for sound_name, sound_path in self.soundfiles.items():
            if sound_name in message.content:
                await self.bot.voice.play(message.author, sound_path)

    async def on_voice_state_update(self, member, before, after):
        if member == self.bot.user or not self.on_join_mode_active:
            return
        if before.channel is None and after.channel:
            if after.channel == self.bot.guild.afk_channel:
                return
            await self.play_random_sound(member)

    def get_filepath(self, filename):
        self.load_sounds()
        if filename not in self.soundfiles:
            raise FileNotFoundError
        else:
            return self.soundfiles[filename]
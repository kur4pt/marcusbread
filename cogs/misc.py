from selfbot import PREFIX
import discord
import asyncio
import random
import emoji
from discord.ext import commands
from PIL import Image
import io
import typing
import aiohttp
import json 
import os 

with open("./data/config.json") as f:
    config = json.load(f)
    bot_PREFIX = config.get("PREFIX")

class misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji_converter = commands.EmojiConverter()
        self.emoji_list = []



    @commands.command()
    async def snipe(self, ctx):
        """Shows you the most recently deleted message"""
        await ctx.send("> " + self.bot.snipes[ctx.message.channel.id])

    @commands.command(aliases=["tt"])
    async def triggertyping(
        self, ctx, duration: int, channel: discord.TextChannel = None
    ):
        """sends a typing indicator for a specified amount of time
        Parameters
        • duration - how long to keep the typing indicator running
        • channel - which channel to send the typing indicator in, defaults to the current channel
        """
        channel = channel or ctx.channel
        async with channel.typing():
            await asyncio.sleep(duration)

    @commands.command()
    async def hexcode(self, ctx, *, role: discord.Role):
        """returns the hexcode of a role's color
        Parameters
        • role - the role to display the color of
        """
        await ctx.send(f"{role.name} : {role.color}")

    @commands.command(aliases=["em"])
    async def embed(self, ctx, color: typing.Optional[discord.Color] = None, *, text):
        """embed text
        Parameters
        • text - the text to embed
        • color - the color of the embed, a random color is used if left empty
        """
        em = discord.Embed(color=color or random.randint(0, 0xFFFFFF))
        em.description = text
        await ctx.send(embed=em)
        await ctx.message.delete()

    @commands.command(aliases=["rr"])
    async def randomreact(
        self,
        ctx,
        message_no: int,
        no_of_reactions: typing.Optional[int] = 20,
        *,
        server: str = None,
    ):
        """react to a message with random emojis
        Parameters
        • message_no - the index of the message to react to
        • no_of_reactions - amount of random emojis to react with, defaults to 20
        • server - the server from which to choose the emojis to react with, defaults to global emojis
        """
        message_no -= 1
        server = server.lower() if server else server
        self.emoji_list = []
        await ctx.message.delete()
        if server is None:
            self.emoji_list = [
                emoji for emoji in self.bot.emojis if emoji.name.startswith("GW")
            ]
        elif server:
            s = discord.utils.find(lambda s: server in s.name.lower(), self.bot.guilds)
            self.emoji_list = [emoji for emoji in s.emojis if not emoji.animated]
        for index, message in enumerate(await ctx.channel.history(limit=30).flatten()):
            if index != message_no:
                continue
            for i in range(no_of_reactions):
                emoji = self.emoji_list.pop(
                    self.emoji_list.index(random.choice(self.emoji_list))
                )
                await message.add_reaction(emoji)
                await asyncio.sleep(0.1)
            break

    @commands.command()
    async def react(self, ctx, message_no: typing.Optional[int] = 1, *, emojis):
        """react to a specified message with emojis
        Parameters
        • message_no - the index of the message to react to
        • emojis - the emojis to react with
        """
        history = await ctx.channel.history(limit=30).flatten()
        message = history[messageNo]
        async for emoji in self.validate_emojis(ctx, emojis):
            await message.add_reaction(emoji)
        await ctx.message.delete()

    async def validate_emojis(self, ctx, *reactions):
        """
        Checks if an emoji is valid otherwise,
        tries to convert it into a custom emoji
        """
        for emote in reactions:
            if emote in emoji.UNICODE_EMOJI:
                yield emote
            else:
                try:
                    yield await self.emoji_converter.convert(ctx, emote)
                except commands.BadArgument:
                    pass

    @commands.command(aliases=["color", "colour", "sc"])
    async def getcolor(
        self,
        ctx,
        color: discord.Colour,
        width: int = 200,
        height: int = 90,
        show_hexcode=True,
    ):
        """displays a color from its name or hex value
        Parameters
        • color - the name or hexcode of the color to display
        • width - width of the image to display, defaults to 200
        • height - height of the image to display, defaults to 90
        • show_hexcode - whether to display the hexcode of the color, defaults to True
        """
        file = io.BytesIO()
        Image.new("RGB", (width, height), color.to_rgb()).save(file, format="PNG")
        file.seek(0)
        if show_hexcode:
            em = discord.Embed(color=color, title=f"Showing Color: {str(color)}")
        elif show_hexcode == False or "false":
            em = discord.Embed(color=color)
        em.set_image(url="attachment://color.png")
        await ctx.send(file=discord.File(file, "color.png"), embed=em)

    @commands.command(name="emoji", aliases=["e"])
    async def _emoji(self, ctx, emoji: discord.Emoji, size: int = None):
        """displays an enlarged pic of the emoji
        Parameters
        • size - the size of the image to display
        • emoji - The name(case sensitive) or id of the emoji
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{emoji.url}" + f"?size={size if size else ' '}"
            ) as resp:
                image = await resp.read()
        if emoji.animated:
            with io.BytesIO(image) as file:
                await ctx.send(file=discord.File(file, "emote.gif"))
        else:
            with io.BytesIO(image) as file:
                await ctx.send(file=discord.File(file, "emote.png"))
        await ctx.message.delete()

    @commands.command()
    async def textreact(self, ctx, messageNo: typing.Optional[int] = 1, *, text):
        """reacts to a message with emojis corresponding to the text
        Parameter
        • messageNo - the number of the message to react to
        • text - the text to react with
        """
        text = (c for c in text.lower())
        emotes = {
            "a": "🇦",
            "b": "🇧",
            "c": "🇨",
            "d": "🇩",
            "e": "🇪",
            "f": "🇫",
            "g": "🇬",
            "h": "🇭",
            "i": "🇮",
            "j": "🇯",
            "k": "🇰",
            "l": "🇱",
            "m": "🇲",
            "n": "🇳",
            "o": "🇴",
            "p": "🇵",
            "q": "🇶",
            "r": "🇷",
            "s": "🇸",
            "t": "🇹",
            "u": "🇺",
            "v": "🇻",
            "w": "🇼",
            "x": "🇽",
            "y": "🇾",
            "z": "🇿",
        }
        for i, m in enumerate(await ctx.channel.history(limit=100).flatten()):
            if messageNo == i:
                for c in text:
                    await m.add_reaction(f"{emotes[c]}")
                break
        await ctx.message.delete()


    @commands.command(pass_context=True, aliases=['stream', 'watching', 'listening'])
    async def game(self, ctx, *, game: str = None):
#        bot_PREFIX = 
        """Set game/stream. Ex: [p]game napping [p]help game for more info

        Your game/stream status will not show for yourself, only other people can see it. This is a limitation of how the client works and how the api interacts with the client.

        --Setting playing/watching/listening--
        Set a game: [p]game <text>
        Set watching: [p]watching <text>
        Set listening: [p]listening <text>
        To set a rotating game status, do [p]game game1 | game2 | game3 | etc.
        It will then prompt you with an interval in seconds to wait before changing the game and after that the order in which to change (in order or random)
        Ex: [p]game with matches | sleeping | watching anime

        --Setting stream--
        Same as above but you also need a link to the stream. (must be a valid link to a stream or else the status will not show as streaming).
        Add the link like so: <words>=<link>
        Ex: [p]stream Underwatch=https://www.twitch.tv/a_seagull
        or [p]stream Some moba=https://www.twitch.tv/doublelift | Underwatch=https://www.twitch.tv/a_seagull"""
        is_stream = False
        if ctx.invoked_with == "game":
            message = "Playing"
            self.bot.status_type = discord.ActivityType.playing
        elif ctx.invoked_with == "stream":
            is_stream = True
            self.bot.status_type = discord.ActivityType.streaming
            self.bot.is_stream = True
        elif ctx.invoked_with == "watching":
            message = "Watching"
            self.bot.status_type = discord.ActivityType.watching
        elif ctx.invoked_with == "listening":
            message = "Listening to"
            self.bot.status_type = discord.ActivityType.listening
        if game:
            # Cycle games if more than one game is given.
            if ' | ' in game:
                await ctx.send(bot_PREFIX + 'Input interval in seconds to wait before changing (``n`` to cancel):')

                def check(msg):
                    return (msg.content.isdigit() or msg.content.lower().strip() == 'n') and msg.author == self.bot.user

                def check2(msg):
                    return (msg.content == 'random' or msg.content.lower().strip() == 'r' or msg.content.lower().strip() == 'order' or msg.content.lower().strip() == 'o') and msg.author == self.bot.user

                reply = await self.bot.wait_for("message", check=check)
                if not reply:
                    return
                if reply.content.lower().strip() == 'n':
                    return await ctx.send(bot_PREFIX + 'Cancelled')
                elif reply.content.strip().isdigit():
                    interval = int(reply.content.strip())
                    if interval >= 10:
                        self.bot.game_interval = interval
                        games = game.split(' | ')
                        if len(games) != 2:
                            await ctx.send(bot_PREFIX + 'Change in order or randomly? Input ``o`` for order or ``r`` for random:')
                            s = await self.bot.wait_for("message", check=check2)
                            if not s:
                                return
                            if s.content.strip() == 'r' or s.content.strip() == 'random':
                                await ctx.send(bot_PREFIX + '{status} set. {status} will randomly change every ``{time}`` seconds'.format(
                                                                status=message, time=reply.content.strip()))
                                loop_type = 'random'
                            else:
                                loop_type = 'ordered'
                        else:
                            loop_type = 'ordered'

                        if loop_type == 'ordered':
                            await ctx.send(bot_PREFIX + '{status} set. {status} will change every ``{time}`` seconds'.format(
                                                            status=message, time=reply.content.strip()))

                        stream = 'yes' if is_stream else 'no'
                        games = {'games': game.split(' | '), 'interval': interval, 'type': loop_type, 'stream': stream, 'status': self.bot.status_type}
                        with open('data/games.json', 'w') as g:
                            json.dump(games, g, indent=4)

                        self.bot.game = game.split(' | ')[0]

                    else:
                        return await ctx.send(bot_PREFIX + 'Cancelled. Interval is too short. Must be at least 10 seconds.')

            # Set game if only one game is given.
            else:
                self.bot.game_interval = None
                self.bot.game = game
                stream = 'yes' if is_stream else 'no'
                games = {'games': str(self.bot.game), 'interval': '0', 'type': 'none', 'stream': stream, 'status': self.bot.status_type}
                with open('data/games.json', 'w') as g:
                    json.dump(games, g, indent=4)
                if is_stream and '=' in game:
                    g, url = game.split('=')
                    await ctx.send(bot_PREFIX + 'Stream set as: ``Streaming %s``' % g)
                    await self.bot.change_presence(activity=discord.Streaming(name=g, url=url))
                else:
                    await ctx.send(bot_PREFIX + 'Game set as: ``{} {}``'.format(message, game))
                    await self.bot.change_presence(activity=discord.Activity(name=game, type=self.bot.status_type))

        # Remove game status.
        else:
            self.bot.game_interval = None
            self.bot.game = None
            self.bot.is_stream = False
            await self.bot.change_presence(activity=None)
            await ctx.send(bot_PREFIX + 'Set playing status off')
            if os.path.isfile('data/games.json'):
                os.remove('data/games.json')



def setup(bot):
    bot.add_cog(misc(bot))

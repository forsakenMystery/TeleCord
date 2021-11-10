from discord.ext.commands import Bot as BotBase
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Embed, File, Intents, Colour
from discord.ext.commands import Context
from datetime import datetime
from discord.ext.commands import CommandNotFound
from ..db import db
from apscheduler.triggers.cron import CronTrigger
from glob import glob
from asyncio import sleep
from discord.errors import HTTPException
from discord.ext.commands import CommandNotFound, BadArgument, MissingRequiredArgument
PREFIX = "^"
OWNER_IDS = [835543456453492767]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]
IGNORE_EXCEPTION = (CommandNotFound, BadArgument)

class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"{cog} cog ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.guild = None
        self.ready = False
        self.cogs_ready = Ready()
        self.scheduler = AsyncIOScheduler()
        # db.autosave(self.scheduler)
        # intents =Intents.default()
        # intents.members=True
        super().__init__(
            command_prefix=PREFIX,
            owner_id=OWNER_IDS,
            intents=Intents.all()
        )

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"{cog} cog loaded")
        print("setup complete")

    def run(self, version):
        self.VERSION = version
        print("running setup")
        self.setup()

        with open("./lib/bot/token", "r", encoding='utf-8') as tf:
            self.TOKEN = tf.read()

        print("running bot...")
        super().run(self.TOKEN, reconnect=True)

    async def print_message(self):
        await self.stdout.send("I am a timed notification")

    async def rules_reminder(self):
        channel = self.get_channel(817351764067614756)
        await channel.send("remember adhere to the rules!")

    async def on_connect(self):
        print("bot connected")

    async def on_disconnect(self):
        print("bot disconnected")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong")
        raise

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            await ctx.send("Wrong command")# you have to pass! you should pass!
        elif isinstance(exc, BadArgument):
            pass
        elif hasattr(exc, "original"):
            if isinstance(exc.original, HTTPException):
                await ctx.send("Unable to send message")
            elif isinstance(exc.original, Forbidden):
                await ctx.send("I don't have the permission")
            else:
                raise exc.original# not always we got original
        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(817351764067614750)
            self.scheduler.start()
            # self.scheduler.add_job(self.print_message, CronTrigger(second="0, 15, 30, 45"))
            self.stdout = self.get_channel(817351764067614756)

            # await self.stdout.send("Going Online!")
            # colour works with hex too 0xFF0000 be onvane adad

            # embed = Embed(title="Now Online!", description="TeleCord is Now Online.", colour=Colour.gold(), timestamp=datetime.utcnow())
            # fields = [("Name", "Value", True),
            #           ("Test field", "stick to each other", True),
            #           ("No", "non inliner", False),
            #           ]
            # for name, value, inline in fields:
            #     embed.add_field(name=name, value=value, inline=inline)# true means next to each other
            # embed.set_footer(text="footer test!")
            # embed.set_thumbnail(url=self.guild.icon_url)
            # embed.set_image(url=self.guild.icon_url)
            # embed.set_author(name="forsaken Mystery", icon_url=self.guild.icon_url)
            # await channel.send(embed=embed)# send message after setting flags
            #
            # await channel.send(file=File("./data/images/test.PNG"))

            while not self.cogs_ready.all_ready():
                await sleep(0.3)

            self.ready = True
            print("bot ready")
        else:
            print("bot reconnected")

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)
        if ctx.command is not None and ctx.guild is not None:  # not in dm
            if self.ready:
                await self.invoke(ctx)
        if not self.ready:
            await ctx.send("I'm not ready yet to receive")

    async def on_message(self, message):
        # self.process_commands(message) # react every message
        if not message.author.bot:
            await self.process_commands(message)


bot = Bot()
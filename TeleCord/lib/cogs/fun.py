from discord.ext.commands import Cog
from discord.ext.commands import command
from random import choice, randint
from discord import Member
from typing import Optional
from discord.errors import HTTPException


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="cmd", aliases=["command", "c"], hidden=True)
    async def some_amazing_command(self, ctx):
        pass

    @command(name="hello", aliases=["hi"])
    async def say_hello(self, ctx):
        await ctx.send(f"{choice(('Hello', 'Hey', 'Hi', 'Yellow'))} {ctx.author.mention}!")

    @command(name="dice", aliases=["roll"])
    async def roll_dice(self, ctx, die: str):
        dice, value = (int(term) for term in die.split("d")) # ^roll 5d6
        if dice*value <= 900:
            rolls = [randint(1, value) for i in range(dice)]

            await ctx.send("+".join(str(r) for r in rolls)+f" = {sum(rolls)}")
        else:
            await ctx.send("Too much dice! what are you doing?")

    # @roll_dice.error
    # async def roll_dice_error(self, ctx, exc):
    #     if isinstance(exc.original, HTTPException):
    #         await ctx.send(f"Too many dice rolled. Please try a lower Number.")

    @command(name="slap", aliases=["hit"])
    async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "being An"):
        await ctx.send(f"{ctx.author.display_name} slapped {member.mention} for {reason}!")
        # mitone nick bashe ke nick name fail mishe age set nakarde bashe

    @slap_member.error
    async def slap_member_error(self, ctx, exc):
        if isinstance(exc, BadArgument):
            await ctx.send("I cannot find this member.")

    @command(name="echo", aliases=["say"])
    async def echo_message(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(f"{message}")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")
        # await self.bot.stdout.send("Fun Cog ready.")
        print("Fun Cog ready!")

    @Cog.listener()
    async def on_message(self, msg):
        pass


def setup(bot):
    bot.add_cog(Fun(bot))
    # bot.scheduler.add_job(...)
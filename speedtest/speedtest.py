import discord
from redbot.core.bot import Red
from redbot.core import commands, checks
from redbot.core.utils.chat_formatting import box

import json
import contextlib
import subprocess
from datetime import datetime
from humanize import naturalsize


class Speedtest(commands.Cog):
    """Speedtest for your bot's server."""

    __version__ = "1.1"
    __author__ = ["Colt#0001", "Dinnerb0ne#2067", "Predä 。#1001"]

    def __init__(self, bot: Red):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthor: {', '.join(self.__author__)}\nCog Version: {self.__version__}"

    def _speedtest(self):
        with subprocess.Popen(
            ["speedtest --format json"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        ) as resp:
            return resp.communicate()

    @checks.is_owner()
    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def speedtest(self, ctx: commands.Context, edit: bool = True):
        """
        Runs a speedtest and prints the result.

        Needs to install Ookla's speedtest package from https://www.speedtest.net/apps/cli
        Use `[p]speedtest false` if you want the result in a new message.
        """
        em = discord.Embed(
            color=await ctx.embed_colour(), title="Running speedtest ... This may take a while! ⏱",
        )
        msg = await ctx.send(embed=em)
        result = await self.bot.loop.run_in_executor(None, self._speedtest)
        if result[1]:
            em.color = discord.Color.dark_red()
            em.title = (
                "Failed to get a speedtest result.\n"
                "Please make sure to follow the installation instructions at: https://www.speedtest.net/apps/cli"
            )
            return await msg.edit(embed=em)
        result = json.loads(result)
        embed = discord.Embed(
            color=0x10A714,
            title="Your speedtest results are:",
            description=(
                box(
                    f"Server   : {result['server']['name']} - {result['server']['location']}\n"
                    f"ISP      : {result['isp']}\n"
                    f"Latency  : {round(result['ping']['latency'], 2)}ms ({round(result['ping']['jitter'], 2)}ms jitter)\n"
                    f"Download : {naturalsize(result['download']['bandwidth'] * 8)}ps\n"
                    f"Upload   : {naturalsize(result['upload']['bandwidth'] * 8)}ps\n"
                    f"Packet loss: {float(result['packetLoss'])}%",
                    lang="py",
                )
            ),
        )
        embed.set_image(url=f"{result['result']['url']}.png")
        embed.set_footer(text=datetime.now().strftime("Server time: %d-%m-%Y  %H:%M:%S"))
        if not edit:
            with contextlib.suppress(discord.NotFound):
                await msg.delete()
            return await ctx.send(embed=embed)
        await msg.edit(embed=embed)

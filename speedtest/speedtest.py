import discord
from redbot.core.bot import Red
from redbot.core import commands, checks
from redbot.core.utils.chat_formatting import box

from datetime import datetime
import re
import contextlib
import subprocess

DOWNLOAD_RE = re.compile(r"Download: ([\d.]+) .bit", re.I)
UPLOAD_RE = re.compile(r"Upload: ([\d.]+) .bit", re.I)
PING_RE = re.compile(r"([\d.]+) ms", re.I)
IMG_RE = re.compile(r"(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|gif|png)", re.I)


class Speedtest(commands.Cog):
    """Speedtest for your bot's server"""

    def __init__(self, bot: Red):
        self.bot = bot

    def _speedtest(self):
        with subprocess.Popen(
            ["speedtest-cli --share"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
        ) as resp:
            return str(resp.communicate())

    @checks.is_owner()
    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def speedtest(self, ctx: commands.Context, edited: bool = True):
        """
        Runs a speedtest and prints the result.

        Use `[p]speedtest false` if you want the result in a new message.
        """
        try:
            em = discord.Embed(
                color=await ctx.embed_colour(),
                title="⏱ Running speedtest ... This may take a while! ⏱",
            )
            msg = await ctx.send(embed=em)
            speedtest_result = await self.bot.loop.run_in_executor(None, self._speedtest)
            download = float(DOWNLOAD_RE.search(speedtest_result).group(1))
            upload = float(UPLOAD_RE.search(speedtest_result).group(1))
            ping = float(PING_RE.search(speedtest_result).group(1))
            img = str(IMG_RE.search(speedtest_result).group(0))
            embed = discord.Embed(color=0x10A714, title="Your speedtest results are:")
            embed.add_field(name="Ping", value=box(f"{ping} ms", lang="py"))
            embed.add_field(name="Download", value=box(f"{download} mbps", lang="py"))
            embed.add_field(name="Upload", value=box(f"{upload} mbps", lang="py"))
            embed.set_image(url=img)
            embed.set_footer(text=datetime.now().strftime("Server time: %d-%m-%Y  %H:%M:%S"))
            if not edited:
                with contextlib.suppress(discord.NotFound):
                    await msg.delete()
                return await ctx.send(embed=embed)
            await msg.edit(embed=embed)
        except KeyError as error:
            await ctx.send(f"An error occured.\n{error}")

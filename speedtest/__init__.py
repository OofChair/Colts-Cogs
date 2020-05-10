from redbot.core.bot import Red
from .speedtest import Speedtest


def setup(bot: Red):
    cog = Speedtest(bot)
    bot.add_cog(cog)

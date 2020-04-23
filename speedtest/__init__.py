from .speedtest import Speedtest


def setup(bot):
    cog = Speedtest(bot)
    bot.add_cog(cog)

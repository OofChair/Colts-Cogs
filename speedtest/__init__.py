from .speedtest import Speedtest


def setup(bot):
    try:
        import speedtest
    except ImportError:
        raise ImportError("Failed to import speedtest-cli. Please do pip install speedtest-cli.")
    cog = Speedtest(bot)
    bot.add_cog(cog)

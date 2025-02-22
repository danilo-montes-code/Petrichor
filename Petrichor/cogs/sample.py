"""sample.py

Boilerplate Cog code.
"""

from discord.ext import commands


class SampleCog(commands.Cog):
    """
    Cog that holds commands.

    Attributes
    ----------
    bot : commands.Bot
        bot that the commands belong to
    """

    def __init__(self, bot : commands.Bot):
        """
        Creates an instance of the SampleCog class.

        Parameters
        ----------
        bot : commands.Bot
            bot that the commands belong to
        """
        self.bot = bot



async def setup(bot : commands.Bot) -> None:
    """
    Sets up the Cog.

    Parameters
    ----------
    bot : commands.Bot
        the bot to add the cog to
    """
    await bot.add_cog(SampleCog(bot))

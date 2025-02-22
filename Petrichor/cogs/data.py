"""data.py

Contains the Cog that holds commands whose main focus is CRUD operations.
"""

from discord.ext import commands


class DataCog(commands.Cog):
    """
    Cog that holds commands whose main focus is CRUD operations.

    Attributes
    ----------
    bot : commands.Bot
        bot that the commands belong to
    """

    def __init__(self, bot : commands.Bot):
        """
        Creates an instance of the DataCog class.

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
    await bot.add_cog(DataCog(bot))

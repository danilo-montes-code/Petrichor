"""data.py

Contains the Cog that holds commands whose main focus is CRUD operations.
"""

from discord.ext import commands
from discord import app_commands
import discord

from discord import (
    Interaction,
    Member,
    Guild
)
from asyncpg import Record

from Petrichor.PetrichorBot import PetrichorBot


class DataCog(commands.Cog):
    """
    Cog that holds commands whose main focus is CRUD operations.

    Attributes
    ----------
    bot : PetrichorBot
        bot that the commands belong to
    """

    def __init__(self, bot : PetrichorBot):
        """
        Creates an instance of the DataCog class.

        Parameters
        ----------
        bot : PetrichorBot
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

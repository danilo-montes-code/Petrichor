"""PetrichorBot.py

Contains a class that represents the Petrichor bot.
"""

import discord
from discord.ext import commands

from util.printing import print_petrichor_msg
from Petrichor.cogs import EXTENSIONS

import os

from util.db_connection_manager import DatabaseConnectionManager



class PetrichorBot(commands.Bot):
    """
    Class that contains functionality for the Petrichor Discord bot.

    Attributes
    ----------
    db_conn : DatabaseConnectionManager
        class that manages the connection to the database
    """

    def __init__(
        self, 
        db_conn : DatabaseConnectionManager, 
        *args, **kwargs
    ):
        """
        Initializes the PetrichorBot instance.

        Parameters
        ----------
        db_conn : DatabaseConnectionManager
            the database connection object
        """

        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(
            command_prefix=os.getenv('PREFIX'),
            intents=intents,
            *args, **kwargs
        )

        self.db = db_conn

    
    async def on_ready(self):
        """
        Runs when the bot has connected to Discord.
        """

        print_petrichor_msg(f'User {self.user} online')

    
    async def setup_hook(self):
        """
        Sets up bot Cogs, database connection, 
        and any other necessary functions.
        """

        await self._setup_cogs()
        await self._ping_db()
        # await self.cogs['RemindersCog'].setup_dle_reminders()


    async def _setup_cogs(self) -> None:
        """
        Sets up the Cogs.
        """

        for extension in EXTENSIONS:
            await self.load_extension(extension)
            print_petrichor_msg(f'Loaded extension: {extension}')

    
    async def _ping_db(self) -> None:
        """
        Pings the database, done to simply verify database connection.
        """
        print_petrichor_msg('pinging tables...')
        await self.db.ping_tables()

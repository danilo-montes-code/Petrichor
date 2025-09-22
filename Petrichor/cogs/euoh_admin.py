"""eouh_dev.py

Contains the Cog that holds commands for euoh-related dev commands.
"""
from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from util.env_vars import get_id

from typing import TYPE_CHECKING
if TYPE_CHECKING:
   from discord import (
        Interaction,
    )
   
   from Petrichor.PetrichorBot import PetrichorBot



class EuohDevCog(commands.Cog):
    """
    Cog that holds commands that holds commands for euoh-related dev commands.

    Attributes
    ----------
    bot : PetrichorBot
        bot that the commands belong to
    """

    def __init__(self, bot : PetrichorBot):
        """
        Creates an instance of the EouhDevCog class.

        Parameters
        ----------
        bot : PetrichorBot
            bot that the commands belong to
        """
        self.bot = bot


    euoh = app_commands.Group(
        name='euoh',
        description='Contains commands related to euohs.'
    )

    @euoh.command(
        name='lock',
        description='Locks the euoh command system.'
    )
    async def lock(
        self,
        interaction : Interaction
    ) -> None:
        """
        Locks the euoh command system.

        Parameters
        ----------
        interaction : Interaction
            interaction that triggered the command
        """
        
        if self.bot.euoh_locked:
            await interaction.response.send_message('The euoh command system is already locked.')
            return
        
        self.bot.euoh_locked = True
        await self.bot.reload_extension('Petrichor.cogs.euoh')
        await interaction.response.send_message('Euoh command system locked.')


    @euoh.command(
        name='unlock',
        description='Unlocks the euoh command system.'
    )
    async def unlock(
        self,
        interaction : Interaction
    ) -> None:
        """
        Unlocks the euoh command system.

        Parameters
        ----------
        interaction : Interaction
            interaction that triggered the command
        """
        
        if not self.bot.euoh_locked:
            await interaction.response.send_message('The euoh command system is already unlocked.')
            return
        
        self.bot.euoh_locked = False
        await self.bot.reload_extension('Petrichor.cogs.euoh')
        await interaction.response.send_message('Euoh command system unlocked.')
        


async def setup(bot : commands.Bot) -> None:
    """
    Sets up the Cog.

    Parameters
    ----------
    bot : commands.Bot
        the bot to add the cog to
    """
    bot : PetrichorBot

    await bot.add_cog(
        EuohDevCog(bot),
        guild=discord.Object(id=get_id('FANTA_ID'))
    )

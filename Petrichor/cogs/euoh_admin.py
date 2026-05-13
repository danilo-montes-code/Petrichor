"""eouh_dev.py

Contains the Cog that holds commands for euoh-related dev commands.
"""
from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands
from discord import Member, Guild

from util.env_vars import get_id
from util.config import VC_EUOH_TYPES

from typing import TYPE_CHECKING
if TYPE_CHECKING:
   from discord import (
        Interaction
    )
   
   from Petrichor.PetrichorBot import PetrichorBot



class EuohAdminCog(commands.Cog):
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
        


    vc_euoh = app_commands.Group(
        name='vc',
        description='Contains commands related to euoh in vc',
        parent=euoh
    )


    @vc_euoh.command(
        name='add-count',
        description='Adds a specified number of vc euohs of a given type to a user.'
    )
    async def add_count(
        self,
        interaction : Interaction,
        server_id : str,
        euoh_recipient_id : str,
        euoh_type : VC_EUOH_TYPES,
        count : int
    ) -> None:
        """
        Adds a specified number of euohs of a given type to a user.

        Parameters
        ----------
        interaction : Interaction
            interaction that triggered the command
        server_id : str
            id of the server the recipient is in
        euoh_recipient_id : str
            id of the member to give the euoh to
        euoh_type : Literal['scuzz', 'kaeley', 'declan', 'armando', 'max moment', 'max yapment']
            type of euoh to give
        count : int
            number of euohs to give
        """

        if self.bot.euoh_locked:
            await interaction.response.send_message('The euoh command system is currently locked. Please try again later.')
            return

        server : Guild = self.bot.get_guild(int(server_id))
        if server is None:
            await interaction.response.send_message('Server not found.')
            return
        
        member : Member = server.get_member(int(euoh_recipient_id))
        if member is None:
            await interaction.response.send_message('Member not found in the specified server.')
            return
        
        for i in range(count):
            print(f"Adding euoh {i+1}/{count}...")
            inserted_successfully = await self.bot.db.insert_row(
                table_name='vc_euohs',
                record_info=[
                    member.id,
                    euoh_type,
                    interaction.user.id,
                    server.id,
                    interaction.created_at
                ]
            )

            if not inserted_successfully:
                await interaction.response.send_message('An error occurred while adding the euohs. Please try again later.')
                return
            
        await interaction.response.send_message('Euohs added successfully')



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
        EuohAdminCog(bot),
        guild=discord.Object(id=get_id('FANTA_ID'))
    )

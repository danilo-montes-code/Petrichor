"""eouh.py

Contains the Cog that holds commands for euoh-related commands.
"""
from __future__ import annotations

from discord import app_commands
from discord.ext import commands
from discord import Member

from typing import Literal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from discord import Interaction
    from asyncpg import Record

    from Petrichor.PetrichorBot import PetrichorBot



class EuohCog(commands.Cog):
    """
    Cog that holds commands that holds commands for euoh-related commands.

    Attributes
    ----------
    bot : PetrichorBot
        bot that the commands belong to
    """

    def __init__(self, bot : PetrichorBot):
        """
        Creates an instance of the EouhCog class.

        Parameters
        ----------
        bot : PetrichorBot
            bot that the commands belong to
        """
        self.bot = bot
        self.locked = False


    euoh = app_commands.Group(
        name='euoh',
        description='Contains commands related to euoh'
    )

    vc_euoh = app_commands.Group(
        name='vc',
        description='Contains commands related to euoh in vc',
        parent=euoh
    )

    @vc_euoh.command(
        name='add',
        description='Adds a given type of vc euoh to the person mentioned.'
    )
    async def vc_euohs_add(
        self,
        interaction : Interaction,
        euoh_recipient : Member,
        euoh_type : Literal[
            'scuzz',
            'kaeley', 
            'declan', 
            'armando'
        ]
    ) -> None:
        """
        Adds a given type of vc euoh to the person mentioned.

        Parameters
        ----------
        interaction : Interaction
            interaction that triggered the command
        euoh_recipient : Member
            member to give the euoh to
        euoh_type : Literal['scuzz', 'kaeley', 'declan', 'armando']
            type of euoh to give
        """

        if self.bot.euoh_locked:
            await interaction.response.send_message('The euoh command system is currently locked. Please try again later.')
            return
        
        inserted_successfully = await self.bot.db.insert_row(
            table_name='vc_euohs',
            record_info=[
                euoh_recipient.id,
                euoh_type,
                interaction.user.id,
                interaction.guild_id,
                interaction.created_at
            ]
        )

        if not inserted_successfully:
            await interaction.response.send_message(
                'There was an error adding the euoh. Please try again later.'
            )
            return
        
        await interaction.response.send_message("euohhhhh")


    @vc_euoh.command(
        name='get',
        description='Gets the number of vc euohs a user has.'
    )
    async def vc_euohs_get(
        self,
        interaction : Interaction,
        euoh_recipient : Member
    ) -> None:
        """
        Displays the number of VC Meuohments a user has.

        Parameters
        ----------
        interaction : Interaction
            interaction that triggered the command
        euoh_recipient : Member
            member to get the VC Meuohment counts of
        """
        
        euoh_type_counts : list[Record] = await self.bot.db.fetch_rows(
            table_name='vc_euohs',
            columns=['COUNT(*) euoh_count', 'euoh_type'],
            group_by='euoh_type',
            where=f"guild_id = '{interaction.guild_id}' AND recipient_id = '{euoh_recipient.id}'",
        )

        if not euoh_type_counts:
            await interaction.response.send_message(
                f'No VC euohs for {euoh_recipient.display_name} were found (yet...).'
            )


        individual_vc_euoh_counts : list[str] = []
        
        for euoh_type_count in euoh_type_counts:
            euoh_type : str = euoh_type_count['euoh_type']
            euoh_count : int = euoh_type_count['euoh_count']

            msg = (
                f"{euoh_count} {euoh_type.title()} "
                f"Meuohment{'s' if euoh_count != 1 else ''}"
            )
            individual_vc_euoh_counts.append(msg)


        response = \
            f'# {euoh_recipient.display_name} VC Meuohments\n- ' + \
            '\n- '.join(individual_vc_euoh_counts)

        await interaction.response.send_message(response)



async def setup(bot : commands.Bot) -> None:
    """
    Sets up the Cog.

    Parameters
    ----------
    bot : commands.Bot
        the bot to add the cog to
    """
    bot : PetrichorBot

    await bot.add_cog(EuohCog(bot))

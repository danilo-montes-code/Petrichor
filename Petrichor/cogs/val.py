"""val.py

Contains the Cog that holds commands related to valentine.
"""
from __future__ import annotations

from discord.ext import commands
from discord import app_commands

from util.env_vars import get_dict
from util.printing import print_petrichor_msg, print_petrichor_error

import re

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from discord import (
        Interaction,
        Message,
        Reaction,
        User
    )
    from asyncpg import Record

    from Petrichor.PetrichorBot import PetrichorBot

    from datetime import timedelta


SIDE_EYE_EMOTE_IDS = [
    1390943526572789821,
    1355315035638862084,
    1440555333260148776,
    1440555109527326771,
    1419431577984831540,
    1411431528336195675,
    1417348512601083997,
    1417349672007106631,
    1391935545676136508
]
VAL_ID : int = int(
    get_dict('FRIEND_IDS')[
        get_dict('FRIEND_NAMES')['VALENTINE']
    ]
)


class ValCog(commands.Cog):
    """
    Cog that holds commands related to valentine.

    Attributes
    ----------
    bot : PetrichorBot
        bot that the commands belong to
    """

    def __init__(self, bot : PetrichorBot):
        """
        Creates an instance of the ValCog class.

        Parameters
        ----------
        bot : PetrichorBot
            bot that the commands belong to
        """
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message : Message):
        """
        Event listener that reacts to all messages.

        Parameters
        ----------
        message : Message
            the message that was sent
        """

        await self.check_for_side_eye(message)

        await self.bot.process_commands(message)


    @commands.Cog.listener()
    async def on_reaction_add(
        self, 
        reaction : Reaction, 
        user : User
    ) -> None:
        """
        Not even reactions are safe hehehehehe.

        Parameters
        ----------
        reaction : Reaction
            the current state of the reaction
        user : User
            the user who added the reaction
        """
        
        if user.id != VAL_ID:
            return
        
        if reaction.emoji.id not in SIDE_EYE_EMOTE_IDS:
            return
        
        inserted_successfully = await self.bot.db.insert_row(
            table_name='val_side_eyes',
            record_info=[
                reaction.message.id,
                reaction.emoji.id,
                False,
                reaction.message.guild.id,
                reaction.message.created_at
            ]
        )

        if not inserted_successfully:
            print_petrichor_error('Failed to log valentine side eye emoji reaction.')
            return

        print_petrichor_msg(
            f'Logged side eye emoji reaction from valentine with id {reaction.emoji.id}.'
        )
    

    async def check_for_side_eye(
        self,
        message : Message
    ) -> None:
        """
        Checks if valentine sends a side eye emoji, and logs it if so.

        Parameters
        ----------
        message : Message
            the message that was sent
        """

        if message.author.id != VAL_ID:
            return
        
        side_eye_id = self._side_eye_emoji_in_message(message.content)

        if not side_eye_id:
            return
        
        inserted_successfully = await self.bot.db.insert_row(
            table_name='val_side_eyes',
            record_info=[
                message.id,
                side_eye_id,
                True,
                message.guild.id,
                message.created_at
            ]
        )

        if not inserted_successfully:
            print_petrichor_error('Failed to log valentine side eye emoji message.')
            return
        
        print_petrichor_msg(
            f'Logged side eye emoji message from valentine with id {side_eye_id}.'
        )


    def _side_eye_emoji_in_message(
        self,
        message : str
    ) -> int | None:
        """
        Checks if a side eye emoji is in the message.

        Parameters
        ----------
        message : str
            the message to check

        Returns
        -------
        int | None
            id of the side eye emoji if found, 
            otherwise None
        """

        for emote_id in SIDE_EYE_EMOTE_IDS:
            emote_regex = re.compile(f'<:.*:{emote_id}>')
            if re.search(emote_regex, message):
                return emote_id
        
        return None


    @app_commands.command(
        name='days-since-last-side-eye',
        description=(
            'Gets the number of days since valentine last sent a '
            'side eye emote or reaction.'
        )
    )
    async def days_since_last_side_eye(self, interaction : Interaction):
        last_side_eye : Record = await self.bot.db.fetch_rows(
            table_name='val_side_eyes',
            where=f"guild_id = '{interaction.guild_id}'",
            order_by='message_time',
            order_by_ascending=False,
            limit=1
        )

        if not last_side_eye:
            await interaction.response.send_message(
                'Apparently val has never sent a side eye emote or reaction '
                'in this server (this simply can not be true)'
            )
            return
        
        last_side_eye = last_side_eye[0]
        
        time_delta : timedelta = interaction.created_at - last_side_eye['message_time']

        days = time_delta.days

        td_seconds = time_delta.seconds
        seconds = td_seconds % 60
        minutes = td_seconds // 60

        td_seconds //= 60
        minutes = td_seconds % 60
        hours = td_seconds // 60

        await interaction.response.send_message(
            f"It has been "
            f"{days} day{'s' if days != 1 else ''}, "
            f"{hours} hour{'s' if hours != 1 else ''}, "
            f"{minutes} minute{'s' if minutes != 1 else ''}, and "
            f"{seconds} second{'s' if seconds != 1 else ''} "
            f"since valentine last sent a side eye emoji."
        )

    
    @app_commands.command(
        name='longest-side-eye-drought',
        description=(
            'Gets the longest number of days where valentine went '
            'without sending a side eye emote or reaction.'
            )
    )
    async def longest_side_eye_drought(self, interaction : Interaction):
        await interaction.response.send_message(
            "soon... (tm)"
        )



async def setup(bot : commands.Bot) -> None:
    """
    Sets up the Cog.

    Parameters
    ----------
    bot : commands.Bot
        the bot to add the cog to
    """
    await bot.add_cog(ValCog(bot))

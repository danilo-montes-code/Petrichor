"""boys_who_cried.py

Contains the Cog that holds the boys who cried functionality.
"""
from __future__ import annotations

from datetime import datetime, timezone

from discord.ext import commands
from discord import (
    app_commands,
    Member,
    Message, 
    Reaction,
    User
)

from util.printing import print_petrichor_error, print_petrichor_msg

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from discord import (
        Interaction,
    )
    from asyncpg import Record

    from Petrichor.PetrichorBot import PetrichorBot



class BoysWhoCried(commands.Cog):
    """
    Cog that holds the boys who cried functionality.

    Attributes
    ----------
    bot : PetrichorBot
        bot that the commands belong to
    """

    def __init__(self, bot : PetrichorBot):
        """
        Creates an instance of the BoysWhoCried class.

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

        await self.check_for_israel_flag(message)

        await self.bot.process_commands(message)


    @commands.Cog.listener()
    async def on_reaction_add(
        self, 
        reaction : Reaction, 
        user : User
    ) -> None:
        """
        Checks for added reactions.


        Parameters
        ----------
        reaction : Reaction
            the current state of the reaction
        user : User
            the user who added the reaction
        """

        if str(reaction.emoji) != '🇮🇱':
            return

        inserted_successfully = await self.bot.db.insert_row(
            table_name='boys_who_cried',
            record_info=[
                reaction.message.guild.id,
                reaction.message.channel.id,
                reaction.message.id,
                user.id,
                False,
                datetime.now(timezone.utc).astimezone()
            ]
        )

        if not inserted_successfully:
            print_petrichor_error('Failed to log israel flag emoji reaction.')
            return

        print_petrichor_msg(
            f'Logged israel flag emoji reaction from user {user.display_name}.'
        )


    async def check_for_israel_flag(
        self,
        message : Message
    ) -> None:
        """
        Checks if someone sends an israel flag emoji in a message, and logs it if so.


        Parameters
        ----------
        message : Message
            the message that was sent
        """

        israel_flag_in_msg = self._israel_flag_emoji_in_message(message.content)

        if not israel_flag_in_msg:
            return

        inserted_successfully = await self.bot.db.insert_row(
            table_name='boys_who_cried',
            record_info=[
                message.guild.id,
                message.channel.id,
                message.id,
                message.author.id,
                True,
                message.created_at
            ]
        )

        if not inserted_successfully:
            print_petrichor_error('Failed to log israel flag emoji message.')
            return

        print_petrichor_msg(
            f'Logged israel flag emoji message from user {message.author.display_name}.'
        )


    def _israel_flag_emoji_in_message(
        self,
        message : str
    ) -> bool:
        """
        Checks if an israel flag emoji is in the message.


        Parameters
        ----------
        message : str
            the message to check

        Returns
        -------
        bool
            True, if an israel flag emoji is in the message |
            False, otherwise
        """
        return '🇮🇱' in str(message)


    @app_commands.command(
        name='the-boy-who-cried-israel',
        description='Get the counts of israel reacts to messages in the server.'
    )
    async def the_boy_who_cried_israel(self, interaction : Interaction) -> None:
        """
        Gets the counts of times users in the server have reacted to messages
        with the israel flag emoji.


        Parameters
        ----------
        interaction : Interaction
            the interaction that evoked the command
        """

        those_who_cried_records : list[Record] = await self.bot.db.fetch_rows(
            table_name='boys_who_cried',
            where=f"guild_id = '{interaction.guild.id}'",
            order_by='user_id'
        )

        if not those_who_cried_records:
            await interaction.response.send_message(
                content='No one has reacted to any messages with the israel flag emoji yet...'
            )
            return
        
        
        server = interaction.guild
        current_user_id = -1
        current_user = None
        those_who_cried : dict[Member, int] = {}

        for record in those_who_cried_records:

            if current_user_id != int(record['user_id']):

                current_user_id = int(record['user_id'])

                if not (check_member := server.get_member(current_user_id)):
                    # the user might have left the server
                    continue

                current_user = check_member
            
            those_who_cried[current_user] = \
                those_who_cried.get(current_user, 0) + 1


        those_who_cried = dict(sorted(those_who_cried.items(), key=lambda name: name[1], reverse=True))
        msg = '# Boys Who Cried Israel\n- '
        msg += '\n- '.join([
                    f'{member.display_name}: {count} times'
                    for member, count 
                    in those_who_cried.items()
                ])
        
        await interaction.response.send_message(
            content=msg
        )



async def setup(bot : commands.Bot) -> None:
    """
    Sets up the Cog.

    Parameters
    ----------
    bot : commands.Bot
        the bot to add the cog to
    """
    await bot.add_cog(BoysWhoCried(bot))

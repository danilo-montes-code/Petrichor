"""roll_the_ping.py

Contains the Cog that holds commands related to `/rtp`.
"""

from discord.ext import commands
from discord import app_commands

import random

from discord import (
    Interaction,
    Member,
    Guild,
    InteractionCallbackResponse
)
from asyncpg import Record

from Petrichor.PetrichorBot import PetrichorBot



class RollThePingCog(commands.Cog):
    """
    Cog that holds commands related to `/rtp`.

    Attributes
    ----------
    bot : PetrichorBot
        bot that the commands belong to
    """

    def __init__(self, bot : PetrichorBot):
        """
        Creates an instance of the RollThePingCog class.

        Parameters
        ----------
        bot : PetrichorBot
            bot that the commands belong to
        """
        self.bot = bot

    ping_counts = app_commands.Group(
        name='ping-counts',
        description='Contains commands related to fetching /rtp data'
    )



    @app_commands.command(
        name='rtp',
        description='Chooses a random active member to ping :D'
    )
    async def roll_the_ping(self, interaction : Interaction):
        """
        Picks a random active member and pings them. Makes a record of the ping
        as well.

        Parameters
        ----------
        interaction : Interaction
            the interaction that evoked the command
        """

        role_havers : list[Member] = []

        for member in interaction.guild.members:

            role_names : list[str] = [role.name.lower() for role in member.roles]

            if member.bot or "has no interesting roles" in role_names:
                continue

            role_havers.append(member)

        ping_victim = random.choice(role_havers)

        bot_response : InteractionCallbackResponse
        bot_response = await interaction.response.send_message(
            f"By fate, {interaction.user.display_name} has pinged {ping_victim.mention}. Congrats!"
        )

        await self.bot.db.insert_row(
            table_name='roll_the_pings',
            record_info=[
                bot_response.message_id,
                interaction.user.id,
                ping_victim.id,
                interaction.guild_id,
                interaction.created_at
            ]
        )

    
    @ping_counts.command(
        name='victim',
        description='Get the ranking of ping victims'
    )
    async def get_ping_victim_counts(
        self, 
        interaction : Interaction,
        count : int = 5,
        reverse : bool = False
    ) -> None:
        """
        Displays the count of `/rtp` ping receivers in the server. 
        Ordered in descending order by default.

        Parameters
        ----------
        interaction : Interaction
            the interaction that evoked the command
        count : int, default = 5
            the number of people whose rankings to show 
            (input 0 for full guild ranking)
        reverse : bool, default = False
            if False, display results in descending order (most to least) |
            if True, display results in ascending order
        """

        response = await self._get_ping_counts(
            perpetrator=False,
            interaction=interaction,
            count=count,
            reverse=reverse
        )

        await interaction.response.send_message(response)


    @ping_counts.command(
        name='perpetrator',
        description='Get the ranking of ping perpetrators'
    )
    async def get_ping_perpetrator_counts(
        self, 
        interaction : Interaction,
        count : int = 5,
        reverse : bool = False
    ) -> None:
        """
        Displays the count of `/rtp` command runners in the server. 
        Ordered in descending order by default.

        Parameters
        ----------
        interaction : Interaction
            the interaction that evoked the command
        count : int, default = 5
            the number of people whose rankings to show 
            (input 0 for full guild ranking)
        reverse : bool, default = False
            if False, display results in descending order (most to least) |
            if True, display results in ascending order
        """

        response = await self._get_ping_counts(
            perpetrator=True,
            interaction=interaction,
            count=count,
            reverse=reverse
        )

        await interaction.response.send_message(response)

    
    async def _get_ping_counts(
        self,
        perpetrator : bool,
        interaction : Interaction,
        count : int,
        reverse : bool
    ) -> str:
        """
        Fetches the count of `/rtp` command uses in the current server, 
        either fetching the perpetrator or victim counts, and returns the
        formatted response. Rankings ordered in descending order by default.
        
        Parameters
        ----------
        perpetrator : bool
            if True, fetches ping perpetrator counts |  
            if False, fetches ping victim counts

        interaction : Interaction
            the interaction that evoked the command

        count : int
            the number of people whose rankings to show 
            (input 0 for full guild ranking)

        reverse : bool
            if False, display results in descending order (most to least) |  
            if True, display results in ascending order
        
        Returns
        -------
        str
            the formatted ranking
        """

        if count < 0: 
            return (
                'Please input a `count` greater than 0, '
                'or 0 to list all relevant server members.'
            )

        rtp_user_type = 'Perpetrator' if perpetrator else 'Victim'
        rtp_user_column_name = 'pinger_id' if perpetrator else 'pingee_id'

        rows : list[Record] = await self.bot.db.fetch_rows(
            table_name='roll_the_pings',
            columns=['COUNT(*) pings', rtp_user_column_name],
            group_by=rtp_user_column_name,
            order_by='pings',
            order_by_ascending=reverse,
            where=f"guild_id = '{interaction.guild_id}'"
        )

        if not rows:
            return 'No applicable records for the search were found.'

        guild : Guild = self.bot.get_guild(interaction.guild_id)

        response = ''

        member_count = 0
        for row in rows:

            # handle `count` check here, rather than passing LIMIT in the SQL
            # query, for cases where users fetched in the query have left the
            # server, and thus offset the returned member count by 1 per user
            if count != 0 and member_count == count:
                break

            member : Member = guild.get_member(int(row[rtp_user_column_name]))
            if not member: continue

            response += (
                f'{member_count+1}. {member.display_name} '
                f'(pinged {row['pings']} times)\n'
            )
            member_count += 1

        if member_count == 0:
            return (
                f'No Ping {rtp_user_type}s were found with the given search.'
            )

        title = '## '
        ranking_order = 'Top' if not reverse else 'Bottom'

        if count:
            title += (
                f'{ranking_order} {member_count} '
                f'Ping {rtp_user_type}{"s" if member_count != 1 else ""} '
                f'in {guild.name}\n'
            )
        else:
            title += (
                f'All Ping {rtp_user_type}s in {guild.name}'
                f'{" in reverse order" if reverse else ""}\n'
            )

        response = title + '\n' + response[:-1]
        return response



async def setup(bot : commands.Bot) -> None:
    """
    Sets up the Cog.

    Parameters
    ----------
    bot : commands.Bot
        the bot to add the cog to
    """
    await bot.add_cog(RollThePingCog(bot))

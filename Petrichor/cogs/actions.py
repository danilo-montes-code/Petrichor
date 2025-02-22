"""actions.py

Contains the Cog that holds commands that perform actions.
"""

from discord import app_commands
from discord.ext import commands

import random

from discord import (
    Interaction,
    Member
)

class ActionsCog(commands.Cog):
    """
    Cog that holds commands that perform actions.

    Attributes
    ----------
    bot : commands.Bot
        bot that the commands belong to
    """

    def __init__(self, bot : commands.Bot):
        """
        Creates an instance of the ActionsCog class.

        Parameters
        ----------
        bot : commands.Bot
            bot that the commands belong to
        """
        self.bot = bot


    @app_commands.command(
        name='rtp',
        description='Chooses a random active member to ping :D'
    )
    async def roll_the_ping(self, interaction : Interaction):

        role_havers : list[Member] = []

        for member in interaction.guild.members:

            role_names : list[str] = [role.name.lower() for role in member.roles]

            if "has no interesting roles" in role_names or "bot schmuck" in role_names:
                continue

            role_havers.append(member)

        ping_victim = random.choice(role_havers)

        await interaction.response.send_message(
            f"By fate, {interaction.user.display_name} has pinged {ping_victim.mention}. Congrats!"
        )


    @app_commands.command(
        name='pingus',
        description='Gets the latency of the bot'
    )
    async def pingus(self, interaction : Interaction):
        '''
        Gets the latency of the bot.
        '''

        await interaction.response.send_message(content=self.bot.latency)



async def setup(bot : commands.Bot) -> None:
    """
    Sets up the Cog.

    Parameters
    ----------
    bot : commands.Bot
        the bot to add the cog to
    """
    await bot.add_cog(ActionsCog(bot))

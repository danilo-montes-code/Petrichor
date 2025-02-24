"""actions.py

Contains the Cog that holds commands that perform actions.
"""

from discord import app_commands
from discord.ext import commands

from util.printing import print_petrichor_error
from util.casting import get_id

import random, pathlib

from discord import (
    Interaction,
    Member,
    Message,
    Forbidden,
    HTTPException
)
from discord import TextChannel

from Petrichor.PetrichorBot import PetrichorBot



class ActionsCog(commands.Cog):
    """
    Cog that holds commands that perform actions.

    Attributes
    ----------
    bot : PetrichorBot
        bot that the commands belong to
    """

    def __init__(self, bot : PetrichorBot):
        """
        Creates an instance of the ActionsCog class.

        Parameters
        ----------
        bot : PetrichorBot
            bot that the commands belong to
        """
        self.bot = bot


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

            if "has no interesting roles" in role_names or "bot schmuck" in role_names:
                continue

            role_havers.append(member)

        ping_victim = random.choice(role_havers)

        await interaction.response.send_message(
            f"By fate, {interaction.user.display_name} has pinged {ping_victim.mention}. Congrats!"
        )

        # TODO add record to rtp table


    @app_commands.command(
        name='pingus',
        description='Gets the latency of the bot'
    )
    async def pingus(self, interaction : Interaction):
        '''
        Gets the latency of the bot.
        
        Parameters
        ----------
        interaction : Interaction
            the interaction that evoked the command
        '''

        await interaction.response.send_message(content=self.bot.latency)


    @app_commands.command(
        name='last-clip',
        description='Gets the link of the user\'s most recent posted clip'
    )
    async def last_clip(
        self, 
        interaction : Interaction, 
        game : str = None,
        limit : int = 100
    ) -> None:
        """
        Gets the link of the last clip that the user posted in the POV channel.
        
        Parameters
        ----------
        interaction : Interaction
            the interaction that evoked the command
        game : str, default = None
            the name of the game to search for the last posted clip of
            (only works on clips sent as links)
        limit : int, default = 100
            the maximum number of messages to search through
        """
        
        pov_channel : TextChannel = self.bot.get_channel(get_id('APEX_POV_ID'))

        try:
            message : Message
            async for message in pov_channel.history(limit=limit):

                if  (not message.embeds 
                     and 'https://' not in message.content):
                    if  (not message.attachments
                         or not [file 
                                 for file in message.attachments 
                                 if pathlib.Path(file.filename).suffix != '.mp4']):
                        continue
                    

                # since I send game clips through this bot, check for messages
                # from both the both and myself if I use this command
                if (
                    (interaction.user.id == get_id('MY_ID') and
                    message.author.id == get_id('PETRICHOR_ID')) 
                    or message.author == interaction.user
                    ):
                    if game:
                        if (not message.embeds 
                            or game.replace(' ', '-') not in message.embeds[-1].url):
                                continue

                        await interaction.response.send_message(
                            content= \
                            f'Your last game clip was here: {message.jump_url}'
                        )

                    else:
                        await interaction.response.send_message(
                            content= \
                            f'Your last game clip was here: {message.jump_url}'
                        )
                        
                    return
                
            await interaction.response.send_message(
                content= \
                (
                    'No recent game clips found. You may want to search '
                    'again with a higher `limit` option.'
                )
            )

        except Forbidden:
            print_petrichor_error('lacking perms to get channel history')
        except HTTPException as err:
            print_petrichor_error('Request failed')
            print_petrichor_error('Response:', err.response)
            print_petrichor_error('Text:', err.text)
            print_petrichor_error('Status:', err.status)
        except Exception as err:
            print_petrichor_error('other exception raised:', err)
    


async def setup(bot : commands.Bot) -> None:
    """
    Sets up the Cog.

    Parameters
    ----------
    bot : commands.Bot
        the bot to add the cog to
    """
    await bot.add_cog(ActionsCog(bot))

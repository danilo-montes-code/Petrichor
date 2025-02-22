"""admin.py

Contains the Cog that holds admin commands.
"""

import discord
from discord import app_commands
from discord.ext import commands

from util.printing import print_petrichor_msg, print_petrichor_error

import os
from typing import Literal
from discord.ext.commands import (
    ExtensionNotLoaded,
    ExtensionNotFound,
    NoEntryPointError,
    ExtensionFailed
)

from discord import Interaction



class AdminCog(commands.Cog):
    """
    Cog that contains admin commands.

    Attributes
    ----------
    bot : commands.Bot
        bot that the commands belong to
    """

    def __init__(self, bot : commands.Bot) -> None:
        """
        Creates an instance of the AdminCog class.
        
        Parameters
        ----------
        bot : commands.Bot
            bot that the commands belong to
        """
        self.bot = bot


    @app_commands.command(
        name = 'shutdown',
        description = 'Shuts down the bot'
    )
    async def shutdown(self, interaction : Interaction) -> None:
        """
        Deactivates the bot, terminating the process that is running it.

        Parameters
        ----------
        interaction : Interaction
            the interaction that evoked the command
        """

        print(f'{self.bot.user} shutting down...')
        await interaction.response.send_message('Shutting down...')
        await self.bot.close()


    @app_commands.command(
        name = 'sync',
        description = 'Syncs the commands on the command tree'
    )
    async def sync(
        self, 
        interaction : Interaction, 
        scope : Literal['fanta', 'kidnamedsoub', 'all'] = 'all'
    ) -> None:
        """
        Syncs the app commands to Discord.

        Parameters
        ----------
        interaction : Interaction
            the interaction that evoked the command
        scope : Literal['fanta', 'kidnamedsoub', 'all'], default = 'all'
            indicates whether to sync commands in all or a specific server  
            'fanta' - archive/admin server
            'kidnamedsoub' - friends server
            'all' - all commands
        """

        if scope == 'fanta':
            await self.bot.tree.sync(guild = discord.Object(id=int(os.getenv('FANTA_ID'))))
            await interaction.response.send_message('Admin server synced.')
        elif scope == 'kidnamedsoub':
            await self.bot.tree.sync(guild = discord.Object(id=int(os.getenv('KNS_ID'))))
            await interaction.response.send_message('kidnamedsoub server synced.')
        else: 
            await self.bot.tree.sync()
            await interaction.response.send_message('Command tree synced on all servers.')


    @app_commands.command(
        name='reload-cog',
        description='Reloads a given Cog'
    )
    async def reload_cog(
        self, 
        interaction : Interaction,
        cog : Literal[
            'actions',
            'admin',
            'data', 
            'message_reacts',
            # 'reminders'
        ]
    ) -> None:
        """
        Reloads a given Cog.
        
        Parameters
        ----------
        cog : Literal[str]
            the cog to reload
        """
        try: 
            cog_path = f'Petrichor.cogs.{cog}'
            print_petrichor_msg(f'Attempting to reload: {cog}')
            await self.bot.reload_extension(cog_path)
            print_petrichor_msg('Reload successful')
            await interaction.response.send_message(f'Reloaded {cog} Cog')

        except ExtensionNotLoaded:
            print_petrichor_error('Extension was not loaded')
        except ExtensionNotFound:
            print_petrichor_error('Extension could not be imported')
        except NoEntryPointError:
            print_petrichor_error('Extension does not have a setup function')
        except ExtensionFailed:
            print_petrichor_error('Extension setup had an execution error')



async def setup(bot : commands.Bot) -> None:
    """
    Sets up the Cog.
    
    Parameters
    ----------
    bot : commands.Bot
        the bot to add the cog to
    """
    await bot.add_cog(
        AdminCog(bot), 
        guild=discord.Object(id=int(os.getenv('FANTA_ID')))
    )

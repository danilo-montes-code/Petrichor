"""admin.py

Contains the Cog that holds admin commands.
"""

import discord
from discord import app_commands
from discord.ext import commands

from util.printing import print_petrichor_msg, print_petrichor_error
from util.env_vars import get_id
from Petrichor.cogs import EXTENSIONS

from typing import Literal
from discord.ext.commands import (
    ExtensionNotLoaded,
    ExtensionNotFound,
    NoEntryPointError,
    ExtensionFailed
)
from discord import Interaction
from discord.ext.commands import Context



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


    @commands.command(
        name = 'sync',
        description = 'Syncs the commands on the command tree'
    )
    @commands.is_owner()
    async def sync(
        self, 
        ctx : Context, 
        scope : Literal['fanta', 'kidnamedsoub', 'all'] = 'all'
    ) -> None:
        """
        Syncs the app commands to Discord.

        Parameters
        ----------
        ctx : Context
            the context in which the command was evoked
        scope : Literal['fanta', 'kidnamedsoub', 'all'], default = 'all'
            indicates whether to sync commands in all or a specific server  
            'fanta' - archive/admin server
            'kidnamedsoub' - friends server
            'all' - all commands
        """

        if scope == 'fanta':
            await self.bot.tree.sync(guild = discord.Object(id=get_id('FANTA_ID')))
            await ctx.send('Admin server synced.')
        elif scope == 'kidnamedsoub':
            await self.bot.tree.sync(guild = discord.Object(id=get_id('KNS_ID')))
            await ctx.send('kidnamedsoub server synced.')
        else: 
            await self.bot.tree.sync()
            await ctx.send('Command tree synced on all servers.')


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
            'dev_commands',
            'event_handlers',
            # 'reminders',
            'roll_the_ping'
        ]
    ) -> None:
        """
        Reloads a given Cog.
        
        Parameters
        ----------
        interaction : Interaction
            the interaction that evoked the command
        cog : Literal[str]
            the cog to reload
        """
        cog_path = f'Petrichor.cogs.{cog}'
        reload_successful = await self._reload_cog(cog_path)
        if reload_successful:
            print_petrichor_msg('Reload successful')
            await interaction.response.send_message(f'Reloaded {cog} Cog')
            return
    
        print_petrichor_msg('Reload unsuccessful')
        await interaction.response.send_message(f'Could not reload {cog} Cog')
        return



    @app_commands.command(
        name='reload-cogs',
        description='Reloads all Cogs'
    )
    async def reload_cogs(
        self, 
        interaction : Interaction
    ) -> None:
        """
        Reloads a given Cog.

        Parameters
        ----------
        interaction : Interaction
            the interaction that evoked the command
        """
        for cog in EXTENSIONS:
            reload_successful = await self._reload_cog(cog)
            if reload_successful:   print_petrichor_msg('Reload successful')
            else:                   print_petrichor_error('Reload unsuccessful')
        await interaction.response.send_message('Reloaded Cogs')


    async def _reload_cog(self, cog_path : str) -> bool:
        """
        Reloads a given cog.
        
        Parameters
        ----------
        cog_path : str
            cog to reload

        Returns
        -------
        bool
            True,   if the reload was successful | 
            False, otherwise
        """
        
        try: 
            cog = cog_path.split('.')[-1]
            print_petrichor_msg(f'Attempting to reload: {cog}')
            await self.bot.reload_extension(cog_path)
            return True

        except ExtensionNotLoaded:
            print_petrichor_error('Extension was not loaded')
        except ExtensionNotFound:
            print_petrichor_error('Extension could not be imported')
        except NoEntryPointError:
            print_petrichor_error('Extension does not have a setup function')
        except ExtensionFailed:
            print_petrichor_error('Extension setup had an execution error')

        return False



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
        guild=discord.Object(id=get_id('FANTA_ID'))
    )

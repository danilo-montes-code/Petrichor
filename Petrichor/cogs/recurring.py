"""recurring.py

Contains the Cog that holds recurring tasks/jobs.
"""
from __future__ import annotations

import datetime
import random

from discord.ext import commands, tasks

from util.env_vars import get_list, get_id
from util.printing import print_petrichor_msg

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from discord import (
        TextChannel
    )

    from Petrichor.PetrichorBot import PetrichorBot


EST_MIDNIGHT = datetime.time(
                    hour=0, 
                    minute=0, 
                    second=0, 
                    tzinfo=datetime.timezone(
                        datetime.timedelta(hours=-5)
                    )
                )

NAMES : list[str] = get_list('FRIENDS_NAMES')



class RecurringCog(commands.Cog):
    """
    Cog that holds recurring tasks/jobs.

    Attributes
    ----------
    bot : PetrichorBot
        bot that the commands belong to
    """

    def __init__(self, bot : PetrichorBot):
        """
        Creates an instance of the RecurringCog class.

        Parameters
        ----------
        bot : PetrichorBot
            bot that the commands belong to
        """
        self.bot = bot
        self.change_pinging_channel_name.start()

    
    def cog_unload(self):
        """
        Runs when the cog is unloaded. Cancels the running tasks.
        """
        self.change_pinging_channel_name.cancel()


    @tasks.loop(time=EST_MIDNIGHT)
    async def change_pinging_channel_name(self):
        """
        Changes the name of the pinging channel to a random friend's name.
        """
        channel : TextChannel = self.bot.get_channel(get_id('APEX_PINGING_ID'))
        
        old_name = new_name = channel.name.split('-')[1]
        while new_name == old_name:
            new_name = random.choice(NAMES).lower()

        new_channel_name = f"pinging-{new_name}"

        print_petrichor_msg(f"Changing pinging channel name from {channel.name} to {new_channel_name}")

        await channel.edit(name=new_channel_name)



async def setup(bot : commands.Bot) -> None:
    """
    Sets up the Cog.

    Parameters
    ----------
    bot : commands.Bot
        the bot to add the cog to
    """
    await bot.add_cog(RecurringCog(bot))

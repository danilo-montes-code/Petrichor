"""recurring.py

Contains the Cog that holds recurring tasks/jobs.
"""
from __future__ import annotations

import datetime
import random
from zoneinfo import ZoneInfo

from discord.ext import commands, tasks

from util.env_vars import get_dict, get_id
from util.printing import print_petrichor_msg

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from discord import (
        TextChannel,
        Role,
        Member
    )

    from Petrichor.PetrichorBot import PetrichorBot


EST_MIDNIGHT = datetime.time(
    hour=0,
    minute=0,
    second=0, 
    tzinfo=ZoneInfo('America/New_York')
)

FRIENDS : dict[str, int] = get_dict('FRIEND_IDS')



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
        print_petrichor_msg(
            'Task Started: change_pinging_channel_name | '
            'Runs: Daily | '
            f'Time: {EST_MIDNIGHT}'
        )
        self.change_grok_owner.start()
        print_petrichor_msg(
            'Task Started: change_grok_owner | '
            'Runs: Daily | '
            f'Time: {EST_MIDNIGHT}'
        )

    
    def cog_unload(self):
        """
        Runs when the cog is unloaded. Cancels the running tasks.
        """
        self.change_pinging_channel_name.cancel()
        self.change_grok_owner.cancel()


    @tasks.loop(time=EST_MIDNIGHT)
    async def change_pinging_channel_name(self) -> None:
        """
        Changes the name of the pinging channel to a random friend's name.
        """

        await self.bot.wait_until_ready()

        channel : TextChannel = self.bot.get_channel(get_id('APEX_PINGING_ID'))
        
        old_name = new_name = channel.name.split('-')[1]
        while new_name == old_name:
            new_name = random.choice(list(FRIENDS.keys())).lower()

        new_channel_name = f"pinging-{new_name}"

        print_petrichor_msg(f"Changing pinging channel name from {channel.name} to {new_channel_name}")

        await channel.edit(name=new_channel_name)

 
    @tasks.loop(time=EST_MIDNIGHT)
    async def change_grok_owner(self) -> None:
        """
        Changes the grok role owner to a random friend.
        """

        async def purge_multiple_groks() -> None:
            """
            Removes grok role from multiple people if multiple people have it.
            """

            guild = await self.bot.fetch_guild(get_id('KNS_ID'))
            grok_role = await guild.fetch_role(get_id('APEX_GROK_ROLE_ID'))

            if not grok_role.members or len(grok_role.members) == 1:
                return
            
            print_petrichor_msg(
                "Multiple grok role owners detected, purging all but one."
            )

            one_member_kept = False
            member : Member
            for member in grok_role.members:
                if not member.bot and not one_member_kept:
                    one_member_kept = True
                    continue

                print_petrichor_msg(f"Removing from {member.name}")
                await member.remove_roles(grok_role.id)


        async def choose_new_grok_member(
            grok_role : Role,
            id_list_to_choose_from : list[int]
        ) -> None:
            """
            Chooses a new grok member from the friends list.
            """
            new_grok_member_id = random.choice(id_list_to_choose_from)
            new_grok_member = await guild.fetch_member(new_grok_member_id)
            await new_grok_member.add_roles(grok_role)
            print_petrichor_msg(f"Assigned grok role to {new_grok_member.name}")


        async def remove_grok_member(
            grok_role : Role,
            member_id_to_remove : int
        ) -> None:
            """
            Removes the grok role from the specified member.
            """
            
            member_to_remove = await guild.fetch_member(member_id_to_remove)
            await member_to_remove.remove_roles(grok_role)
            print_petrichor_msg(f"Removed grok role from {member_to_remove.name}")


        await self.bot.wait_until_ready()
        
        await purge_multiple_groks()

        guild = await self.bot.fetch_guild(get_id('KNS_ID'))
        grok_role = await guild.fetch_role(get_id('APEX_GROK_ROLE_ID'))

        if not grok_role.members:
            await choose_new_grok_member(grok_role, list(FRIENDS.values()))
            return

        current_grok_member_id = grok_role.members[0].id
        eligible_friends = [
            id 
            for id 
            in list(FRIENDS.values())
            if id != current_grok_member_id
        ]

        await remove_grok_member(grok_role, current_grok_member_id)
        await choose_new_grok_member(grok_role, eligible_friends)
        return



async def setup(bot : commands.Bot) -> None:
    """
    Sets up the Cog.

    Parameters
    ----------
    bot : commands.Bot
        the bot to add the cog to
    """
    await bot.add_cog(RecurringCog(bot))

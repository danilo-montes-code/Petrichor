"""message_reacts.py

Contains the Cog that manages message reactions.
"""
from __future__ import annotations

import random
import asyncio

from discord.ext import commands
from discord import VoiceChannel

from util.env_vars import get_id, get_dict
from util.server_info import SERVERS

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from discord import (
        Message, 
        Member,
        Role,
    )

    from Petrichor.PetrichorBot import PetrichorBot
    from util.server_info import ServerInfo


EMBED_FAILS = [
    'https://tenor.com/view/epic-embed-fail-ryan-gosling-cereal-embed-failure-laugh-at-this-user-gif-20627924',
    'https://tenor.com/view/epic-embed-fail-embed-fail-embed-discord-embed-gif-embed-gif-21924703',
    'https://tenor.com/view/embed-perms-no-image-perms-epic-embed-fail-laughing-emoji-gif-25041403',
    'https://tenor.com/view/epic-embed-fail-embed-embedfail-get-it-fail-embed-gif-22402006'
]

EMBED_SUCCESSES = [
    'https://tenor.com/view/epic-embed-success-gif-25677703',
    'https://tenor.com/view/catboy-cereal-embed-success-ryan-gosling-gif-21943489',
    'https://tenor.com/view/epic-embed-success-epic-embed-fail-gif-21239189',
    'https://tenor.com/view/embed-fail-embed-gif-24490045'
]

EMBED_FAIL_EXCEPTIONS = [
    'discord.com',
    'instagram.com',
    'discordapp.com'
]

DEFAULT_REPOST_SERVERS = {
    "apex-legends" : SERVERS["guard"]
}



class EventHandlersCog(commands.Cog):
    """
    Cog that manages message reactions.

    Attributes
    ----------
    bot : PetrichorBot
        bot that the commands belong to
    """

    def __init__(self, bot : PetrichorBot):
        """
        Creates an instance of the MessageReactsCog class.
        
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

        # preserve the ability to react to bots
        await self.igh_bro(message)

        if message.author.bot:
            return

        await self.repost_game_clips(message)
        await self.ping_vc(message)

        # await self.crazy_check(message)
        # await self.embed_evaluation(message)

        await self.bot.process_commands(message)


    @commands.Cog.listener()
    async def on_member_join(self, member : Member) -> None:
        if member.bot:
            bot_role : Role = member.guild.get_role(1184688230721921074)
            await member.add_roles(bot_role)
            return
        
        no_interesting_roles_role : Role = member.guild.get_role(1324385353783840931)
        await member.add_roles(no_interesting_roles_role)
        await self.bot.db.insert_row(
            table_name='users',
            record_info=[
                member.id,
                member.name
            ]
        )



    ##############################################################
    #######                                                #######
    ###                   message reactions                    ###
    #######                                                #######
    ##############################################################

    async def crazy_check(self, message : Message):
        """
        crazy? i was crazy once.
        they locked me in a room.
        a rubber room.
        a rubber room with rats.
        and rats make me crazy.

        Parameters
        ----------
        message : Message
            the message that was sent
        """

        msg = message.content.lower()

        if 'crazy' in msg:
            if 'i was crazy once' in msg:
                await self.respond_to_user(message, 'they locked me in a room.')
                return
            else:
                await self.respond_to_user(message, 'crazy? i was crazy once.')
                return

        if 'locked' in msg and 'in a room' in msg:
            await self.respond_to_user(message, 'a rubber room.')
            return

        if 'rubber room' in msg:
            if 'a rubber room with rats' in msg:
                await self.respond_to_user(message, 'and rats make me crazy.')
                return
            else:
                await self.respond_to_user(message, 'a rubber room with rats.')
                return


    async def igh_bro(self, message : Message):
        """
        igh bro
        
        Parameters
        ----------
        message : Message
            the message that was sent
        """

        if message.channel.id != get_id('KNS_GAME_UPDATES'):
            return

        if message.author.id in (get_id('PETRICHOR_ID'), get_id('PETRICHOR_TESTING_ID')):
            return

        await self.respond_to_user(message=message, response='igh bro')
        return


    async def embed_evaluation(self, message : Message):
        """
        epic fail of the embed

        Parameters
        ----------
        message : Message
            the message that was sent
        """

        # re-fetch the message after a short delay to ensure embeds are
        # properly detected before evaluation
        await asyncio.sleep(5)
        message = await self.bot.get_channel(message.channel.id) \
                                .fetch_message(message.id)

        if not message.embeds:
            if 'https://' not in message.content:
                return
            
            if self._link_is_an_embed_exception(message.content):
                return
            
            await message.reply(content=random.choice(EMBED_FAILS))
            return


        # dont run this in the clips channel bc that would be too much spam
        if message.channel.id == get_id('KNS_POV_ID'):
            return

        # only run this 2% of the time because it would get annoying real quick
        # more than it already will be
        if random.random() < (98 / 100):
            return

        await message.reply(content=random.choice(EMBED_SUCCESSES))
        return
    

    def _link_is_an_embed_exception(self, message : str) -> bool:
        """
        Returns True if the given message has a link that is an exception
        for embed evaluations.
        
        Parameters
        ----------
        message : str
            the message to process
        
        Returns
        -------
        bool
            True,   if the given message has a link that is an exception
            for embed evaluations |
            False,  otherwise
        """

        return any(link in message for link in EMBED_FAIL_EXCEPTIONS)



    ##############################################################
    #######                                                #######
    ###                    channel posting                     ###
    #######                                                #######
    ##############################################################

    async def repost_game_clips(
        self,
        message : Message,
    ) -> None:
        """
        Reposts game clips posted to my archive server to another server.
        
        Parameters
        ----------
        message : Message
            the message to repost, if applicable
        """
        
        if message.guild.id != get_id('FANTA_ID'):
            return
        
        if 'clips' not in message.channel.name:
            return
        
        if '!keep' in message.content:
            return
                
        text_to_send = self._replace_name_with_id(message.content)

        await self.repost_to_channel(text_to_send)


    async def ping_vc(
        self,
        message : Message,
    ) -> None:
        """
        Replaces an instance of @vc with a ping to all the users in
        the voice chat.
        
        Parameters
        ----------
        message : str
            the message to process
        """

        if not isinstance(message.channel, VoiceChannel):
            return
        
        if '@vc' not in message.content.lower():
            return
        
        members_in_vc = message.channel.members
        if not members_in_vc:
            await message.reply(
                content=(
                    'Voice channel is empty, "@vc" command only works '
                    'when there are people in the voice channel.'
                ),
                mention_author=True
            )
            return
        
        mentions = ' '.join(member.mention for member in members_in_vc)

        await message.reply(
            content=message.content.replace("@vc", mentions),
            mention_author=False
        )


    def _replace_name_with_id(self, message : str) -> str:
        """
        Replaces the name with the direct @ of the user.
        
        Parameters
        ----------
        message : str
            the message to process
        
        Returns
        -------
        str
            the new message with the names swapped with the @ pings
        """

        friends = get_dict('FRIEND_IDS')

        for friend in friends:
            friend : str

            if friend.lower() in message.lower():

                message = message.replace(
                    friend.lower(),
                    f'<@{friends[friend]}>'
                )


        return message


    async def repost_to_channel(self, message_content : str) -> None:
        """
        Reposts a clip from my archive server's game clips channels
        to one of the game clips channels. The message should start with the respective
        flag for which server should be posted to. Defaults to kidnamedsoub.
        Options are: !guard


        Parameters
        ----------
        message_content : str
            the message to be transferred
        """

        server_to_repost_to = self._get_server_to_repost(message_content)
        message_content = self._clean_message_content(message_content)

        channel = self.bot.get_channel(server_to_repost_to.repost_channel_id)
        await channel.send(content=message_content)

    
    def _get_server_to_repost(self, message_content : str) -> ServerInfo:
        """
        Returns the server to repost to based on the given message content.
        Defaults to kidnamedsoub if no server is specified.

        
        Parameters
        ----------
        message_content : str
            the message to be transferred

        Returns
        -------
        ServerInfo
            the server to repost to
        """

        for server in SERVERS.values():
            if message_content.startswith(f"!{server.guild_flag}"):
                return server
            
        if default_server := self._check_for_default_server_for_game(message_content):
            return default_server

        return SERVERS["kns"]
    
    def _check_for_default_server_for_game(self, message_content : str) -> ServerInfo | None:
        """
        Returns the default server to report for a given game, if one exists.


        Parameters
        ----------
        message_content : str
            the message to check for a default server

        Returns
        -------
        ServerInfo
            the default server
        None
            if no server default exists
        """

        for game, server in DEFAULT_REPOST_SERVERS.items():
            if game in message_content:
                return server
            
        return None


    def _clean_message_content(self, message_content : str) -> str:
        """
        Removes the flag from the beginning of the message if present.

        
        Parameters
        ----------
        message_content : str
            the message to clean
        
        Returns
        -------
            the cleaned message
        """

        if message_content.startswith("!"):

            flag_cutoff = message_content.index(" ")
            return message_content[flag_cutoff+1:]
        
        return message_content


    async def respond_to_user(self, message : Message, response : str) -> None:
        """
        Responds to a user in the same channel they typed in with
        a given message.

        Parameters
        ----------
        message : Message
            the message that the user sent
        response : str
            the desired response to the user from the bot
        """
        await message.channel.send(content=response)



async def setup(bot : commands.Bot) -> None:
    """
    Sets up the Cog.

    Parameters
    ----------
    bot : commands.Bot
        the bot to add the cog to
    """
    await bot.add_cog(EventHandlersCog(bot))

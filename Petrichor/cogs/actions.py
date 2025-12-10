"""actions.py

Contains the Cog that holds commands that perform actions.
"""
from __future__ import annotations

import pathlib

from discord import app_commands
from discord.ext import commands

from util.printing import print_petrichor_error
from util.env_vars import get_id, get_dict

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from discord import (
        Interaction,
        TextChannel,
        Message,
        Forbidden,
        HTTPException
    )

    from Petrichor.PetrichorBot import PetrichorBot


GAME_CLIP_LINKS = (
    'https://outplayed.tv',
    'https://medal.tv',
    'https://youtu.be',
    'https://cdn.steamusercontent.com'
)



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


    # TODO maybe making into hybrid command? if the app command is too long,
    # a standard command might be able to handle the increased wait time
    @app_commands.command(
        name='last-clip',
        description='Gets the link of the user\'s most recent posted clip'
    )
    async def last_clip(
        self, 
        interaction : Interaction, 
        game : str = '',
        limit : int = 100,
        skip : int = 0
    ) -> None:
        """
        Gets the link of the last clip that the user posted in the POV channel.
        
        Parameters
        ----------
        interaction : Interaction
            the interaction that evoked the command
        game : str, default = ''
            the name of the game to search for the last posted clip of
            (only works on clips sent as links)
        limit : int, default = 100
            the maximum number of messages to search through
        skip : int, default = 0
            the number of found clips/files to skip over. Useful if you have
            sent non-clip mp4 files and wish to pass over them to continue searching.
        """

        if skip < 0:
            await interaction.response.send_message(
                'Please enter a positive number of found messages to skip.'
            )
            return
        
        pov_channel : TextChannel = self.bot.get_channel(get_id('APEX_POV_ID'))

        if not pov_channel:
            print_petrichor_error('Clips channel not found.')
            return

        if game: game = game.lower()

        try:
            message : Message
            async for message in pov_channel.history(limit=limit):

                if not self._message_has_clip_link_or_mp4(message):
                    continue
                    
                if not self._message_is_from_user(message, interaction):
                    continue

                if game:
                    if (not message.embeds 
                        or not self._link_has_game_in_text(
                            game=game,
                            link=str(message.embeds[-1].url).lower()
                        )):
                            continue
                    
                if skip > 0:
                    skip -= 1
                    continue
            
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
            print_petrichor_error('Lacking perms to get channel history')
        except HTTPException as err:
            print_petrichor_error('Request to get channel history failed')
            print_petrichor_error('Response:' + str(err.response))
            print_petrichor_error('Text:' + str(err.text))
            print_petrichor_error('Status:' + str(err.status))
        except Exception as err:
            print_petrichor_error('Other exception raised:' + str(err))


    def _message_has_clip_link_or_mp4(self, message : Message) -> bool:
        """
        Returns True if the given Message has either a link to a clip 
        or an mp4 file.

        Parameters
        ----------
        message : Message
            the message to process

        Returns
        -------
        bool
            True,   if the given Message has either a clip link or an mp4 file |
            False,  otherwise
        """

        if 'https://' not in message.content:

            if not message.attachments:
                return False
            
            if not [file 
                    for file in message.attachments 
                    if pathlib.Path(file.filename).suffix == '.mp4']:
                return False
        
        if not self._link_is_a_game_clip(message.content):
            return False

        return True


    def _link_is_a_game_clip(self, message : str) -> bool:
        """
        Returns True if the given message has a link that is a game clip.

        Parameters
        ----------
        message : str
            the message to process

        Returns
        -------
        bool
            True,   if the given message has a link that is a game clip |
            False,  otherwise
        """

        return any(link in message for link in GAME_CLIP_LINKS)
    

    def _message_is_from_user(
            self, 
            message : Message, 
            interaction: Interaction
        ) -> bool:
        """
        Returns True if the given Message was sent from the same user that
        sent the Interaction.

        Parameters
        ----------
        message : Message
            the message to process

        Returns
        -------
        bool
            True,   if the given Message is from the user |
            False,  otherwise
        """
        # since I send game clips through this bot, check for messages
        # from both the both and myself if I use this command
        return (
            (
                interaction.user.id == get_id('MY_ID') and
                message.author.id == get_id('PETRICHOR_ID')
            ) or message.author == interaction.user
        )


    def _link_has_game_in_text(
        self, 
        game : str,
        link : str
    ) -> bool:
        """
        Returns True if the game appears in the text of the link.
        
        Parameters
        ----------
        game : str
            the name of the game to check for
        link : str
            the link to check
        
        Returns
        -------
        True,   if the given link has the game inside |
        False,  otherwise
        """
        return game.replace(' ', '-') in link


    @app_commands.command(
        name='dailies',
        description='Gets the links to common dailies that we do.'
    )
    async def dailies(self, interaction : Interaction) -> None:
        """
        Displays the links to common dailies that we do.
        
        Parameters
        ----------
        interaction : Interaction
            the interaction that evoked the command
        """

        await interaction.response.send_message(
            content=(
                f'**Duolingo**: <@{get_dict('FRIEND_IDS')['MAX']}> thoughts?\n'
                '**Wordle**: Discord activity (`/wordle`)\n'
                '**Bandle**: https://bandle.app/menu\n'
                '**Gamedle**: https://www.gamedle.wtf/guess#\n'
                '**Apex**:\n'
                '- guess the character: https://thevalber.github.io/apexdle/classic\n'
                '- guess the rank: https://rankdle.com/games/apex\n'
                '**Overwatch**:\n'
                '- guess the character: https://owdle.guessing.day/\n'
                '- guess the rank: https://rankdle.com/games/ow2\n'
                '**Pokedle**: https://pokedle.io/\n'
                '**Smashdle**: https://smashdle.net/classic\n'
                '**Tekkendle**: https://tekkendle.net/'
            ),
            suppress_embeds=True
        )


    @app_commands.command(
        name='help',
        description='Displays a list of commands that the bot can perform.'
    )
    async def help(self, interaction : Interaction) -> None:
        """
        Displays a list of commands that the bot can perform.
        
        Parameters
        ----------
        interaction : Interaction
            the interaction that evoked the command
        """

        await interaction.response.send_message(
            content=(
                '# Petrichor Commands\n'
                '## euoh Commands\n'
                '* `/euoh vc add <euoh_recipient> <euoh_type>` - add a VC Meuohment of a given type to a person\n'
                '* `/euoh vc get <euoh_recipient>` - get a person\'s VC Meuohment counts\n'
                '## rtp Commands\n'
                '* `/rtp` - "roll the ping", chooses a random active member and pings them\n'
                '* `/ping-counts perpetrator` - show a ranking of `/rtp` command runners\n'
                '* `/ping-counts victim` - show a ranking of `/rtp` command receivers\n'
                '## kaeley Commands\n'
                '* `/kaeley days-since-last-side-eye` - get the time since kaeley\'s last side eye reaction\n'
                '* `/kaeley longest-side-eye-drought` - get the longest number of days where kaeley didn\'t react with a side eye\n'
                '* `/kaeley total-side-eye-count` - get the total number of side eye reactions kaeley has made\n'
                '## Assorted Commands\n'
                '* `/dailies`: get the links to common dailies that we do\n'
                '* `/last-clip`: get the link of the last clip that the user posted in the POV channel\n'
                '  * `game` - **(optional)** the game to search for, doesn\'t check for game by default (only works on clips sent as links)\n'
                '  * `limit` - **(optional)** the maximum number of messages to search through, 100 by default\n'
                '  * `skip` - **(optional)** the number of successfully found clips to skip over, 0 by default\n'
                '* `/pingus`: get the latency of the bot\n'
                '* `/help`: display this message\n'
                '# Petrichor Functions\n'
                '* repost game clips to the `#pov-ur-bad` channel\n'
                '* change pinging channel to a random friend everyday at midnight\n'
                '* change @Grok role owner to a random friend everyday at midnight\n'
                '* **[DISABLED]** occassionally send responses to messages with embeds (and embed fails)\n'
                '* **[DISABLED]** crazy? i was crazy once.'
            ),
            suppress_embeds=True
        )



async def setup(bot : commands.Bot) -> None:
    """
    Sets up the Cog.

    Parameters
    ----------
    bot : commands.Bot
        the bot to add the cog to
    """
    bot : PetrichorBot

    await bot.add_cog(ActionsCog(bot))

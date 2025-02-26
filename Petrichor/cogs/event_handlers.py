"""message_reacts.py

Contains the Cog that manages message reactions.
"""

from discord.ext import commands

from util.casting import get_id

import random, time

from discord import (
    Message, 
    Member
)
from Petrichor.PetrichorBot import PetrichorBot



class MessageReactsCog(commands.Cog):
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
        self.embed_fails = [
            'https://tenor.com/view/epic-embed-fail-ryan-gosling-cereal-embed-failure-laugh-at-this-user-gif-20627924',
            'https://tenor.com/view/epic-embed-fail-embed-fail-embed-discord-embed-gif-embed-gif-21924703',
            'https://tenor.com/view/embed-perms-no-image-perms-epic-embed-fail-laughing-emoji-gif-25041403',
            'https://tenor.com/view/epic-embed-fail-embed-embedfail-get-it-fail-embed-gif-22402006'
        ]
        # mid ground
        # 'https://tenor.com/view/embed-fail-embed-fail-intentional-intentional-embed-gif-17355838859230793055',
        self.embed_successes = [
            'https://tenor.com/view/epic-embed-success-gif-25677703',
            'https://tenor.com/view/catboy-cereal-embed-success-ryan-gosling-gif-21943489',
            'https://tenor.com/view/epic-embed-success-epic-embed-fail-gif-21239189',
            'https://tenor.com/view/embed-fail-embed-gif-24490045'
        ]



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

        # sends messages from clips channels in archive server
        # to another server
        if (message.guild.id == get_id('FANTA_ID') and 
           'clips' in message.channel.name):

            await self.post_to_pov(message.content)

        await self.crazy_check(message)
        await self.embed_evaluation(message)

        await self.bot.process_commands(message)


    @commands.Cog.listener()
    async def on_member_join(self, member : Member) -> None:
        if member.bot:
            return
        
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

        if message.channel.id != get_id('APEX_GAME_UPDATES'):
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
        time.sleep(2)
        message = await self.bot.get_channel(message.channel.id) \
                                .fetch_message(message.id)

        if not message.embeds:
            if 'https://' not in message.content:
                return
            
            await self.respond_to_user(
                message=message, 
                response=random.choice(self.embed_fails)
            )
            return


        # dont run this in the clips channel bc that would be too much spam
        if message.channel.id == get_id('APEX_POV_ID'):
            return

        # only run this 10% of the time because it would get annoying real quick
        # more than it already will be
        if random.random() < (90 / 100):
            return

        await self.respond_to_user(
            message=message, 
            response=random.choice(self.embed_successes)
        )
        return



    ##############################################################
    #######                                                #######
    ###                    channel posting                     ###
    #######                                                #######
    ##############################################################

    async def post_to_power(self, message_content: str) -> None:
        """
        Posts a given message from my archive server's game clips channels
        to the soup game clips channel.

        Parameters
        ----------
        message_content : str
            the message to be transferred
        """
        power = self.bot.get_channel(get_id('SOUP_POWER_ID'))
        await power.send(content=message_content)


    async def post_to_pov(self, message_content : str) -> None:
        """
        Posts a clip from my archive server's game clips channels
        to the POV game clips channel.

        Parameters
        ----------
        message_content : str
            the message to be transferred
        """
        power = self.bot.get_channel(get_id('APEX_POV_ID'))
        await power.send(content=message_content)


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
    await bot.add_cog(MessageReactsCog(bot))

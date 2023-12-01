from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import discord
from discord import Message

import os

### handled by pipenv
# from dotenv import load_dotenv
# load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)



@client.event
async def on_ready() -> None:
    """
    Sets up the bot when the client has connected.
    """

    scheduler = AsyncIOScheduler()

    # remind about rankdle at 9p EST
    scheduler.add_job(remind_about_rankdle, 
                      CronTrigger(hour=9 + 12))
    
    # remind about pokedle at 7p EST
    scheduler.add_job(remind_about_pokedle, 
                      CronTrigger(hour=7 + 12))
    
    # remind about gamedle at 9p EST
    scheduler.add_job(remind_about_gamedle, 
                      CronTrigger(hour=9 + 12))
    
    scheduler.start()

    print(f'User {client.user} logged in')


@client.event
async def on_message(message: Message) -> None:
    """
    Responds to messages sent in servers that the bot is in.

    Parameters
    ----------
    message : Message
        the message that was sent in a channel
    """

    # prevents recursive call
    if message.author == client.user:
        return


    # sends messages from clips channels in archive server
    # to another server
    if (message.guild.id == int(os.getenv('FANTA_ID')) and 
       'clips' in message.channel.name):
        
        await post_to_power(message.content)
        if 'apex' in message.channel.name:
            await post_to_apex(message.content)
            
        return

    # funny crazy
    crazy_check()


async def crazy_check(message: Message):
    """
    crazy? i was crazy once.
    they locked me in a room.
    a rubber room.
    a rubber room with rats.
    and rats make me crazy.
    """

    msg = message.content.lower()

    # swap order to avoid wrong call
    if 'crazy? i was crazy once' in msg:
        await respond_to_user(message, 'they locked me in a room.')
        return

    if 'crazy' in msg:
        await respond_to_user(message, 'crazy? i was crazy once.')
        return
    
    if 'locked' in msg and 'in a room' in msg:
        await respond_to_user(message, 'a rubber room.')
        return
    
    if 'a rubber room' in msg:
        await respond_to_user(message, 'a rubber room with rats.')
    
    if 'rubber room with rats' in msg:
        await respond_to_user(message, 'and rats make me crazy.')
        return



async def post_to_power(message_content: str) -> None:
    """
    Posts a given message from my archive server's game clips channels
    to the soup game clips channel.

    Parameters
    ----------
    message_content : str
        the message to be transferred
    """
    power = client.get_channel(int(os.getenv('POWER_ID')))
    await power.send(content=message_content)


async def post_to_apex(message_content: str) -> None:
    """
    Posts an Apex clip from my archive server's game clips channels
    to the Apex game clips channel.

    Parameters
    ----------
    message_content : str
        the message to be transferred
    """
    power = client.get_channel(int(os.getenv('APEX_LES_POV_ID')))
    await power.send(content=message_content)


async def respond_to_user(message: Message, response: str) -> None:
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
    await client.get_channel(message.channel.id) \
                .send(content=response)


async def remind_about_rankdle() -> None:
    # https://stackoverflow.com/a/63388134

    content = f'Rankdle has reset! https://rankdle.com/'
    await client.get_channel(int(os.getenv('DROPPED_ID'))) \
                .send(content=content)
    await client.get_channel(int(os.getenv('APEX_LES_GEN_ID'))) \
                .send(content=content)
    

async def remind_about_pokedle() -> None:

    content = f'Pokedle has reset! https://pokedle.io/'
    await client.get_channel(int(os.getenv('APEX_LES_GEN_ID'))) \
                .send(content=content)
    

async def remind_about_gamedle() -> None:

    content = f'Gamedle has reset! https://www.gamedle.wtf/guess#'
    await client.get_channel(int(os.getenv('APEX_LES_GEN_ID'))) \
                .send(content=content)
    



client.run(os.getenv('BOT_TOKEN'))
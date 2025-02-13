from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import discord
from discord.ext import commands
from discord import (
    Message,
    Interaction,
    Member
)
from discord.ext.commands import Context

import os, random
import typing


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='?', intents=intents)



##############################################################
#######                                                #######
###                    event handling                      ###
#######                                                #######
##############################################################

@bot.event
async def on_ready() -> None:
    """
    Sets up the bot when the client has connected.
    """

    # we don't really use these anymore
    # setup_dle_reminders()

    # TODO remove from comments once hybrid command is created for syncing
    # await bot.tree.sync()
    # await bot.tree.sync(guild = discord.Object(id=int(os.getenv('FANTA_ID'))))

    print(f'User {bot.user} online')


@bot.event
async def on_message(message: Message) -> None:
    """
    Responds to messages sent in servers that the bot is in.

    Parameters
    ----------
    message : Message
        the message that was sent in a channel
    """

    # prevents recursive call
    if message.author == bot.user:
        return

    await bot.process_commands(message)

    # sends messages from clips channels in archive server
    # to another server
    if (message.guild.id == int(os.getenv('FANTA_ID')) and 
       'clips' in message.channel.name):
        
        await post_to_apex_server(message.content)
        # if '0' in message.channel.name:
            # await post_to_power(message.content)

    await crazy_check(message)
    await igh_bro(message)
    await embed_evaluation(message)



##############################################################
#######                                                #######
###                 public slash commands                  ###
#######                                                #######
##############################################################

@bot.tree.command(
    name='rtp',
    description='Chooses a random active member to ping :D'
)
async def roll_the_ping(interaction : Interaction):

    role_havers : list[Member] = []

    for member in interaction.guild.members:

        role_names : list[str] = [role.name.lower() for role in member.roles]

        if "has no interesting roles" in role_names or "bot schmuck" in role_names:
            # print(f'{member.display_name} is excluded')
            continue

        role_havers.append(member)

    # print([user.name for user in role_havers])

    ping_victim = random.choice(role_havers)

    await interaction.response.send_message(
        f"By fate, {interaction.user.display_name} has pinged {ping_victim.mention}. Congrats!"
    )


@bot.tree.command(
    name='pingus',
    description='Gets the latency of the bot'
)
async def pingus(interaction : Interaction):
    '''
    Gets the latency of the bot.
    '''

    await interaction.response.send_message(content=bot.latency)



##############################################################
#######                                                #######
###                  owner slash commands                  ###
#######                                                #######
##############################################################


@bot.tree.command(
    name = 'shutdown',
    description = 'Shuts down the bot',
    guild = discord.Object(id=int(os.getenv('FANTA_ID')))
)
async def shutdown(interaction : Interaction):
    print(f'{bot.user} shutting down...')
    await interaction.response.send_message('Shutting down...')
    await bot.close()


@bot.hybrid_command(
    name = 'sync',
    description = 'Syncs the commands on the command tree',
    guild = discord.Object(int(os.getenv('FANTA_ID')))
)
async def sync(ctx : Context, scope : typing.Literal['fanta', 'all'] = 'all'):
    if scope == 'fanta':
        await bot.tree.sync(guild = discord.Object(id=int(os.getenv('FANTA_ID'))))
        await ctx.send('Admin command tree synced.')
    else: 
        await bot.tree.sync()
        await ctx.send('Command tree synced.')



##############################################################
#######                                                #######
###                    channel posting                     ###
#######                                                #######
##############################################################

async def crazy_check(message: Message):
    """
    crazy? i was crazy once.
    they locked me in a room.
    a rubber room.
    a rubber room with rats.
    and rats make me crazy.
    """

    msg = message.content.lower()

    if 'crazy' in msg:
        if 'i was crazy once' in msg:
            await respond_to_user(message, 'they locked me in a room.')
            return
        else:
            await respond_to_user(message, 'crazy? i was crazy once.')
            return
    
    if 'locked' in msg and 'in a room' in msg:
        await respond_to_user(message, 'a rubber room.')
        return
    
    if 'rubber room' in msg:
        if 'a rubber room with rats' in msg:
            await respond_to_user(message, 'and rats make me crazy.')
            return
        else:
            await respond_to_user(message, 'a rubber room with rats.')
            return


async def igh_bro(message: Message):

    if message.channel.id != int(os.getenv('APEX_GAME_UPDATES')):
        return

    await respond_to_user(message=message, response='igh bro')
    return


embed_links = [
    # failure
    'https://tenor.com/view/epic-embed-fail-ryan-gosling-cereal-embed-failure-laugh-at-this-user-gif-20627924',
    'https://tenor.com/view/epic-embed-fail-embed-fail-embed-discord-embed-gif-embed-gif-21924703',
    'https://tenor.com/view/embed-perms-no-image-perms-epic-embed-fail-laughing-emoji-gif-25041403',
    'https://tenor.com/view/epic-embed-fail-embed-embedfail-get-it-fail-embed-gif-22402006',

    'https://tenor.com/view/embed-fail-embed-fail-intentional-intentional-embed-gif-17355838859230793055',

    # sucess
    'https://tenor.com/view/epic-embed-success-gif-25677703',
    'https://tenor.com/view/catboy-cereal-embed-success-ryan-gosling-gif-21943489',
    'https://tenor.com/view/epic-embed-success-epic-embed-fail-gif-21239189',
    'https://tenor.com/view/embed-fail-embed-gif-24490045'
]
async def embed_evaluation(message: Message):

    # only reply to embeds bc like that's the whole point
    if not message.embeds:
        return

    # dont run this in the clips channel bc that would be too much spam
    if message.channel.id == int(os.getenv('APEX_POV_ID')):
        return

    # only run this 10% of the time because it would get annoying real quick
    # more than it already will be
    if random.randint(0, 9) not in (3, 6, 9):
        return
    
    await respond_to_user(
        message=message, 
        response=random.choice(embed_links)
    )
    return



##############################################################
#######                                                #######
###                    channel posting                     ###
#######                                                #######
##############################################################

async def post_to_power(message_content: str) -> None:
    """
    Posts a given message from my archive server's game clips channels
    to the soup game clips channel.

    Parameters
    ----------
    message_content : str
        the message to be transferred
    """
    power = bot.get_channel(int(os.getenv('SOUP_POWER_ID')))
    await power.send(content=message_content)


async def post_to_apex_server(message_content: str) -> None:
    """
    Posts an Apex clip from my archive server's game clips channels
    to the Apex game clips channel.

    Parameters
    ----------
    message_content : str
        the message to be transferred
    """
    power = bot.get_channel(int(os.getenv('APEX_POV_ID')))
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
    await bot.get_channel(message.channel.id) \
                .send(content=response)



##############################################################
#######                                                #######
###                    -dle reminders                      ###
#######                                                #######
##############################################################

# https://stackoverflow.com/a/63388134

async def setup_dle_reminders() -> None:
    scheduler = AsyncIOScheduler()

    # remind about rankdle at 9p EST
    scheduler.add_job(remind_about_rankdle, 
                      CronTrigger(hour=9 + 12))

    # remind about wordle at 12a EST
    scheduler.add_job(remind_about_wordle, 
                      CronTrigger(hour=0))

    # remind about bandle at 12a EST
    scheduler.add_job(remind_about_bandle, 
                      CronTrigger(hour=0))

    # remind about pokedle at 7p EST
    scheduler.add_job(remind_about_pokedle, 
                      CronTrigger(hour=7 + 12))

    # remind about gamedle at 9p EST
    scheduler.add_job(remind_about_gamedle, 
                      CronTrigger(hour=10 + 12))

    # remind about smashdle at 1a EST
    scheduler.add_job(remind_about_smashdle, 
                      CronTrigger(hour=1))

    scheduler.start()

async def remind_about_rankdle() -> None:
    content = f'Rankdle has reset! https://rankdle.com/games/apex'
    await bot.get_channel(int(os.getenv('APEX_RANKDLE_ID'))) \
                .send(content=content)

async def remind_about_wordle() -> None:
    content = \
        f'Wordle has reset! https://www.nytimes.com/games/wordle/index.html'
    await bot.get_channel(int(os.getenv('APEX_WORDLE_ID'))) \
                .send(content=content)

async def remind_about_bandle() -> None:
    content = f'Bandle has reset! https://bandle.app/'
    await bot.get_channel(int(os.getenv('APEX_BANDLE_ID'))) \
                .send(content=content)

async def remind_about_pokedle() -> None:
    content = f'Pokedle has reset! https://pokedle.io/'
    await bot.get_channel(int(os.getenv('APEX_POKEDLE_ID'))) \
                .send(content=content)

async def remind_about_gamedle() -> None:
    content = f'Gamedle has reset! https://www.gamedle.wtf/guess#'
    await bot.get_channel(int(os.getenv('APEX_GAMEDLE_ID'))) \
                .send(content=content)

async def remind_about_smashdle() -> None:
    content = f'Smashdle has reset! https://smashdle.net/classic'
    await bot.get_channel(int(os.getenv('APEX_SMASHDLE_ID'))) \
                .send(content=content)



##############################################################
#######                                                #######
###                       run bot                          ###
#######                                                #######
##############################################################

bot.run(os.getenv('BOT_TOKEN'))
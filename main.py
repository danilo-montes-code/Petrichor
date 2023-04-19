import discord, os
# from dotenv import load_dotenv
from discord import Message
# load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)



@client.event
async def on_ready() -> None:
    print(f'User {client.user} logged in')


@client.event
async def on_message(message: Message) -> None:
    """Responds to messages sent in servers that the bot is in

    Parameters
    ----------
    """

    # prevents recursive call
    if message.author == client.user:
        return


    # sends messages from clips channels in archive server
    # to another server
    if (message.guild.id == int(os.getenv('FANTA_ID')) and 
       'clips' in message.channel.name):
        content = message.content
        power = client.get_channel(int(os.getenv('POWER_ID')))
        await power.send(content=content)



client.run(os.getenv('BOT_TOKEN'))
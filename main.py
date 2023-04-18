import discord, os
from dotenv import load_dotenv
from keep_alive import keep_alive
from discord import Message
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready() -> None:
    print(f'User {client.user} logged in')

@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return

    if (message.guild.id == int(os.getenv('FANTA_ID')) and 
       'clips' in message.channel.name):
        content = message.content
        power = client.get_channel(int(os.getenv('POWER_ID')))
        await power.send(content=content)


keep_alive()
client.run(os.getenv('BOT_TOKEN'))
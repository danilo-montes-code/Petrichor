"""main.py

The driver for the Petrichor bot.
"""

from Petrichor.PetrichorBot import PetrichorBot
from util.db_connection_manager import DatabaseConnectionManager

import os, asyncio



async def main():
    async with DatabaseConnectionManager() as db_conn:
        async with PetrichorBot(
            db_conn=db_conn
        ) as bot:
            await bot.start(os.getenv('BOT_TOKEN'))


if __name__ == "__main__":
    asyncio.run(main())

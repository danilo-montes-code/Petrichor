#!/usr/bin/env -S uv run --env-file .env
"""main.py

The driver for the Petrichor bot.
"""

import os
import asyncio
import logging
import logging.handlers
from pathlib import Path

from Petrichor.PetrichorBot import PetrichorBot
from util.db_connection_manager import DatabaseConnectionManager



async def main():
    async with DatabaseConnectionManager() as db_conn:
        async with PetrichorBot(
            db_conn=db_conn
        ) as bot:
            await bot.start(os.getenv('BOT_TOKEN'))


def setup_logging():

    # logging configuration obtained from discord.py documentation
    # https://discordpy.readthedocs.io/en/stable/logging.html
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    logging.getLogger('discord.http').setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename=Path('logs', os.getenv('BOT_NAME') + '.log'),
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)



if __name__ == "__main__":
    setup_logging()
    asyncio.run(main())

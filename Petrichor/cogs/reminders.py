"""reminders.py

Contains the Cog that manages reminders.
"""

from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from util.printing import print_petrichor_msg
from util.env_vars import get_id

import os


class RemindersCog(commands.Cog):
    """
    Cog that manages reminders.

    Attributes
    ----------
    bot : commands.Bot
        bot that the commands belong to
    """

    def __init__(self, bot : commands.Bot):
        """
        Creates an instance of the RemindersCog class.

        Parameters
        ----------
        bot : commands.Bot
            bot that the commands belong to
        """
        self.bot = bot



    ##############################################################
    #######                                                #######
    ###                    -dle reminders                      ###
    #######                                                #######
    ##############################################################

    # https://stackoverflow.com/a/63388134

    async def setup_dle_reminders(self) -> None:
        """
        Sets up reminders for "-dle" websites.
        """

        print_petrichor_msg('Setting up -dle reminders')
        scheduler = AsyncIOScheduler()

        # remind about rankdle at 9p EST
        scheduler.add_job(self.remind_about_rankdle, 
                          CronTrigger(hour=9 + 12))

        # remind about wordle at 12a EST
        scheduler.add_job(self.remind_about_wordle, 
                          CronTrigger(hour=0))

        # remind about bandle at 12a EST
        scheduler.add_job(self.remind_about_bandle, 
                          CronTrigger(hour=0))

        # remind about pokedle at 7p EST
        scheduler.add_job(self.remind_about_pokedle, 
                          CronTrigger(hour=7 + 12))

        # remind about gamedle at 9p EST
        scheduler.add_job(self.remind_about_gamedle, 
                          CronTrigger(hour=10 + 12))

        # remind about smashdle at 1a EST
        scheduler.add_job(self.remind_about_smashdle, 
                          CronTrigger(hour=1))

        scheduler.start()
        print_petrichor_msg('-dle reminders setup completed')


    async def remind_about_rankdle(self) -> None:
        """
        Sends a reminder about rankdle refresh.
        """
        content = f'Rankdle has reset! https://rankdle.com/games/apex'
        await self.bot.get_channel(get_id('APEX_RANKDLE_ID')) \
                      .send(content=content)


    async def remind_about_wordle(self) -> None:
        """
        Sends a reminder about wordle refresh.
        """
        content = \
            f'Wordle has reset! https://www.nytimes.com/games/wordle/index.html'
        await self.bot.get_channel(get_id('APEX_WORDLE_ID')) \
                      .send(content=content)


    async def remind_about_bandle(self) -> None:
        """
        Sends a reminder about bandle refresh.
        """
        content = f'Bandle has reset! https://bandle.app/'
        await self.bot.get_channel(get_id('APEX_BANDLE_ID')) \
                      .send(content=content)


    async def remind_about_pokedle(self) -> None:
        """
        Sends a reminder about pokedle refresh.
        """
        content = f'Pokedle has reset! https://pokedle.io/'
        await self.bot.get_channel(get_id('APEX_POKEDLE_ID')) \
                      .send(content=content)


    async def remind_about_gamedle(self) -> None:
        """
        Sends a reminder about gamedle refresh.
        """
        content = f'Gamedle has reset! https://www.gamedle.wtf/guess#'
        await self.bot.get_channel(get_id('APEX_GAMEDLE_ID')) \
                      .send(content=content)


    async def remind_about_smashdle(self) -> None:
        """
        Sends a reminder about smashdle refresh.
        """
        content = f'Smashdle has reset! https://smashdle.net/classic'
        await self.bot.get_channel(get_id('APEX_SMASHDLE_ID')) \
                      .send(content=content)



async def setup(bot : commands.Bot) -> None:
    """
    Sets up the Cog.

    Parameters
    ----------
    bot : commands.Bot
        the bot to add the cog to
    """
    await bot.add_cog(RemindersCog(bot))

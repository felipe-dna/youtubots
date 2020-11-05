import logging

from typing import Any, Dict


class Bot:
    def __init__(self):
        self.__state: Dict[str, Any] = dict()
        self.bot_name: str = ''
        self.logger = logging.Logger(name=self.bot_name, level='INFO')
        self.state: str = 'offline'

    async def run(self) -> None:
        """
        Runs the bot.
        """
        self.logger.info(f'> Initializing the {self.bot_name}...')

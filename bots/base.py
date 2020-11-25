"""Contains the base robots class and all the other objects that it uses."""

import logging
from pprint import pformat
from typing import Any, Dict, List, Optional


class Bot:
    """
    An Factory class that contains all the basic behavior for construct any bot.
    """

    def __init__(self):
        """Initializes an new Bot instance."""
        self.__state: Dict[str, Any] = dict()
        self._bot_name: str = ''
        self.logger = Logger(bot_name=self.name)
        self.state = State()
        self.maximum_sentences = 7

        self.logger.log('Ready!')

    @property
    def name(self) -> str:
        """
        Returns the robot name property.

        :return: The current robot name property.
        """
        return self._bot_name

    @name.setter
    def name(self, bot_name: str) -> None:
        """
        Sets the robot name property.

        :param bot_name: The new robot name value.
        """
        self._bot_name = bot_name

    async def run(self) -> None:
        """Logs an message indicating that the robot started."""
        self.logger.log('Starting...')

    async def stop(self) -> None:
        """Logs some data about the robot processing."""
        self.logger.log(f'State updated: {pformat(self.state.changed_fields)}')
        self.logger.log('Finishing...')


class Logger:  # pylint: disable=too-few-public-methods
    """Provides custom logs for the robots."""

    def __init__(self, bot_name: str) -> None:
        """
        Initializes an new Logger instance.

        :param bot_name: The name of the robot.
        """
        self.log_format = '> [%(name)s] | %(levelname)s | %(message)s'
        logging.basicConfig(level=logging.INFO, format=self.log_format)
        self.logger = logging.getLogger(name=bot_name)

    def log(self, message: str, **kwargs: Dict[str, Any]) -> None:
        """
        Logs an message in the console by using the logging library.

        :param message: The message that will be logged.
        :param kwargs: Possible kwargs to pass to the logger.
        """
        self.logger.info(message, extra=kwargs)


class State:
    """
    An singleton that stores the session data and make it available for
    all the robots and the orchestrator.
    """

    __instance = None

    def __init__(self) -> None:
        """Initializes an new State object instance."""
        self.search_term: Optional[str] = None
        self.prefix: Optional[str] = None
        self.source_content_original: Optional[str] = None
        self.source_sanitized_content: Optional[str] = None
        self.sentences: List[str] = []
        self.changed_fields: List[str] = []

    def update(self, **kwargs: Dict[str, Any]) -> None:  # pylint: disable=unused-argument  # NOQA
        """
        Updates the state basing on the received kwargs.

        :param kwargs: The new state key and value.
        """
        __changed_fields: List[str] = []

        for state_name, state_value in kwargs.items():
            self.__setattr__(state_name, state_value)
            __changed_fields.append(state_name)

        self.changed_fields = __changed_fields

    def __call__(self, *args, **kwargs) -> Dict[str, Any]:
        return self.__dict__

    def __new__(cls, *args, **kwargs) -> "State":  # pylint: disable=unused-argument  # NOQA
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

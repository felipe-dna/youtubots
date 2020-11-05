import logging

from pprint import pformat
from typing import Any, Dict, List


class Bot:
    def __init__(self):
        self.__state: Dict[str, Any] = dict()
        self._bot_name: str = ''
        self.logger = Logger(bot_name=self.name)
        self.state = State()

        self.logger.log(f'Ready!')

    @property
    def name(self) -> str:
        return self._bot_name

    @name.setter
    def name(self, bot_name: str) -> None:
        self._bot_name = bot_name

    async def run(self) -> None:
        self.logger.log(f'Starting...')

    async def stop(self) -> None:
        self.logger.log(f'State updated: {pformat(self.state.changed_fields)}')
        self.logger.log('Finishing...')


class Logger:
    def __init__(self, bot_name: str) -> None:
        self.log_format = '> [%(name)s] | %(levelname)s | %(message)s'
        logging.basicConfig(level=logging.INFO, format=self.log_format)
        self.logger = logging.getLogger(name=bot_name)

    def log(self, message: str, **kwargs) -> None:
        self.logger.info(message, extra=kwargs)


class State:
    __instance = None
    changed_fields = ()

    def __init__(
            self,
            search_term: str = None,
            prefix: str = None,
            source_content_original: str = None,
            source_sanitized_content: str = None,
            sentences: List[Dict[str, Any]] = []
    ) -> None:
        self.search_term = search_term
        self.prefix = prefix
        self.source_content_original = source_content_original
        self.source_sanitized_content = source_sanitized_content
        self.sentences = sentences

    def update(self, **kwargs):
        __changed_fields = []

        for state_name, state_value in kwargs.items():
            self.__setattr__(state_name, state_value)
            __changed_fields.append(state_name)

        self.changed_fields = __changed_fields

    def __call__(self, *args, **kwargs):
        return self.__dict__

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

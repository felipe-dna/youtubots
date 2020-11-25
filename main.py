"""Contains the orchestrator object and the entry point to tun the robots."""
import asyncio

from bots.base import State
from bots.text import TextRobot


class Orchestrator:
    """
    Orchestrates all the flow. It is responsible for run each one of the robots.
    """
    state = State()

    # Registered robots.
    text_robot = TextRobot()

    async def ask_and_return_search_term(self) -> None:
        """
        Asks for the user write an search term and stores it in the state.
        """
        search_term: str = input('\nType a search term: ')
        self.state.update(search_term=search_term)

    async def ask_and_return_prefix(self) -> None:
        """
        Asks for the user select an prefix and stores it in the state.
        """
        prefixes = ('who is', 'what is', 'The history of')

        prefixes_with_indexes: str = '\n'.join(list(map(
            lambda index_and_prefix_tuple: '[{0}] {1}'.format(
                *index_and_prefix_tuple
            ),
            enumerate(iterable=prefixes, start=1)
        )))

        prefix_index: int = int(input(
            f'\n{prefixes_with_indexes}\nChoose an option: '
        ))

        self.state.update(prefix=prefixes[prefix_index - 1])
        print('\n')

    async def start(self) -> None:
        """
        Starts the orchestrator asking for the user the needed data and run the
        bots.
        """
        await self.ask_and_return_search_term()
        await self.ask_and_return_prefix()

        await self.text_robot.run()


if __name__ == '__main__':
    orchestrator = Orchestrator()
    asyncio.run(orchestrator.start())

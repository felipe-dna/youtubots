import asyncio

from bots.base import State
from bots.text import TextRobot


class Orchestrator:
    state = State()

    text_robot = TextRobot()

    async def ask_and_return_search_term(self) -> None:
        search_term: str = input('\nType a search term: ')
        self.state.update(search_term=search_term)

    async def ask_and_return_prefix(self) -> None:
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

    async def retrieve_data_to_initialize_robots(self) -> None:
        await self.ask_and_return_search_term()
        await self.ask_and_return_prefix()

    async def start(self):
        await self.retrieve_data_to_initialize_robots()
        await self.text_robot.run()


if __name__ == '__main__':
    orchestrator = Orchestrator()
    asyncio.run(orchestrator.start())

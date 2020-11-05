from bots.base import Bot


class TextRobot(Bot):
    name = 'Text Robot'

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

    async def run(self) -> None:
        await super().run()

        await self.ask_and_return_search_term()
        await self.ask_and_return_prefix()

        await self.stop()

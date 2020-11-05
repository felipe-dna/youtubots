import Algorithmia

from decouple import config as env

from bots.base import Bot


class TextRobot(Bot):
    name = 'Text Robot'

    @staticmethod
    async def instantiate_and_return_algorithmia_client() -> Algorithmia:
        __algorithmia_api_key = env('ALGORITHMIA_API_KEY')
        client = Algorithmia.client(__algorithmia_api_key)
        return client

    async def fetch_content_from_wikipedia(self) -> None:
        client = await self.instantiate_and_return_algorithmia_client()

        self.logger.log('Fetching content from Wikipedia...')

        wikipedia_algorithm = client.algo('web/WikipediaParser/0.1.2')

        self.logger.log(f'Looking for {self.state.search_term} in Wikipedia...')
        wikipedia_response = wikipedia_algorithm.pipe(self.state.search_term)
        wikipedia_content = wikipedia_response.result.get('content')

        print(wikipedia_content)

    async def sanitize_content(self) -> None:
        pass

    async def break_content_into_sentences(self) -> None:
        pass

    async def run(self) -> None:
        await super().run()

        await self.fetch_content_from_wikipedia()
        await self.sanitize_content()
        await self.break_content_into_sentences()

        await self.stop()

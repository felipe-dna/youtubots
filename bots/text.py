from typing import List

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

    async def remove_blank_lines_and_markdown(self, text: str) -> str:
        self.logger.log('Removing blank lines and markdown from the text...')

        all_lines: List[str] = text.split('\n')

        text_without_blank_lines_and_markdown: List[str] = list(filter(
            lambda line: (
                False if len(line) == 0 or line.startswith('=') else True
            ),
            all_lines
        ))

        return ' '.join(text_without_blank_lines_and_markdown)

    async def fetch_content_from_wikipedia(self) -> None:
        client = await self.instantiate_and_return_algorithmia_client()

        self.logger.log('Fetching content from Wikipedia...')

        wikipedia_algorithm = client.algo('web/WikipediaParser/0.1.2')

        self.logger.log(f'Looking for {self.state.search_term} in Wikipedia...')
        wikipedia_response = wikipedia_algorithm.pipe(self.state.search_term)
        wikipedia_content = wikipedia_response.result['content']

        self.state.update(source_content_original=wikipedia_content)

    async def sanitize_content(self) -> None:
        self.logger.log('Sanitizing wikipedia content...')

        cleaned_text = await self.remove_blank_lines_and_markdown(
            text=self.state.source_content_original
        )

        print(cleaned_text)

    async def break_content_into_sentences(self) -> None:
        pass

    async def run(self) -> None:
        await super().run()

        await self.fetch_content_from_wikipedia()
        await self.sanitize_content()
        await self.break_content_into_sentences()

        await self.stop()


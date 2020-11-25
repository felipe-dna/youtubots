"""Contains the TextRobot class."""
# pylint: disable=import-error

import json
import re
from pprint import pprint
from typing import Any, Dict, List, Set

from Algorithmia import client as AlgorithmiaClient
from decouple import config as env
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1 as Nlu
from pysbd import Segmenter

from bots.base import Bot


class TextRobot(Bot):
    """
    The TextRobot.

    It is responsible for:

    - Retrieve the data from the Wikipedia by using Algorithmia and the given
      search term;
    - Sanitize the retrieved content;
        - Remove blank lines;
        - Remove Markdown;
        - Remove dates inside parentheses;
    - Break the text into sentences;
    - Limit the sentences;
    - Find keywords for each one of the sentences;
    """

    name = 'Text Robot'
    __segmenter = Segmenter(language='en', clean=False)

    @staticmethod
    async def instantiate_and_return_algorithmia_client() -> AlgorithmiaClient:
        """
        Instantiates the Algorithmia client and returns it.

        :return: The instantiated Algorthmia client.
        """
        __algorithmia_api_key = env('ALGORITHMIA_API_KEY')
        client = AlgorithmiaClient(__algorithmia_api_key)

        return client

    @staticmethod
    async def instantiate_and_return_ibm_watson_client() -> Nlu:
        """
        Instantiates the Natural Language Understanding library passing the
        version we will use and an Authenticator object with the credentials.

        :return: An NaturalLanguageUnderstanding instance.
        """
        __authenticator = IAMAuthenticator(env('IBM_WATSON_API_KEY'))
        __nlu = Nlu(version='2018-11-16', authenticator=__authenticator)
        __nlu.set_service_url(env('IBM_WATSON_API_URL'))

        return __nlu

    async def remove_blank_lines_and_markdown(self, text: str) -> str:
        """
        Removes blank lines and markdown markers from the text.

        The wikipedia text can contain blank lines or markdown markers inside
        it, so this method will remove it by breaking the text into lines
        splitting it by the '\n' marker and then, filtering the lines where the
        text do not starts with '=' (markdown indicator on wikipedia content)
        and have an length greater than 0.

        :param text: The received wikipedia content.

        :return: The text without markdown and blank lines.
        """
        self.logger.log('Removing blank lines and markdown from the text...')

        all_lines: List[str] = text.split('\n')

        text_without_blank_lines_and_markdown: List[str] = list(filter(
            lambda line: not (len(line) == 0 or line.startswith('=')),
            all_lines
        ))

        return ' '.join(text_without_blank_lines_and_markdown)

    async def remove_dates_in_parentheses(self, text: str) -> str:
        """
        It removes dates inside parentheses from the text.

        It's important to remove this dates because it is, in the most of times,
        born and death date, and we do not want to show this information in the
        video.

        :param text: The retrieved wikipedia content.

        :return: The received text without the dates.
        """
        self.logger.log('Removing dates from the text...')

        text_without_dates = re.sub(
            r'\(\w{1,} \d{2}, \d{4} – \w{1,} \d{2}, \d{4}\)', '', text
        )

        return text_without_dates

    async def limit_maximum_sentences(
            self, sentences_list: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Receives an sentences list and returns the first N sentences.

        This N number must be configured in the robot class. It does this
        because in the video we need just a limited number of sentences, so use
        more than this in the next steps will be an memory and processing waste.

        :param sentences_list: An list of sentences.

        :return: The limited list of sentences.
        """
        return sentences_list[0:7]

    async def fetch_sentence_keywords(self, sentence: str) -> Set[str]:
        """
        Fetches keywords in an sentence using IBM watson and returns them.

        :param sentence: The sentence string from where the IBM Watson will
                         fetch the keywords.

        :return: An list with the fetched keywords.
        """
        watson_client = await self.instantiate_and_return_ibm_watson_client()

        response = watson_client.analyze(
            text=sentence,
            features={'keywords': {}}
        )

        response_result: List[Dict[str, Any]] = response.result['keywords']

        keywords: Set[str] = set(map(
            lambda keyword: keyword['text'], response_result
        ))

        return keywords

    async def fetch_content_from_wikipedia(self) -> None:
        """
        Fetches the content from the wikipedia according with the given search
        term.
        """
        client = await self.instantiate_and_return_algorithmia_client()

        self.logger.log('Fetching content from Wikipedia...')
        wikipedia_algorithm = client.algo('web/WikipediaParser/0.1.2')

        self.logger.log(
            f'Looking for {self.state.search_term} in Wikipedia...')
        wikipedia_response = wikipedia_algorithm.pipe(
            json.dumps(self.state.search_term))

        self.state.update(
            source_content_original=wikipedia_response.result['content']
        )

    async def sanitize_content(self) -> None:
        """
        Sanitizes the retrieved wikipedia content and stores it in the state.
        """
        self.logger.log('Sanitizing wikipedia content...')

        cleaned_text = await self.remove_blank_lines_and_markdown(
            text=self.state.source_content_original
        )

        text_without_dates = await self.remove_dates_in_parentheses(
            text=cleaned_text
        )

        self.state.update(source_sanitized_content=text_without_dates)

    async def break_content_into_sentences(self) -> None:
        """
        Breaks the retrieved wikipedia content into sentences and stores it in
        the state.
        """
        self.logger.log('Breaking the text in sentences...')

        sentences = self.__segmenter.segment(
            self.state.source_sanitized_content
        )

        sentences_list: List[Dict[str, Any]] = list(map(
            lambda sentence: {'text': sentence, 'keywords': [], 'images': []},
            sentences
        ))

        limited_sentences_list = await self.limit_maximum_sentences(
            sentences_list=sentences_list
        )

        self.state.update(sentences=limited_sentences_list)

    async def fetch_keywords_in_all_sentences(self) -> None:
        """
        Fetches keywords from all the sentences and stores them all in the
        state.
        """
        self.logger.log('Fetching keywords using IBM Watson...')

        for sentence_object in self.state.sentences:
            sentence_object['keywords'] = await self.fetch_sentence_keywords(
                sentence_object['text']
            )

        pprint(self.state.sentences)

    async def run(self) -> None:
        """
        Runs the TextRobot. Call each one of the steps.

        - Fetch te content from the wikipedia
        - Sanitize the retrieved content
        - break the content into sentences
        - fetch keywords from all the sentences
        """
        await super().run()

        await self.fetch_content_from_wikipedia()
        await self.sanitize_content()
        await self.break_content_into_sentences()
        await self.fetch_keywords_in_all_sentences()

        await self.stop()

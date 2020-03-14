import asyncio


async def start():
    content = dict()
    content["search-term"] = ask_and_return_search_term()

    print(content)


def ask_and_return_search_term():
    search_term = input("Type a Wikipedia search term: ")

    return search_term


if __name__ == "__main__":
    asyncio.run(start())

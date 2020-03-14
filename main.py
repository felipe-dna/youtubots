import asyncio


async def start():

    def ask_and_return_search_term():
        search_term = input("Type a Wikipedia search term: ")

        return search_term

    def ask_and_return_prefix():
        prefixes = ('Who is', 'What is', 'The history of')

        for index, prefix in enumerate(prefixes):
            print(f"[{index + 1}] - {prefix}")

        selected_prefix_index = input(f"Select a prefix: ")
        selected_prefix = prefixes[int(selected_prefix_index) - 1]

        return selected_prefix

    content = dict()
    content["search-term"] = ask_and_return_search_term()
    content["prefix"] = ask_and_return_prefix()

    print(content)

if __name__ == "__main__":
    asyncio.run(start())

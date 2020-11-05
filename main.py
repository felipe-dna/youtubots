import asyncio

from bots.text import TextRobot


class Orchestrator:
    text_robot = TextRobot()

    async def start(self):
        await self.text_robot.run()


if __name__ == '__main__':
    orchestrator = Orchestrator()
    asyncio.run(orchestrator.start())

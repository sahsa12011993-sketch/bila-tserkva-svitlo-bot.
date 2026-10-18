import asyncio
from dtek_client import DtekClient


async def main():
    async with DtekClient("krem") as client:
        streets = await client.get_streets("м.Біла Церква")
        print("Знайдено вулиць:", len(streets))

        for street in streets[:10]:
            print(street.name)


if __name__ == "__main__":
    asyncio.run(main())

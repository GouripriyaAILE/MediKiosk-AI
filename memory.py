import asyncio
from hindsight_client import Hindsight

API_KEY = "hsk_06f13e07411aa27f822e83452eff3b0c_aa8a5d956b2cbccd"

BANK_ID = "medikiosk"

BASE_URL = "https://api.hindsight.vectorize.io"


async def recall_memory(query):
    client = Hindsight(
        base_url=BASE_URL,
        api_key=API_KEY
    )

    try:
        result = await client.arecall(
            bank_id=BANK_ID,
            query=query
        )

        return result.results

    finally:
        await client.aclose()


async def retain_memory(content):
    client = Hindsight(
        base_url=BASE_URL,
        api_key=API_KEY
    )

    try:
        await client.aretain(
            bank_id=BANK_ID,
            content=content
        )

    finally:
        await client.aclose()


def get_memory(query):
    return asyncio.run(recall_memory(query))


def store_memory(content):
    asyncio.run(retain_memory(content))
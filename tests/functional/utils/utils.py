import aiohttp
from functional.settings import test_settings


async def make_request(
    service_path: str,
    query_data: list[dict] | None = None,
    service_url: str = f'http://{test_settings.service_url}:{test_settings.service_port}/api/v1',
) -> dict:
    session = aiohttp.ClientSession()
    url = service_url + service_path

    async with session.get(url, params=query_data) as response:
        body = await response.json()
        status = response.status
        headers = response.headers
    await session.close()
    return {'body': body, 'status': status, 'headers': headers}

from http import HTTPStatus

import pytest
from functional.utils.utils import make_request


@pytest.mark.asyncio
async def test_genres_list():
    response = await make_request(service_path='/genres')

    received_status = response['status']
    received_length = len(response['body'])
    assert received_status == HTTPStatus.OK
    assert received_length == 3


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'person_id': '120a21cf-9097-479e-904a-13dd7198c1dd'},
            {'status': HTTPStatus.OK, 'length': 2, 'name': 'Adventure'}
        ),
        (
            {'person_id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07f1'},
            {'status': HTTPStatus.NOT_FOUND, 'length': 1, 'name': 'List of genres not found'}
        ),
        (
            {'person_id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07f'},
            {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1, 'name': 'value is not a valid uuid'}
        ),
    ]
)
@pytest.mark.asyncio
async def test_get_genre_by_id(
        query_data,
        expected_answer,
):
    response = await make_request(service_path=f'/genres/{query_data["person_id"]}')

    received_status = response['status']
    received_length = len(response['body'])
    match received_status:
        case HTTPStatus.NOT_FOUND: received_name = response['body']['detail']
        case HTTPStatus.UNPROCESSABLE_ENTITY: received_name = response['body']['detail'][0]['msg']
        case _: received_name = response['body']['name']

    expected_status = expected_answer['status']
    expected_length = expected_answer['length']
    expected_name = expected_answer['name']

    assert received_status == expected_status
    assert received_length == expected_length
    assert received_name == expected_name


@pytest.mark.asyncio
async def test_if_genre_cache(
        set_up_and_flush_cache,
        redis_client,
):
    await make_request(service_path='/genres/120a21cf-9097-479e-904a-13dd7198c1dd')

    cache = await redis_client.get('120a21cf-9097-479e-904a-13dd7198c1dd_genre_details')

    assert cache

from http import HTTPStatus

import pytest
from functional.utils.utils import make_request


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'query': '*Kolber*', 'page[number]': '1', 'page[size]': '50'},
            {'status': HTTPStatus.OK, 'length': 2}
        ),
        (
            {'query': 'somthing', 'page[number]': '1', 'page[size]': '50'},
            {'status': HTTPStatus.NOT_FOUND, 'length': 1}
        ),
        (
            {'query': 'George*', 'page[number]': '-1', 'page[size]': '50'},
            {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1}
        ),
        (
            {'query': 'George*', 'page[number]': '1', 'page[size]': '-1'},
            {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1}
        ),
        (
            {
                'query': 'A string more then 50 chars length 12345678901234567890123',
                'page[number]': '1',
                'page[size]': '50'
            },
            {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1}
        ),
    ]
)
@pytest.mark.asyncio
async def test_persons_search(
        query_data,
        expected_answer
):
    response = await make_request(
        service_path='/persons/search',
        query_data=query_data
    )

    received_status = response['status']
    expected_status = expected_answer['status']
    received_length = len(response['body'])
    expected_length = expected_answer['length']
    assert received_status == expected_status
    assert received_length == expected_length


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'person_id': '11c6187d-69f5-4587-b19a-6113946f8f54'},
            {'status': HTTPStatus.OK, 'length': 4}
        ),
        (
            {'person_id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07f1'},
            {'status': HTTPStatus.NOT_FOUND, 'length': 1}
        ),
        (
            {'person_id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07f'},
            {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1}
        ),
    ]
)
@pytest.mark.asyncio
async def test_get_persons_by_id(
        query_data,
        expected_answer
):
    response = await make_request(
        service_path=f'/persons/{query_data["person_id"]}',
        query_data={}
    )

    received_status = response['status']
    expected_status = expected_answer['status']
    received_length = len(response['body'])
    expected_length = expected_answer['length']
    assert received_status == expected_status
    assert received_length == expected_length


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'person_id': '11c6187d-69f5-4587-b19a-6113946f8f54'},
            {'status': HTTPStatus.OK, 'length': 5}
        ),
        (
            {'person_id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07f1'},
            {'status': HTTPStatus.NOT_FOUND, 'length': 1}
        ),
        (
            {'person_id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07f'},
            {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1}
        ),
    ]
)
@pytest.mark.asyncio
async def test_get_persons_by_id_detailed(
        query_data,
        expected_answer
):
    response = await make_request(
        service_path=f'/persons/{query_data["person_id"]}/detailed',
        query_data={}
    )

    received_status = response['status']
    expected_status = expected_answer['status']
    received_length = len(response['body'])
    expected_length = expected_answer['length']
    assert received_status == expected_status
    assert received_length == expected_length


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'person_id': '11c6187d-69f5-4587-b19a-6113946f8f54'},
            {'status': HTTPStatus.OK, 'length': 1}
        ),
        (
            {'person_id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07f1'},
            {'status': HTTPStatus.NOT_FOUND, 'length': 1}
        ),
        (
            {'person_id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07f'},
            {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1}
        ),
    ]
)
@pytest.mark.asyncio
async def test_persons_id_film(
        query_data,
        expected_answer
):
    response = await make_request(
        service_path=f'/persons/{query_data["person_id"]}/film',
        query_data={'sorting': 'true'}
    )

    received_status = response['status']
    expected_status = expected_answer['status']
    received_length = len(response['body'])
    expected_length = expected_answer['length']
    assert received_status == expected_status
    assert received_length >= expected_length

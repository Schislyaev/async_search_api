import json
from http import HTTPStatus

import pytest
from functional.utils.utils import make_request


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'filmwork_id': '793a77e4-7ab8-11ed-a1eb-0242ac120002'},
                {'status': HTTPStatus.OK, 'length': 8,
                 'keys': ['id', 'title', 'imdb_rating', 'description', 'genre', 'actors', 'writers', 'director']}
        ),
        (
                {'filmwork_id': '793a77e4-7ab8-11ed-a1eb-0242ac121112'},
                {'status': HTTPStatus.NOT_FOUND, 'length': 1}
        ),
        (
                {'filmwork_id': '793a77e4-7ab8-11ed-a1eb-0242ac121'},
                {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1}
        ),
    ]
)
@pytest.mark.asyncio
async def test_films_by_id(
        query_data,
        expected_answer,
):
    response = await make_request(
        service_path='/films/{}'.format(query_data['filmwork_id']),
    )

    received_status = response['status']
    expected_status = expected_answer['status']
    received_length = len(response['body'])
    expected_length = expected_answer['length']
    response = json.dumps(response['body'])
    assert received_status == expected_status
    assert received_length == expected_length
    if expected_answer['status'] == HTTPStatus.OK:
        for key in expected_answer['keys']:
            assert key in response


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'page[number]': 1, 'page[size]': 3, 'imdb_ratings': [8.5, 7, 6]},
                {'status': HTTPStatus.OK, 'length': 3}
        ),
        (
                {'sort': 'imdb_rating', 'page[number]': 1, 'page[size]': 3, 'imdb_ratings': [6, 7, 8.5]},
                {'status': HTTPStatus.OK, 'length': 3}
        ),
        (
                {'page[number]': 1, 'page[size]': 2, 'imdb_ratings': [8.5, 7]},
                {'status': HTTPStatus.OK, 'length': 2}
        ),
        (
                {'filters': '7c637264-7abc-11ed-a1eb-0242ac120002',
                 'page[number]': 1, 'page[size]': 3, 'imdb_ratings': [6]},
                {'status': HTTPStatus.OK, 'length': 1}
        ),
        (
                {'filters': 'bbb193d2-7ab8-11ed-a1eb-0242ac120002', 'sort': 'imdb_rating',
                 'page[number]': 1, 'page[size]': 3, 'imdb_ratings': [7, 8.5]},
                {'status': HTTPStatus.OK, 'length': 2}
        ),
        (
                {'imdb_ratings': [8.5, 7, 6]},
                {'status': HTTPStatus.OK, 'length': 3}
        ),
        (
                {'filters': 'bbb193d2-7ab8-11ed-a1eb-0242ac1'},
                {'status': HTTPStatus.UNPROCESSABLE_ENTITY}
        ),
        (
                {'filters': 'bbb193d2-7ab8-11ed-a1eb-0242ac1', 'page[number]': 1, 'page[size]': -1},
                {'status': HTTPStatus.UNPROCESSABLE_ENTITY}
        ),
        (
                {'filters': 'bbb193d2-7ab8-11ed-a1eb-0242ac120002', 'page[number]': 50, 'page[size]': 1},
                {'status': HTTPStatus.NOT_FOUND}
        ),
    ]
)
@pytest.mark.asyncio
async def test_films_sorted_list(
        query_data,
        expected_answer
):
    response = await make_request(
        service_path='/films',
        query_data=query_data
    )
    received_status = response['status']
    assert received_status == expected_answer['status']
    if expected_answer['status'] == HTTPStatus.OK:
        response = response['body']['result']
        for number, row in enumerate(response):
            assert 'imdb_rating' in row
            assert 'title' in row
            assert 'id' in row
            assert response[number]['imdb_rating'] == query_data['imdb_ratings'][number]
        assert len(response) == expected_answer['length']


@pytest.mark.asyncio
async def test_search():
    response = await make_request(
        service_path='/films/search/',
        query_data={
            'query': 'Star Wars',
            'page[number]': '1',
            'page[size]': '50 ',
        },
    )

    assert response['body']['result'] == [
        {
            'id': '793a77e4-7ab8-11ed-a1eb-0242ac120002',
            'title': 'Star Wars: Last Chance',
            'imdb_rating': 7.0,
        },
        {
            'id': '6c3c2d54-7abc-11ed-a1eb-0242ac120002',
            'title': 'Star Warses',
            'imdb_rating': 6.0,
        }
    ]


@pytest.mark.asyncio
async def test_search_not_found():
    response = await make_request(
        service_path='/films/search/',
        query_data={
            'query': 'test',
            'page[number]': '1',
            'page[size]': '50 ',
        },
    )

    assert response['status'] == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_search_page_size_filter():
    response = await make_request(
        service_path='/films/search/',
        query_data={
            'query': 'Star Wars',
            'page[number]': '1',
            'page[size]': '1 ',
        },
    )

    assert len(response['body']) == 1


@pytest.mark.asyncio
async def test_search_page_number_filter():
    response = await make_request(
        service_path='/films/search/',
        query_data={
            'query': 'Star Wars',
            'page[number]': '2',
            'page[size]': '1 ',
        },
    )

    assert response['body']['result'][0] == {
        'id': '6c3c2d54-7abc-11ed-a1eb-0242ac120002',
        'title': 'Star Warses',
        'imdb_rating': 6.0,
    }


@pytest.mark.parametrize(
    'query_data',
    [
        {'query': 'Star', 'page[number]': '-1', 'page[size]': '50'},
        {'query': 'Star', 'page[number]': '1', 'page[size]': '-1'},
    ]
)
@pytest.mark.asyncio
async def test_search_filter_validation(query_data):
    response = await make_request(
        service_path='/films/search/',
        query_data=query_data,
    )

    assert response['status'] == HTTPStatus.UNPROCESSABLE_ENTITY

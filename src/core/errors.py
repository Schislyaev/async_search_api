"""
Хранение констант сообщений об ошибках.
"""

from pydantic import BaseModel


class Films(BaseModel):
    search_not_found: str = 'Nothing found'
    list_not_found: str = 'List of films not found'
    details_not_found: str = 'Film not found'


class Persons(BaseModel):
    search_not_found: str = 'Nothing found, try to use wildcards'
    details_not_found: str = 'Person not found'
    details_detailed_not_found: str = 'Person not found'
    films_details_not_found: str = 'Persons in this film not found'


class Genres(BaseModel):
    details_not_found: str = 'Details not found'
    list_not_found: str = 'List of genres not found'

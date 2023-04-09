FILMWORKS_DATA = [
    {
        "_id": "793a77e4-7ab8-11ed-a1eb-0242ac120002",
        "_source": {
            "id": "793a77e4-7ab8-11ed-a1eb-0242ac120002",
            "imdb_rating": 7.0,
            "genre": [{
                "id": "bbb193d2-7ab8-11ed-a1eb-0242ac120002",
                "name": "Fantasy",
            }],
            "title": "Star Wars: Last Chance",
            "description": "Greatest film of the year",
            "director":
            [{
                "id": "3092f808-7ab9-11ed-a1eb-0242ac120002",
                "name": "George Lu"
            }],
            "actors_names": ["Frank", "Micholas", "Louis"],
            "writers_names": ["John", "Kate"],
            "actors": [{
                "id": "9e17d88a-7ab9-11ed-a1eb-0242ac120002",
                "name": "Nicholas Menret",
            }],
            "writers": [{
                "id": "c908e3c2-7ab9-11ed-a1eb-0242ac120002",
                "name": "Andrew Fox",
            }]
        },
    },
    {
        "_id": "e782b936-7ab9-11ed-a1eb-0242ac120002",
        "_source": {
            "id": "e782b936-7ab9-11ed-a1eb-0242ac120002",
            "imdb_rating": 8.5,
            "genre": {
                "id": "bbb193d2-7ab8-11ed-a1eb-0242ac120002",
                "name": "Horror",
            },
            "title": "Captain Black",
            "description": "Amazing drama fixtion",
            "director":
                {
                    "id": "1147cab8-7aba-11ed-a1eb-0242ac120002",
                    "name": "Inokentiy Force"
                },
            "actors_names": ["Ken", "Nicholas"],
            "writers_names": ["Vladimir"],
            "actors": {
                "id": "2f22ed60-7aba-11ed-a1eb-0242ac120002",
                "name": "Fred Washington",
            },
            "writers": {
                "id": "53b4d04c-7abc-11ed-a1eb-0242ac120002",
                "name": "Steve Cork",
            }
        },
    },
    {
        "_id": "6c3c2d54-7abc-11ed-a1eb-0242ac120002",
        "_source": {
            "id": "6c3c2d54-7abc-11ed-a1eb-0242ac120002",
            "imdb_rating": 6.0,
            "genre": {
                "id": "7c637264-7abc-11ed-a1eb-0242ac120002",
                "name": "Detective",
            },
            "title": "Star Warses",
            "description": "Bad film",
            "director":
                {
                    "id": "3018c994-7abd-11ed-a1eb-0242ac120002",
                    "name": "Megan Krag"
                },
            "actors_names": ["Lui", "Gomer", "Frank", "Louis"],
            "writers_names": ["Kate"],
            "actors": {
                "id": "52060c88-7abd-11ed-a1eb-0242ac120002",
                "name": "Krage Finders",
            },
            "writers": {
                "id": "5e20c40e-7abd-11ed-a1eb-0242ac120002",
                "name": "Frog German",
            }
        },
    },
]

FILMWORK_INDEX = '''{
    "settings": {
        "refresh_interval": "1s",
        "analysis": {
            "filter": {
                "english_stop": {
                    "type": "stop",
                    "stopwords": "_english_"
                },
                "english_stemmer": {
                    "type": "stemmer",
                    "language": "english"
                },
                "english_possessive_stemmer": {
                    "type": "stemmer",
                    "language": "possessive_english"
                },
                "russian_stop": {
                    "type": "stop",
                    "stopwords": "_russian_"
                },
                "russian_stemmer": {
                    "type": "stemmer",
                    "language": "russian"
                }
            },
            "analyzer": {
                "ru_en": {
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "english_stop",
                        "english_stemmer",
                        "english_possessive_stemmer",
                        "russian_stop",
                        "russian_stemmer"
                    ]
                }
            }
        }
    },
    "mappings": {
        "dynamic": "true",
        "properties": {
            "id": {
                "type": "keyword"
            },
            "imdb_rating": {
                "type": "float"
            },
            "genre": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "id": {
                        "type": "keyword"
                    },
                    "name": {
                        "type": "text",
                        "analyzer": "ru_en"
                    }
                }
            },
            "title": {
                "type": "text",
                "analyzer": "ru_en",
                "fields": {
                    "raw": {
                        "type": "keyword"
                    }
                }
            },
            "description": {
                "type": "text",
                "analyzer": "ru_en"
            },
            "director": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "id": {
                        "type": "keyword"
                    },
                    "name": {
                        "type": "text",
                        "analyzer": "ru_en"
                    }
                }
            },
            "actors_names": {
                "type": "text",
                "analyzer": "ru_en"
            },
            "writers_names": {
                "type": "text",
                "analyzer": "ru_en"
            },
            "actors": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "id": {
                        "type": "keyword"
                    },
                    "name": {
                        "type": "text",
                        "analyzer": "ru_en"
                    }
                }
            },
            "writers": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "id": {
                        "type": "keyword"
                    },
                    "name": {
                        "type": "text",
                        "analyzer": "ru_en"
                    }
                }
            }
        }
    }
}
'''

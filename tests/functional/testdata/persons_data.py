PERSONS_INDEX = '''{
  "settings": {
    "refresh_interval": "1s",
    "analysis": {
      "filter": {
        "english_stop": {
          "type":       "stop",
          "stopwords":  "_english_"
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
          "type":       "stop",
          "stopwords":  "_russian_"
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
      "full_name": {
        "type": "keyword",
        "fields": {
          "raw": {
            "type":  "keyword"
          }
        }
      },
      "director_films": {
        "type": "nested",
        "dynamic": "strict",
        "properties": {
          "id": {
            "type": "keyword"
          },
          "title": {
            "type": "text",
            "analyzer": "ru_en"
          },
          "imdb_rating": {
            "type": "float"
          }
        }
      },
      "actor_films": {
        "type": "nested",
        "dynamic": "strict",
        "properties": {
          "id": {
            "type": "keyword"
          },
          "title": {
            "type": "text",
            "analyzer": "ru_en"
          },
          "imdb_rating": {
            "type": "float"
          }
        }
      },
      "writer_films": {
        "type": "nested",
        "dynamic": "strict",
        "properties": {
          "id": {
            "type": "keyword"
          },
          "title": {
            "type": "text",
            "analyzer": "ru_en"
          },
          "imdb_rating": {
            "type": "float"
          }
        }
      }
    }
  }
}
'''


PERSONS_DATA = [
    {
        "_id": "11c6187d-69f5-4587-b19a-6113946f8f54",
        "_source": {
            'id': '11c6187d-69f5-4587-b19a-6113946f8f54',
            'full_name': 'Gerald Potterton',
            'director_films': [
                {
                    'id': 'a59f548f-e660-4994-ae5e-ed3c911225d3',
                    'title': 'Some title',
                    'imdb_rating': 0.6
                }
            ],
            'actor_films': [
                {
                    'id': 'a59f548f-e660-4994-ae5e-ed3c911225d3',
                    'title': 'Some title',
                    'imdb_rating': 0.7
                }
            ],
            'writer_films': [
                {
                    'id': 'a59f548f-e660-4994-ae5e-ed3c911225d3',
                    'title': 'Some title',
                    'imdb_rating': 0.8
                }
            ]
        }
    },
    {
        "_id": "3d772bf3-3263-4b4e-93f4-ab6fa1c35c58",
        "_source": {
            'id': '3d772bf3-3263-4b4e-93f4-ab6fa1c35c58',
            'full_name': 'Dave Broadfoot Kolber',
            'director_films': [
                {
                    'id': 'a59f548f-e660-4994-ae5e-ed3c911225d3',
                    'title': 'Some title',
                    'imdb_rating': 0.7
                }
            ],
            'actor_films': [
                {
                    'id': 'a59f548f-e660-4994-ae5e-ed3c911225d3',
                    'title': 'Some title',
                    'imdb_rating': 0.6
                }
            ],
            'writer_films': []
        }
    },
    {
        "_id": "c8fd73f6-5046-4860-b420-884cd6f30c54",
        "_source": {
            'id': 'c8fd73f6-5046-4860-b420-884cd6f30c54',
            'full_name': 'Lynne Kolber',
            'director_films': [
                {
                    'id': 'a59f548f-e660-4994-ae5e-ed3c911225d3',
                    'title': 'Some title',
                    'imdb_rating': 0.5
                }
            ],
            'actor_films': [],
            'writer_films': [
                {
                    'id': 'a59f548f-e660-4994-ae5e-ed3c911225d3',
                    'title': 'Some title',
                    'imdb_rating': 0.7
                }
            ]
        }
    }
]

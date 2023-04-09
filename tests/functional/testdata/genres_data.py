GENRES_DATA = [
  {
    "_id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff",
    "_source": {
      "id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff",
      "name": "Action"
    },
  },
  {
    "_id": "120a21cf-9097-479e-904a-13dd7198c1dd",
    "_source": {
      "id": "120a21cf-9097-479e-904a-13dd7198c1dd",
      "name": "Adventure"
    },
  },
  {
    "_id": "5373d043-3f41-4ea8-9947-4b746c601bbd",
    "_source": {
      "id": "5373d043-3f41-4ea8-9947-4b746c601bbd",
      "name": "Comedy"
    },
  }
]

GENRES_INDEX = '''{
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
    "dynamic": "strict",
    "properties": {
      "id": {
        "type": "keyword"
      },
      "name": {
        "type": "keyword"
      }
    }
  }
}
'''

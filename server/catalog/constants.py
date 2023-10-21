ES_INDEX = "beer"

ES_MAPPING = {
    "dynamic": "strict",
    "properties": {
        "style": {
            "type": "text",
            "analyzer": "english",
        },
        "name": {
            "type": "text",
            "analyzer": "english",
        },
        "country": {
            "type": "keyword",
        },
        "price": {
            "type": "keyword",
        },
        "brewery": {
            "type": "text",
            "analyzer": "english",
        },
        "description": {
            "type": "text",
            "analyzer": "english",
        },
        "points": {
            "type": "float",
        },
    },
}

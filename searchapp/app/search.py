from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from typing import List

from searchapp.constants import INDEX_NAME

HEADERS = {'content-type': 'application/json'}


class SearchResult():
    """Represents a product returned from elasticsearch."""
    def __init__(self, id_, title, track_rating, album_name, artist_name, artist_rating, lyrics):
        self.id = id_
        self.title = title
        self.track_rating = track_rating
        self.album_name = album_name
        self.artist_name = artist_name
        self.artist_rating = artist_rating
        self.lyrics = lyrics

    def from_doc(doc) -> 'SearchResult':
        return SearchResult(
                id_ = doc.meta.id,
                title = doc.title,
                track_rating = doc.track_rating,
                album_name = doc.album_name,
                artist_name = doc.artist_name,
                artist_rating = doc.artist_rating,
                lyrics = doc.lyrics
            )


def search(term: str, count: int) -> List[SearchResult]:
    client = Elasticsearch()

    # Elasticsearch 6 requires the content-type header to be set, and this is
    # not included by default in the current version of elasticsearch-py
    client.transport.connection_pool.connection.headers.update(HEADERS)

    s = Search(using=client, index=INDEX_NAME)
    title_query = {'match': {'title': {'query': term, 'operator': 'and', 'fuzziness': 'AUTO'}}}
    #lyrics_query = {'match': {'lyrics': {'query': term, 'operator': 'and', 'fuzziness':'AUTO'}}}
    #name_query = {'term': {'name.english_analyzed': term}}
    dis_max_query = {'dis_max': {'queries': [title_query]}}

    docs = s.query(dis_max_query)[:count].execute()

    print(docs[0].title)

    return [SearchResult.from_doc(d) for d in docs]

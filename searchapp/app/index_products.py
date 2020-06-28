from elasticsearch import Elasticsearch, helpers
from sinling import SinhalaTokenizer
from searchapp.constants import INDEX_NAME
from searchapp.data import all_songs, SongData


def main():
    # Connect to localhost:9200 by default.
    es = Elasticsearch()

    es.indices.delete(index=INDEX_NAME, ignore=404)
    es.indices.create(
        index=INDEX_NAME,
        body={
            'mappings': {
        		'properties': {
        			'lyrics': {
        				'type': 'text',
        				'fields': {
        					'lyrics_analyzed': {
        						'type': 'text',
        						'analyzer': 'Sinhala_lyrics_analyzer'
        					}
        				}
        			}#,
        			#'description': {
        			#	'type': 'text',
        			#	'fields': {
        			#		'english_analyzed': {
        			#			'type': 'text',
        			#			'analyzer': 'custom_english_analyzer'
        			#		}
        			#	}
        			#}
        		}
            },
            'settings': {	
                'analysis': {
                    'analyzer': {
                        'Sinhala_lyrics_analyzer': {
                            'type': 'custom',
                            'tokenizer': 'SinhalaTokenizer'
                        }
                    }
                }
            },
        },
    )

    #index_product(es, all_products())
    songs_to_index(es, all_songs())

def index_song(es, songs):
    """Add a single product to the ProductData index."""
    for song in songs:
	    es.create(
	        index=INDEX_NAME,
	        id=song.id,
	        body={
	            "title": song.title,
	            "track_rating": song.track_rating,
	            "artist_name": song.artist_name,
	            "artist_rating": song.artist_rating,
                "album_name": song.album_name,
	            "lyrics": song.lyrics
	        },
	        request_timeout=10
	    )

    # Don't delete this! You'll need it to see if your indexing job is working,
    # or if it has stalled.
    print("Indexed {}".format("A Great Song"))

def songs_to_index(es, songs):
	actions = [
		{
		"_index": INDEX_NAME,
	    "_id": i.id,
        "_source":{
        	"title": i.title,
            "track_rating": i.track_rating,
            "artist_name": i.artist_name,
            "artist_rating": i.artist_rating,
            "album_name": i.album_name,
            "lyrics": i.lyrics
        	}
		}
		for i in songs
	]
	helpers.bulk(es, actions)
	print("Indexed {}".format("bulk indexing done"))


if __name__ == '__main__':
    main()
SUPERFAVE_SCORE: int = 5
FAVE_SCORE: int = 1

def song_score_aggregate(score_per: int):
    return [
        {
            '$group': {
                '_id': '$song',
                'points': {
                    '$sum': score_per
                }
            }
        }, {
            '$sort': {
                'points': -1
            }
        }, {
            '$project': {
                '_id': 0,
                'song': '$_id',
                'points': 1
            }
        }
    ]

all_songs_ranked =[
    {
        '$project': {
            'song': '$song',
            'points': {
                '$literal': FAVE_SCORE
            }
        }
    }, {
        '$unionWith': {
            'coll': 'superfaves',
            'pipeline': [
                {
                    '$project': {
                        'song': '$song',
                        'points': {
                            '$literal': SUPERFAVE_SCORE
                        }
                    }
                }
            ]
        }
    }, {
        '$group': {
            '_id': '$song',
            'points': {
                '$sum': '$points'
            }
        }
    }, {
        '$project': {
            'song': '$_id',
            'points': 1
        }
    }, {
        '$sort': {
            'points': -1
        }
    }
]

user_fave_points = [
    {
        '$project': {
            'song': '$song',
            'user': '$user_id',
            'points': {
                '$literal': FAVE_SCORE
            }
        }
    }, {
        '$unionWith': {
            'coll': 'superfaves',
            'pipeline': [
                {
                    '$project': {
                        'song': '$song',
                        'user': '$user_id',
                        'points': {
                            '$literal': SUPERFAVE_SCORE
                        }
                    }
                }
            ]
        }
    }, {
        '$group': {
            '_id': '$user',
            'voted': {
                '$sum': '$points'
            }
        }
    }, {
        '$sort': {
            'voted': -1
        }
    }
]

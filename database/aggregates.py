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
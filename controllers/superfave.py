from controllers.fave import FaveController


class SuperfaveController(FaveController):
    collection_name = 'superfaves'
    points_per_fave = 5

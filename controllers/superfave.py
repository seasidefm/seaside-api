from controllers.fave import FaveController


class SuperFaveController(FaveController):
    super.collection_name = 'superfaves'

class AppResponse:
    def __init__(self, message="", error=None, data=None, code=200):
        self.message = message
        self.error = error
        self.data = data
        self.code = code

    def to_dict(self):
        return {
            "message": self.message,
            "error": self.error,
            "data": self.data
        }

    def response_tuple(self):
        return (
            self.to_dict(),
            self.code
        )


class AppResult(AppResponse):
    pass


class AppError(AppResponse):
    pass

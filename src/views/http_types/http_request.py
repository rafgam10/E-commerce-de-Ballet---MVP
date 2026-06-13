class HttpRequest:

    def __init__(
        self, header: dict = None, body: dict = None, path_params: dict = None
    ):

        self.headers = header
        self.body = body
        self.path_params = path_params

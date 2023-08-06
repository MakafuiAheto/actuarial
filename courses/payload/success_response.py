class AuthorCreationSuccessResponse:

    def __init__(self, message, jwtResponse):
        super().__init__(self.message, self.jwtResponse)
        self.message = message
        self.jwtResponse = jwtResponse

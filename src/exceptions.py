class FileWithNoContentException(Exception):
    """ File without content exception """

    def __init__(self, code, message):
        super(FileWithNoContentException, self).__init__()
        self.code = code
        self.message = message

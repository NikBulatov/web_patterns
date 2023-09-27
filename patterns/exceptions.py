class DBCommitException(Exception):
    def __init__(self, message):
        super().__init__(f"DB commit error: {message}")


class DBUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f"DB update error: {message}")


class DBDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f"DB delete error: {message}")


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f"Record not found: {message}")
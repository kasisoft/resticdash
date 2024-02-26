class ResticDashException(Exception):

    def __init__(self, message: str, cause: Exception = None):
        super().__init__(message)
        self.cause = cause

    # @property
    def __str__(self):
        cause_str = f": (Cause: {self.cause})" if self.cause else ""
        return f"{super().__str__()}{cause_str}"

    @staticmethod
    def wrap(ex: Exception):
        if isinstance(ex, ResticDashException):
            return ex
        return ResticDashException(str(ex), ex)

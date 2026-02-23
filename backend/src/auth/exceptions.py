class BusinessRuleException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class InvalidRefreshTokenException(BusinessRuleException):
    pass


class InvalidTokenException(BusinessRuleException):
    pass

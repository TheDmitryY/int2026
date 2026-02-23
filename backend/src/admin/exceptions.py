from src.auth.exceptions import BusinessRuleException


class NotFoundException(BusinessRuleException):
    pass


class BanException(BusinessRuleException):
    pass


class UnBanException(BusinessRuleException):
    pass

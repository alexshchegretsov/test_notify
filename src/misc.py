class TemplateType:
    NAMED = 'named'
    UNNAMED = 'unnamed'

    __slots__ = ()

    @classmethod
    def as_list(cls):
        return [cls.NAMED, cls.UNNAMED]


class JobCustomer:
    ADMIN = 'admin'
    API = 'api'
    PERIODIC = 'periodic'

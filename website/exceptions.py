class WrongPasswdException(Exception):
    def __unicode__(self):
        return u"the password aren't the same"


class MissingFieldException(Exception):
    def __init__(self, field):
        self.field = field

    def __unicode__(self):
        return u""
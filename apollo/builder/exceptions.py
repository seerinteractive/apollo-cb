class MethodError(Exception):
    pass


class NestedFoldersForbidden(Exception):
    pass


class ListAsValueRequired(Exception):
    pass


class OnlyStringsOrIntsAllow(Exception):
    pass


class MoreThanOneKeySupplied(Exception):
    pass


class DelimiterMustBeString(Exception):
    pass


class WrongDataType(Exception):
    def __init__(self, submitted, accepted):
        self.submitted = submitted
        self.accepted = accepted if isinstance(accepted, (list, tuple)) else [accepted]

    def __str__(self):
        accepted_str = ", ".join([name.__name__ for name in self.accepted])
        return f"{self.submitted.__class__.__name__} was given but {accepted_str} is accepted."

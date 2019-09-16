from apollo.request.abstract import RequestABC


class RequestBase(RequestABC):

    @property
    def header(self):
        return dict()

    @property
    def param(self):
        return dict()

    @property
    def auth(self):
        return tuple()

from abc import ABC
from abc import abstractmethod
from abc import abstractproperty


class RequestABC(ABC):
    @abstractproperty
    def header(self):
        pass

    @abstractproperty
    def param(self):
        pass

    @abstractproperty
    def auth(self):
        pass

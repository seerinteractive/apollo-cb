from abc import ABC
from abc import abstractmethod
from abc import abstractproperty


class FileStorageABC(ABC):
    @abstractmethod
    def write(self):
        pass

    @abstractmethod
    def read(self):
        pass

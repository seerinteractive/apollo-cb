from apollo.storage.abstract import FileStorageABC


class StorageBase(FileStorageABC):
    """Used for storing data. Implemented by the :class:`~apollo.ApolloCB`.

    """

    def write(self, *args, **kwargs):
        """Must implement a write function. ``file_path`` and ``data`` are recommended parameters, but not mandatory.

        """
        pass

    def read(self, *args, **kwargs):
        # TODO
        pass
